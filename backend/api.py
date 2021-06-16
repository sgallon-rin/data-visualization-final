#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/6/4 10:50
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : api.py
# @Description : api
# to run:
# $ uvicorn api:app --reload

import uvicorn
from datetime import datetime
from dateutil import parser
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logger_utils import logger
from mongo_utils.mongo_client_utils import read_with_condition_from
from config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME

app = FastAPI()

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:8080",
    "https://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}


@app.get("/api/pollution_data/daily")
async def read_pollution_data_daily(date: str = "2013-01-01", lat: Optional[float] = None,
                                    long: Optional[float] = None):
    query_dict = dict()
    if lat and long:
        query_dict["lat"] = lat
        query_dict["long"] = long
    query_dict["date"] = parser.parse(date)
    # print(query_dict)
    records = read_with_condition_from(MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME,
                                       query_dict=query_dict, projection_dict={"_id": 0})
    # return {"result_len": len(records)}
    # print(records)
    return {"result_len": len(records), "result": records}


@app.get("/api/pollution_data/place")
async def read_pollution_data_place(lat: float, long: float, startdate: Optional[str] = None,
                                    enddate: Optional[str] = None):
    query_dict = dict()
    query_dict["lat"] = lat
    query_dict["long"] = long
    if startdate and enddate:
        startdate = parser.parse(startdate)
        enddate = parser.parse(enddate)
        query_dict["date"] = {"$gte": startdate, "$lte": enddate}
    records = read_with_condition_from(MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME,
                                       query_dict=query_dict, projection_dict={"_id": 0})
    return {"result_len": len(records), "result": records}


@app.get("/api/pollution_data/place/year_interval")
async def read_pollution_data_place(lat: float, long: float, startyear: str, endyear: str):
    query_dict = dict()
    query_dict["lat"] = lat
    query_dict["long"] = long
    if startyear and endyear:
        startdate = parser.parse(startyear + "-01-01")
        enddate = parser.parse(endyear + "-12-31")
        query_dict["date"] = {"$gte": startdate, "$lte": enddate}
    records = read_with_condition_from(MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME,
                                       query_dict=query_dict, projection_dict={"_id": 0})
    return {"result_len": len(records), "result": records}


@app.get("/test_api")
async def read_test_api():
    return {"time": {"updated": "Jun 7, 2021 08:54:00 UTC", "updatedISO": "2021-06-07T08:54:00+00:00",
                     "updateduk": "Jun 7, 2021 at 09:54 BST"},
            "disclaimer": "This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data "
                          "converted using hourly conversion rate from openexchangerates.org",
            "chartName": "Bitcoin",
            "bpi": {
                "USD": {"code": "USD", "symbol": "&#36;", "rate": "36,129.2477", "description": "United States Dollar",
                        "rate_float": 36129.2477},
                "GBP": {"code": "GBP", "symbol": "&pound;", "rate": "25,560.5756",
                        "description": "British Pound Sterling",
                        "rate_float": 25560.5756},
                "EUR": {"code": "EUR", "symbol": "&euro;", "rate": "29,692.8584", "description": "Euro",
                        "rate_float": 29692.8584}}}


if __name__ == "__main__":
    uvicorn.run(app='api:app', host="localhost", port=8000, reload=True, debug=True)
