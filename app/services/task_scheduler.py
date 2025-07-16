import machine
import uasyncio
from services.json_db import Log


async def schedule_daily_task(hour: int, minute: int, task, task_args: tuple):
    while True:
        Log.add(
            "task_scheduler",
            "Scheduling task",
            f"task: {task.__name__}, at: {hour}:{minute}, args: {task_args}",
        )
        await uasyncio.sleep(_seconds_until(hour, minute))
        uasyncio.get_event_loop().create_task(task(*task_args))


def _seconds_until(schedule_hour: int, schedule_minute: int) -> int:
    present_hour, present_minute, present_second = machine.RTC().datetime()[4:7]
    present_time_in_seconds = present_hour * 3600 + present_minute * 60
    if present_hour > schedule_hour or (
        present_hour == schedule_hour and present_minute >= schedule_minute
    ):
        # if the scheduled time is in the past, schedule for the next day
        schedule_hour += 24
    Log.add(
        "task_scheduler",
        f"Calculating seconds until next task call:{(schedule_hour * 3600 + schedule_minute * 60) - present_time_in_seconds}",
    )
    return (schedule_hour * 3600 + schedule_minute * 60) - present_time_in_seconds
