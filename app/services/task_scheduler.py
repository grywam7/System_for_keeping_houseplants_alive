import machine
import uasyncio


async def schedule_daily_task(hour: int, minute: int, task, task_args: tuple):
    while True:
        print("scheduling task: {} at {}:{}".format(task, hour, minute))
        await uasyncio.sleep(_seconds_until(hour, minute))
        uasyncio.get_event_loop().create_task(task(*task_args))


def _seconds_until(schedule_hour: int, schedule_minute: int) -> int:
    present_hour, present_minute, present_second = machine.RTC().datetime()[4:7]
    present_time_in_seconds = present_hour * 3600 + present_minute * 60 + present_second
    print(
        "scheduling taskt to run in {} seconds".format(
            (schedule_hour * 3600 + schedule_minute * 60) - present_time_in_seconds
        )
    )
    return (schedule_hour * 3600 + schedule_minute * 60) - present_time_in_seconds
