from fastapi import FastAPI, Request, Body
from datetime import datetime

from db.database import engine
from db.models import RequestLog

from typing import Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from utils.weather_api_utils import get_weather_by_date


app = FastAPI()


@app.get("/weather/{str_date}")
async def get_weather(str_date):
    try:
        is_valid = datetime.strptime(str_date, "%Y-%m-%d")
    except ValueError:
        is_valid = False

    if is_valid:
        service_response = await get_weather_by_date(str_date)
        base_response = service_response["days"][0]

        return base_response
    else:
        return {
                "status": "Not OK",
                "error": "Value Error"
            }


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
