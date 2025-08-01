import machine
import uasyncio
from models.plant import Plant
from services.json_db import Log


async def execute_watering(plant: Plant):
    _update_moisture(plant)
    await _run_water_pump(plant)


def _update_moisture(plant: Plant):
    present_moisture = _read_moisture(plant)
    _update_moisture_history(
        plant,
        present_moisture - plant.last_measured_moisture,
        plant.last_watering_duration,
    )
    plant.last_measured_moisture = present_moisture


def _update_moisture_history(plant, moisture_change, watering_duration):
    plant.moisture_history.append(
        {"moisture_change": moisture_change, "watering_duration": watering_duration}
    )
    if len(plant.moisture_history) > 20:
        plant.moisture_history.pop(0)


def _moisture_difference(plant: Plant) -> int:
    return plant.moisture_target - plant.last_measured_moisture


def _calculate_watering(plant: Plant) -> int:
    xs = plant.moisture_changes()
    ys = plant.watering_durations()

    if len(plant.moisture_history) < 3:
        return len(plant.moisture_history) * 40  # not enough data → fallback

    a, b, c = _polyfit_quadratic(xs, ys)

    if a <= 0:  # parabola opens downwards → something went wrong
        return 0

    diff = _moisture_difference(plant)
    val = a * diff * diff + b * diff + c
    if int(val) > 1000:
        Log.add(
            "watering",
            "Calculated watering duration is too high (more than 1000s), using fallback",
            {"plant": plant.pot_index, "calculated_duration": val},
        )
    return max(0, int(val))


async def _run_water_pump(plant: Plant):
    pump = machine.Pin(plant.pump_pin, machine.Pin.OUT)
    Log.add("watering", "Running water pump", {"plant": plant.pot_index})
    watering_duration = _calculate_watering(plant)
    if watering_duration > 0:
        pump.on()
        await uasyncio.sleep(watering_duration)
        pump.off()
    plant.last_watering_duration = watering_duration
    Log.add(
        "watering",
        "Watering completed",
        {"plant": plant.pot_index, "watering_duration": watering_duration},
    )


def _read_moisture(plant: Plant) -> int:
    return plant.moisture_sensor.read()


### generated by chat, as im not fluent in math


# ---------- 1. very small helper : 3×3 linear solver (Gaussian) ---------
def _solve_3x3(M, b):
    """Gaussian elimination for a 3x3 system  M·x = b  ->  returns (x0,x1,x2)."""
    # forward elimination -------------------------------------------------
    for i in range(3):
        # pivot
        pivot = M[i][i]
        if abs(pivot) < 1e-12:  # almost singular
            raise ZeroDivisionError("Singular matrix in polyfit")
        inv = 1.0 / pivot
        # normalise current row
        for j in range(i, 3):
            M[i][j] *= inv
        b[i] *= inv
        # eliminate below
        for k in range(i + 1, 3):
            factor = M[k][i]
            for j in range(i, 3):
                M[k][j] -= factor * M[i][j]
            b[k] -= factor * b[i]
    # back substitution ---------------------------------------------------
    x2 = b[2]
    x1 = b[1] - M[1][2] * x2
    x0 = b[0] - M[0][1] * x1 - M[0][2] * x2
    return x0, x1, x2


# ---------- 2. quadratic least‑squares fit (a, b, c) --------------------
def _polyfit_quadratic(xs, ys):
    """Return (a, b, c) for y = a·x² + b·x + c  (ordinary least squares)."""
    n = float(len(xs))
    Sx = Sy = Sx2 = Sx3 = Sx4 = Sxy = Sx2y = 0.0
    for x, y in zip(xs, ys):
        Sx += x
        Sy += y
        xx = x * x
        Sx2 += xx
        Sx3 += xx * x
        Sx4 += xx * xx
        Sxy += x * y
        Sx2y += xx * y

    # normal‑equation matrix M and vector b
    M = [
        [n, Sx, Sx2],
        [Sx, Sx2, Sx3],
        [Sx2, Sx3, Sx4],
    ]
    b = [Sy, Sxy, Sx2y]

    c, b_coeff, a = _solve_3x3(M, b)  # note: order after elimination
    return a, b_coeff, c
