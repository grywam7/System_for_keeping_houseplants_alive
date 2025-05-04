from microdot_asyncio import Microdot, Response

app = Microdot()
app.run(port=80)
Response.default_content_type = "text/html"


@app.get("/")
async def index(request):
    open("index.html", "rb").read()
    return Response(open("index.html", "rb").read())


@app.post("/new_plant")
async def new_plant(request):
    open("new_plant.html", "rb").read()
    return Response(open("new_plant.html", "rb").read())


@app.post("/flowering")
async def flowering(request):
    open("flowering.html", "rb").read()
    return Response(open("flowering.html", "rb").read())


@app.post("/fruiting")
async def fruiting(request):
    open("fruiting.html", "rb").read()
    return Response(open("fruiting.html", "rb").read())


@app.post("/plant_params")
async def plant_params(request):
    open("plant_params.html", "rb").read()
    return Response(open("plant_params.html", "rb").read())


@app.post("/delete_plant")
async def delete_plant(request):
    open("delete_plant.html", "rb").read()
    return Response(open("delete_plant.html", "rb").read())


@app.route("/favicon.ico")
async def favicon(request):
    open("favicon.ico", "rb").read()
    return Response(open("favicon.ico", "rb").read())


@app.get("/plants")
async def get_plants(request):
    # Assuming you have a function to get all plants
    plants = await plant_repo.load_all()
    return Response(
        ujson.dumps([plant.to_dict() for plant in plants]),
        content_type="application/json",
    )


@app.get("/plants/<pid>")
async def get_plant(request, pid):
    # Assuming you have a function to get a plant by ID
    plant = await plant_repo.get_by_id(pid)
    if plant:
        return Response(ujson.dumps(plant.to_dict()), content_type="application/json")
    else:
        return Response("Plant not found", status=404)


@app.post("/plants/<pid>", methods=["PUT"])
async def update(request, pid):
    # Assuming you have a function to update a plant by ID
    data = await request.json()
    plant = await plant_repo.update(pid, data)
    if plant:
        return Response(ujson.dumps(plant.to_dict()), content_type="application/json")
    else:
        return Response("Plant not found", status=404)
