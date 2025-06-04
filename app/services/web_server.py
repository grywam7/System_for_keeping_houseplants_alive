from microdot import Microdot, Response, send_file, redirect
from services.websites_generator import generate_plants_cards
from services.json_db import PlantRepo
from models.plant import Plant
from present_state import plants, find_plant_by, remove_plant
from services.websites_generator import generate_logs_site
import network
import uasyncio
import ujson

app = Microdot()
Response.default_content_type = "text/html"


def run_web_server():
    uasyncio.create_task(app.start_server(host="0.0.0.0", port=80))
    uasyncio.get_event_loop().run_forever()


def page(name):
    return send_file(f"../public/{name}", max_age=0)  # 0 = no cache when testing


@app.get("/")
async def index(req):
    print("index")
    print(req)
    return page("index.html")


@app.get("/new_plant")
async def new_plant(req):
    return page("new_plant.html")


@app.get("/add_new_plant.json")
async def add_new_plant(req):
    print("add_new_plant", req)
    p = req.args
    data = {
        "plant_name": p.get("fname"),
        "pot_index": int(p.get("pot_index")),
        "pump_pin": int(p.get("pump_pin")),
        "moisture_sensor_pin": int(p.get("moisture_sensor_pin")),
        "moisture_target": int(p.get("water_taget")),
        "planted_on": p.get("planted_on"),
    }
    print("add_new_plant", data)
    new_plant = Plant.from_dict(data)
    plants.append(new_plant)
    await PlantRepo().save(new_plant)
    return redirect("/plants")


@app.get("/flowering")
async def flowering(req):
    return page("set_flowering.html")


@app.get("/set_flowering.json")
async def set_flowering(req):
    print("set_flowering", req)
    p = req.args
    plant = find_plant_by("pot_index", int(p.get("pot_index")))
    if plant is not None:
        plant.set_is_flowering(bool(p.get("is_flowering")))
    # TO DO komunikat, żę się nie udało
    return redirect("/plants")


@app.get("/fruiting")
async def fruiting(req):
    return page("set_fruiting.html")


@app.get("/set_fruiting.json")
async def set_fruiting(req):
    print("set_fruiting", req)
    p = req.args
    plant = find_plant_by("pot_index", int(p.get("pot_index")))
    if plant is not None:
        plant.set_is_fruiting(bool(p.get("is_fruiting")))
    # TO DO komunikat, żę się nie udało
    return redirect("/plants")


@app.get("/delete_plant")
async def delete_plant(req):
    return page("delete_plant.html")


@app.get("/delete_plant.json")
async def delete_plant_json(req):
    print("set_fruiting", req)
    p = req.args
    plant = find_plant_by("pot_index", int(p.get("pot_index")))
    if plant is not None:
        remove_plant(plant)
    # TO DO komunikat, żę się nie udało
    return redirect("/plants")


@app.get("/favicon.ico")
async def favicon(req):
    return page("favicon.ico")


@app.get("/plants")
async def get_plants(req):
    plants = await PlantRepo().load_all()
    html = generate_plants_cards(plants)
    print(html)
    return Response(html)


# @app.get("/plant/<pid>")
# async def get_plant(request, pid):
#     plant = await PlantRepo.get_by_id(pid)
#     if plant:
#         return Response(ujson.dumps(plant.to_dict()), content_type="application/json")
#     else:
#         return Response("Plant not found", status=404)


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
    generate_logs_site()