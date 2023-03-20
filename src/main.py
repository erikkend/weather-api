from fastapi import FastAPI, Request

from db.database import engine
from db.models import RequestLog

from typing import Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from utils.weather_api_utils import get_weather_by_date


app = FastAPI()


@app.get("/weather/{date}")
async def get_weather(date: str):
    service_response = await get_weather_by_date(date)
    base_response = service_response["days"][0]

    return base_response


@app.get("/requests")
async def get_requests(limit: Optional[int] = 100):
    with Session(engine) as session:
        requests = session.query(RequestLog).order_by(desc(RequestLog.date)).limit(limit).all()

        requests_dict = []
        for i in requests:
            requests_dict.append({col.name: getattr(i, col.name) for col in i.__table__.columns})

        return requests_dict


@app.middleware("http")
async def add_request_log(request: Request, call_next):
    remote_addr = request.client.host
    query_string = str(request.url)
    response = await call_next(request)

    if response.status_code == 200:
        try:
            with Session(engine) as session:
                request_log = RequestLog(ip=remote_addr, query=query_string)
                session.add(request_log)
                session.commit()
        except SQLAlchemyError as e:
            print(e)
    return response
