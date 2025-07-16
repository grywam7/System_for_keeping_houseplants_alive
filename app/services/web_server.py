from microdot import Microdot, Response, send_file, redirect
from services.websites_generator import generate_plants_cards
from services.json_db import PlantRepo
from models.plant import Plant
from present_state import plants, find_plant_by, remove_plant
from services.websites_generator import generate_logs_site, generate_plant_page
from services.json_db import Log
import uasyncio
import ujson

app = Microdot()
Response.default_content_type = "text/html"


# def run_web_server():
#     uasyncio.get_event_loop().create_task(app.start_server(host="0.0.0.0", port=80))
#     print("Web server started")


async def run_web_server():
    Log.add("web_server", "Starting web server")
    await app.start_server(host="0.0.0.0", port=80)


def page(name):
    Log.add("web_server", "Serving page", {"name": name})
    return send_file(f"../public/{name}", max_age=0)  # 0 = no cache when testing


@app.get("/")
async def index(req):
    return page("index.html")


@app.get("/new_plant")
async def new_plant(req):
    return page("new_plant.html")


@app.get("/add_new_plant.json")
async def add_new_plant(req):
    data = {
        "plant_name": req.args.get("fname"),
        "pot_index": int(req.args.get("pot_index")),
        "pump_pin": int(req.args.get("pump_pin")),
        "moisture_sensor_pin": int(req.args.get("moisture_sensor_pin")),
        "light_pins": [int(pin) for pin in req.args.get("light_pins").split(",")],
        "moisture_target": int(req.args.get("water_taget")),
        "planted_on": req.args.get("planted_on"),
    }
    print("add_new_plant", data)
    new_plant = Plant.from_dict(data)
    plants.append(new_plant)
    await PlantRepo().save(new_plant)
    Log.add(
        "add_new_plant",
        "New plant added",
        f"pot_index: {new_plant.pot_index}, plant_name: {new_plant.plant_name}",
    )
    return redirect("/plants")


@app.get("/flowering")
async def flowering(req):
    return page("set_flowering.html")


@app.get("/set_flowering.json")
async def set_flowering(req):
    plant = find_plant_by("pot_index", int(req.args.get("pot_index")))
    if plant is not None:
        plant.set_is_flowering(bool(req.args.get("is_flowering")))
        Log.add(
            "set_flowering",
            "Plant flowering state updated",
            f"pot_index: {plant.pot_index}, is_flowering: {plant.is_flowering}",
        )
        return redirect("/plants")
    else:
        Log.add(
            "set_flowering",
            "Plant not found",
            f"pot_index: {req.args.get('pot_index')}",
        )
        return redirect("/set_flowering?error=Plant_not_found")


@app.get("/fruiting")
async def fruiting(req):
    return page("set_fruiting.html")


@app.get("/set_fruiting.json")
async def set_fruiting(req):
    plant = find_plant_by("pot_index", int(req.args.get("pot_index")))
    if plant is not None:
        plant.set_is_fruiting(bool(req.args.get("is_fruiting")))
        Log.add(
            "set_fruiting",
            "Plant fruiting state updated",
            f"pot_index: {plant.pot_index}, is_fruiting: {plant.is_fruiting}",
        )
    return redirect("/plants")


@app.get("/delete_plant")
async def delete_plant(req):
    return page("delete_plant.html")


@app.get("/delete_plant.json")
async def delete_plant_json(req):
    plant = find_plant_by("pot_index", int(req.args.get("pot_index")))
    if plant is not None:
        remove_plant(plant)
        Log.add(
            "delete_plant",
            "Plant deleted",
            f"pot_index: {plant.pot_index}, plant_name: {plant.plant_name}",
        )
        return redirect("/plants")
    else:
        Log.add(
            "delete_plant",
            "Plant not found",
            f"pot_index: {req.args.get('pot_index')}",
        )
        return redirect("/delete_plant?error=Plant_not_found")


@app.get("/favicon.ico")
async def favicon(req):
    return page("favicon.ico")


@app.get("/plants")
async def get_plants(req):
    html = generate_plants_cards(plants)
    Log.add("web_server", "Plants page generated", f"plants_count: {len(plants)}")
    return Response(html)


@app.get("/plant")  # GET /plant?pot=<pot_index>
async def plant(req):
    pot_q = req.args.get("pot")
    if pot_q is None or not pot_q.isdigit():
        Log.add("web_server", "Bad request for plant", {"pot": pot_q})
        return "<h1>Bad request - give /plant?pot=N</h1>", 400

    plant = find_plant_by("pot_index", int(pot_q))
    if plant is None:
        Log.add("web_server", "Plant not found", {"pot": pot_q})
        return "<h1>Plant not found</h1>", 404
    Log.add("web_server", "Plant page requested", {"pot": pot_q})
    return generate_plant_page(plant)


# @app.post("/plant/<pid>", methods=["PUT"])
# async def update(request, pid):
#     data = await request.json()
#     plant = await PlantRepo.update(pid, data)
#     if plant:
#         return Response(ujson.dumps(plant.to_dict()), content_type="application/json")
#     else:
#         return Response("Plant not found", status=404)


@app.get("/log")
async def get_log(req):
    Log.add("web_server", "Log page requested")
    return Response(generate_logs_site())
