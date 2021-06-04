# -*- coding: utf-8 -*-
"""
@File       : mongo_client_utils.py
@Author     : Yuka
@Time       : 2021/3/23 14:37
@Version    : 1.0.0
@Description: 
"""
from bson import ObjectId

from logger_utils import logger
from mongo_utils import CLIENT_POOL
import traceback

import pymongo


def get_client(uri):
    if uri not in CLIENT_POOL:
        CLIENT_POOL[uri] = pymongo.MongoClient(uri)
    return CLIENT_POOL[uri]


def read_all_from(uri, db_name, collection_name):
    client = get_client(uri)
    db = client[db_name]
    collection = db[collection_name]
    records = [record for record in collection.find()]
    client.close()
    return records


def read_with_condition_from(uri, db_name, collection_name, query_dict=None, projection_dict=None):
    if query_dict is None:
        query_dict = {}
    client = get_client(uri)
    db = client[db_name]
    collection = db[collection_name]
    records = [record for record in collection.find(query_dict, projection_dict)]
    client.close()
    return records


def get_by_id(id, uri, db_name, collection_name):
    client = get_client(uri)
    db = client[db_name]
    collection = db[collection_name]
    return collection.find_one({"_id": id})


def replace_one_document(record, uri, db_name, collection_name):
    client = get_client(uri)
    db = client[db_name]
    collection = db[collection_name]
    collection.replace_one(filter={"_id": record["_id"]}, replacement=record, upsert=True)


def batch_save_into_collection(records, uri, db_name, collection_name, batch_size=500):
    logger.info("开始向{}中插入数据，总量{}，每批{}...".format(db_name + "." + collection_name, len(records), batch_size))
    client = get_client(uri)
    db = client[db_name]
    collection = db[collection_name]

    buffer = []
    total_success_count = 0
    total_fail_count = 0
    for record in records:
        buffer.append(record)
        if len(buffer) >= batch_size:
            count = len(try_insert(collection, buffer, uri).inserted_ids)
            logger.info("尝试插入数据{}条，成功{}条。".format(len(buffer), count))
            total_success_count += count
            total_fail_count += (batch_size - count)
            buffer.clear()
    if len(buffer) > 0:
        count = len(try_insert(collection, buffer).inserted_ids)
        logger.info("尝试插入数据{}条，成功{}条。".format(len(buffer), count))
        total_success_count += count
        total_fail_count += (len(buffer) - count)
        buffer.clear()

    logger.info("数据写入完毕，总共成功{}条，失败{}条。".format(total_success_count, total_fail_count))


def try_insert(collection, records, exception_uri=None):
    try:
        count = collection.insert_many(records)
        return count
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        logger.warning("数据插入过程中发生异常。正在向数据异常表中写入数据...")
        if exception_uri is not None:
            exception_client = get_client(exception_uri)
            exception_db = exception_client["exception"]
            exception_collection = exception_db[collection.name + "_insert_exception"]
            count = 0
            for record in records:
                if "_id" in record:
                    del record["_id"]
                count += exception_collection.insert(record)
            logger.warning("向异常表中写入数据{}条。".format(count))


def remove_record(id, uri, db_name, collection_name):
    logger.info("删除{}数据，其_id为{}...".format(db_name + "." + collection_name, id))
    client = get_client(uri)
    db = client[db_name]
    collection = db[collection_name]
    collection.delete_one({"_id": id})


def drop_collection(uri, db_name, collection_name):
    logger.info("drop集合{}...".format(db_name + "." + collection_name))
    client = get_client(uri)
    db = client[db_name]
    collection = db[collection_name]
    collection.drop()


def get_between(start_id, until_id, uri, db, collection):
    logger.info("开始读取满足条件{} <= _id < {}的数据...".format(start_id, until_id))
    client = get_client(uri)
    db = client[db]
    collection = db[collection]
    if until_id is None:
        return [document for document in collection.find({"_id": {"$gte": start_id}})]
    return [document for document in collection.find({"_id": {"$gte": start_id, "$lt": until_id}})]


def split_collection(batch, uri, db, collection_name):
    logger.info("开始对{}进行按照id的批次({})划分...".format(db + "." + collection_name, batch))
    client = get_client(uri)
    db = client[db]
    collection = db[collection_name]
    first_document = collection.find_one(sort=[('_id', 1)])
    if first_document is None:
        logger.warn("")
        return []
    start_id = first_document["_id"]
    split_result = []
    count = 0
    while start_id is not None:
        document = collection.find_one(filter={"_id": {"$gte": start_id}},
                                       projection={"_id": 1},
                                       sort=[('_id', 1)],
                                       skip=batch,
                                       limit=1)
        split_result.append({
            "_id": count,
            "start_id": start_id,
            "until_id": document["_id"] if document is not None else None
        })
        start_id = document["_id"] if document is not None else None
        count += 1
    return split_result
