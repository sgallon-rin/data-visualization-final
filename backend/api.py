#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/6/4 10:50
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : api.py
# @Description : api
# to run:
# $ uvicorn api:app --reload

from datetime import datetime
from dateutil import parser
from typing import Optional
from fastapi import FastAPI
from logger_utils import logger
from mongo_utils.mongo_client_utils import read_with_condition_from
from config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}


@app.get("/api/pollution_data_daily")
async def read_pollution_data_daily(date: str = "20130101", lat: Optional[float] = None, long: Optional[float] = None):
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


@app.get("/api/pollution_data_place")
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
