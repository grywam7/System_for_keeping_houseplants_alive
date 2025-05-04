from services.http_requests import http_get
import machine


class Weather:
    WEATHER_API_HOURLY = "https://www.meteosource.com/api/v1/free/point?lat=50.098011&lon=19.891431&sections=hourly&timezone=CET&language=en&units=auto&key=kqngt51q4u1xid9ys4orkxcofumfllqkthcp3dp0"
    WEATHER_API_SUNRISE = "http://api.weatherapi.com/v1/forecast.json?key=21c1dc7e612f4f448b9131803251104&q=50.098011,19.891431&days=1&aqi=no&alerts=no"

    def __init__(self, sunrise: int, sunset: int, clouds: dict):
        self.sunrise = sunrise
        self.sunset = sunset
        self.clouds = clouds
        self.date = machine.RTC().datetime()[:3]

    def get_weather(self):
        if self.date != machine.RTC().datetime()[:3]:
            self._update_weather()
        return self._clouds, self.sunrise, self.sunset

    def _update_weather(self):
        self.date = machine.RTC().datetime()[:3]
        self.clouds = self._get_clouds_hourly()
        self.sunrise, self.sunset = self._parsed_day_times().values()

    # returns dict containing: {1: 88} // {hour: cloud_cover(0-100)}
    def _get_clouds_hourly(self):
        return {
            hourly_weather["date"][11:13]: hourly_weather["cloud_cover"]["total"]
            for hourly_weather in http_get(self.WEATHER_API_HOURLY, True)["hourly"][
                "data"
            ]
        }

    # returns dict: {sunrise: 6, sunset: 18}
    def _parsed_day_times(self):
        return {
            key: int(value[:2]) + (12 if value[-2:] == "PM" else 0)
            for key, value in self._get_day_times().items()
        }

    # returns dict: {'sunrise': '06:00 AM', 'sunset': '06:00 PM'}
    def _get_day_times(self):
        return http_get(self.WEATHER_API_SUNRISE, False)["forecast"]["forecastday"][0][
            "astro"
        ]
