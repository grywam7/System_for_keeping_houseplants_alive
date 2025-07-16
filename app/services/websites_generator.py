from services.json_db import Log
import utime

# from services.json_db import PlantTypeRepo
from models.plant import Plant


def generate_plants_cards(plants: list) -> str:
    html_header = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Plant Cards</title>
  <style>
    .card-container {
      display: flex;
      flex-wrap: wrap;
      gap: 1em;
    }
    table {
      margin: 1em;
    }
    table, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
  </style>
</head>
<body>
<h1>Plant Cards</h1>
<div class="card-container">
"""
    html_footer = """
</div>
</body>
</html>
"""
    body = ""
    for plant in plants:
        info = plant.to_dict()
        card = '<div class="card"><table>'
        for key, value in info.items():
            card += f"<tr><td>{key}</td><td><strong>{value}</strong></td></tr>"
        card += "</table>"
        body += card

    return html_header + body + html_footer


# def generate_plant_site(plant: Plant) -> str:
# TODO: implement this function
# This function should generate a detailed HTML page for a single plant
# using the plant's data.


def generate_logs_site() -> str:
    html_header = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Log reports</title>
  <style>
    table {
      margin: 1em;
    }
    table, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
  </style>
</head>
<body>
<h1>Log Reports</h1>
<table>
    <th>
        <td>Time Stamp</td>
        <td>Name</td>
        <td>Message</td>
        <td>Additional Info</td>
    </th>
"""
    html_footer = """
</table>
</body>
</html>
"""
    body = ""
    for log in Log.load_all():
        body += f"""<tr>
    <td>{log.timestamp}</td>
    <td>{log.name}</td>
    <td>{log.message}</td>
    <td>{log.info}</td>
</tr>"""

    return html_header + body + html_footer


def _make_svg_line(vals, w=150, h=50, color="#2a6"):
    """Return an inline-SVG string representing vals (list of int)."""
    if not vals:
        return "<svg width=%d height=%d></svg>" % (w, h)
    vmin, vmax = min(vals), max(vals)
    rng = (vmax - vmin) or 1
    step_x = w / (len(vals) - 1 or 1)
    # map every value to 'x,y'
    pts = [
        "%.1f,%.1f" % (i * step_x, h - (v - vmin) * h / rng) for i, v in enumerate(vals)
    ]
    path = "M" + " L".join(pts)
    return (
        '<svg width="%d" height="%d" viewBox="0 0 %d %d">'
        '<polyline fill="none" stroke="%s" stroke-width="1" points="%s"/></svg>'
    ) % (w, h, w, h, color, " ".join(pts))


def _median(values: list[int]) -> int | None:
    """
    Return the median of a list of integers, or None if empty.
    Uses integer division for even-length lists.
    """
    if not values:
        return None
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2:
        return s[mid]
    # even count: average the two middle values
    return (s[mid - 1] + s[mid]) // 2


def _median_gap(history):
    """Return median gap (days) between consecutive events in list of {"start","end"}."""
    dates = [h["start"] for h in history]
    if len(dates) < 2:
        return None
    gaps = []
    for a, b in zip(dates, dates[1:]):
        t_a = utime.mktime(
            a
            + (
                0,
                0,
                0,
                0,
            )
        )  # make tuple 8-elements for mktime
        t_b = utime.mktime(
            b
            + (
                0,
                0,
                0,
                0,
            )
        )
        gaps.append((t_b - t_a) // 86400)
    return _median(gaps)


def _dt_tuple_to_str(dt: tuple) -> str:
    """
    Convert an 8-tuple from utime.localtime() into 'YYYY-MM-DD' string.
    """
    year, month, day = dt[0], dt[1], dt[2]
    return f"{year:04d}-{month:02d}-{day:02d}"


def _predict_next(history):
    if not history:
        return "n/a"
    med = _median_gap(history)
    if med is None:
        return "n/a"
    last = history[-1]["end"] or utime.localtime()[:3]
    t_last = utime.mktime(
        last
        + (
            0,
            0,
            0,
            0,
        )
    )
    return _dt_tuple_to_str(utime.localtime(t_last + med * 86400))


def generate_plant_page(plant):
    d = plant.to_dict()
    svg = _make_svg_line(d["moisture_history"] or [])
    flower_next = _predict_next(d["flowering_history"] or [])
    fruit_next = _predict_next(d["fruiting_history"] or [])

    head = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{font-family:sans-serif} td{border:1px solid #666;padding:2px 6px}
table{border-collapse:collapse;margin-bottom:1em;font-size:.9em}
a.btn{display:inline-block;padding:2px 6px;background:#48f;color:#fff;text-decoration:none;font-size:.8em}</style>
</head><body>"""
    foot = "</body></html>"

    rows = "".join(
        f"<tr><td>{k}</td><td>{v}</td></tr>"
        for k, v in d.items()
        if k not in ("moisture_history", "fruiting_history", "flowering_history")
    )
    controls = (
        f'<a class="btn" href="/flowering?pot_index={d["pot_index"]}">set flowering</a> '
        f'<a class="btn" href="/fruiting?pot_index={d["pot_index"]}">set fruiting</a> '
        f'<a class="btn" href="/delete_plant?pot_index={d["pot_index"]}">delete</a>'
    )

    return (
        head
        + f"<h2>{d['plant_name']}</h2>"
        + controls
        + "<h3>Parameters</h3><table>"
        + rows
        + "</table>"
        "<h3>Moisture history</h3>"
        + svg
        + f"<h3>Next flowering (est.): {flower_next}</h3>"
        f"<h3>Next fruiting (est.): {fruit_next}</h3>" + foot
    )
