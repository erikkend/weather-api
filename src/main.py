from fastapi import FastAPI, Request


app = FastAPI()


@app.get("/weather/{date}")
async def get_weather_by_date(date: str, request: Request):
    client_host = request.client.host
    print(request)
    return {"client_host": client_host, "date": date}
