#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/6/4 10:12
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : data.py
# @Description : prepare data and save it to mongoDB

import os
import json
import pandas as pd
import datetime
from dateutil import parser
from typing import List
from config import DATA_ROOT, MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME
from logger_utils import logger
from mongo_utils.mongo_client_utils import batch_save_into_collection


class PollutionCsv:
    def __init__(self, filename):
        self.df = self.make_dataframe(filename)
        self.date = self.get_date_from_filename(filename)

    @staticmethod
    def get_date_from_filename(filename: str) -> datetime.datetime:
        # filename like "CN-Reanalysis-daily-2013010100.csv"
        filename_list = filename.split(os.sep)
        filename = filename_list[-1]
        assert filename.endswith(".csv"), "Filename error: {}".format(filename)
        ymd = filename.split("-")[-1].split(".")[0]
        assert ymd.isdigit() and len(ymd) == 10, "Wrong date: {}".format(ymd)
        ymd = ymd[:8]
        return parser.parse(ymd)

    @staticmethod
    def make_dataframe(filename: str) -> pd.DataFrame:
        df = pd.read_csv(filename, encoding="utf-8")
        logger.info("Successfully load csv: {}".format(filename))
        if df.shape[1] > 13:  # 原始数据最后有空列，需要删除
            df.drop(df.columns[13:df.shape[1]], axis=1, inplace=True)
        df.columns = ["pm25", "pm10", "so2", "no2", "co", "o3", "u", "v", "temp", "rh", "psfc", "lat", "long"]
        return df

    def make_records(self) -> List[dict]:
        records = json.loads(self.df.to_json(orient="records"))
        for record in records:
            record["date"] = self.date
        return records


def test():
    f = os.path.join(DATA_ROOT, "201301", "CN-Reanalysis-daily-2013010100.csv")
    p = PollutionCsv(f)
    records = p.make_records()
    batch_save_into_collection(records, MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME)


def main():
    logger.info("Start processing all data from DATA_ROOT: {}".format(DATA_ROOT))
    for directory in sorted(os.listdir(DATA_ROOT)):
        full_directory = os.path.join(DATA_ROOT, directory)
        if directory.startswith(".") or not os.path.isdir(full_directory):
            logger.info("Skipping hidden or non-directory: {}".format(full_directory))
            continue
        else:
            logger.info("Processing directory: {}".format(full_directory))
            for filename in sorted(os.listdir(full_directory)):
                full_filename = os.path.join(full_directory, filename)
                if filename.startswith(".") or not filename.endswith(".csv"):
                    logger.info("Skipping hidden or non-csv file: {}".format(full_filename))
                    continue
                else:
                    logger.info("Processing file : {}".format(full_filename))
                    pollution_csv = PollutionCsv(full_filename)
                    records = pollution_csv.make_records()
                    batch_save_into_collection(records, MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME,
                                               batch_size=2000)
                    logger.info("Done for file: {}".format(full_filename))
            logger.info("Done for directory: {}".format(full_directory))
    logger.info("Done for all data from DATA_ROOT: {}".format(DATA_ROOT))


if __name__ == "__main__":
    main()
