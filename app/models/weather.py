from services.http_requests import http_get
import machine


class Weather:
    WEATHER_API_HOURLY = "https://www.meteosource.com/api/v1/free/point?lat=50.098011&lon=19.891431&sections=hourly&timezone=CET&language=en&units=auto&key=kqngt51q4u1xid9ys4orkxcofumfllqkthcp3dp0"
    WEATHER_API_SUNRISE = "http://api.weatherapi.com/v1/forecast.json?key=21c1dc7e612f4f448b9131803251104&q=50.098011,19.891431&days=1&aqi=no&alerts=no"

    def __init__(self):
        self.sunrise = None
        self.sunset = None
        self.clouds = None
        self.date = None

    def get_weather(self) -> tuple[dict[int, int], int, int]:
        today = machine.RTC().datetime()[:3]
        if self.date != today:
            try:
                self._update_weather()
            except Exception as e:
                print("Error updating weather data:", e)
                return self._default_weather()
            else:
                self.date = today
        return self.clouds, self.sunrise, self.sunset

    def _default_weather(self) -> tuple[dict[int, int], int, int]:
        "returns default weather data - used when API is unavailable - 100% clouds"
        return {hour: 100 for hour in range(0, 25)}, 5, 19

    def _update_weather(self):
        self.clouds = self._get_clouds_hourly()
        self.sunrise, self.sunset = self._parsed_day_times().values()

    def _get_clouds_hourly(self) -> dict[int, int]:
        "returns dict containing: {1: 88} // {hour: cloud_cover(0-100)}"
        return {
            hourly_weather["date"][11:13]: hourly_weather["cloud_cover"]["total"]
            for hourly_weather in http_get(self.WEATHER_API_HOURLY, True)["hourly"][
                "data"
            ]
        }

    def _parsed_day_times(self) -> dict[str, int]:
        "returns dict: {sunrise: 6, sunset: 18}"
        return {
            key: int(value[:2]) + (12 if value[-2:] == "PM" else 0)
            for key, value in self._get_day_times().items()
        }

    def _get_day_times(self) -> dict[str, str]:
        "returns dict: {'sunrise': '06:00 AM', 'sunset': '06:00 PM'}"
        return http_get(self.WEATHER_API_SUNRISE, False)["forecast"]["forecastday"][0][
            "astro"
        ]
