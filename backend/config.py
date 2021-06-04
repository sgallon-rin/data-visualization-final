#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/5/27 11:15
# @Author      : sgallon
# @Email       : shcmsgallon@outlook.com
# @File        : config.py
# @Description :

import os

# HOME = r"home/jupyter/sjl/data-visualization-final"
HOME = r"/Users/sgallon/Documents/Docus/kjzl/5B/数据可视化 Data Visualization/data-visualization-final/"
DATA_ROOT = os.path.join(HOME, "data", "ChinaVis2021大气污染再分析数据集")

MONGO_URI = r"mongodb://localhost:27017/"
MONGO_DB_NAME = "sjl"
MONGO_COLLECTION_NAME = "pollution_sharded"
