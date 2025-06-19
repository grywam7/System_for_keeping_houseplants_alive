from services.http_requests import http_get
import machine
import ujson


class Weather:
    WEATHER_API = "http://api.open-meteo.com/v1/forecast?latitude=50.098011&longitude=19.891431&daily=sunrise,sunset&hourly=sunshine_duration&forecast_days=1&forecast_hours=24&past_hours=1"

    def __init__(self):
        self.sunrise = None
        self.sunset = None
        self.sunshine = None
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
        return self.sunshine, self.sunrise, self.sunset

    def _default_weather(self) -> tuple[dict[int, int], int, int]:
        "returns default weather data - used when API is unavailable - 0% sunshine"
        return {hour: 0 for hour in range(0, 25)}, 5, 19

    def _update_weather(self):
        data = self._get_weather_from_api()

        times = data["hourly"]["time"]
        sunshine_values = data["hourly"]["sunshine_duration"]

        sunshine = {}
        for date, sushine_time in zip(times, sunshine_values):
            hour = int(date[11:13])
            sunshine[hour] = sushine_time

        self.sunshine = sunshine

        self.sunrise = int(data["daily"]["sunrise"][0][11:13])
        self.sunset = int(data["daily"]["sunset"][0][11:13])

    def _get_weather_from_api(self):
        raw = http_get(self.WEATHER_API)
        sep = "\r\n\r\n"
        idx = raw.find(sep)
        body = raw[idx + len(sep) :] if idx != -1 else raw
        return ujson.loads(body)
