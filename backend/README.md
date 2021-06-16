# data-visualization-final
FDU DATA130012 Data Visualization - final project | 数据可视化期末project

## backend | 后端

### Technology Stacks | 技术栈
* Python
* FastAPI + uvicorn
* mongoDB

### Code description | 代码说明

|  file name    |  description    |
| :----: | :----: |
|   api.py   |  main file, the api to serve frontend   |
|   data.py   |  preprocesses the data and save into mongoDB    |
|   logger_utils.py   |  utils for logging    |
|  mongo_utils/mongo_client_utils.py    |   utils for mongoDB   |
|   config.py   |   config the mongoDB address   |



### Run backend | 启动后端

Customize your mongoDB address in `config.py`, run all the preprocessing stages.

Then, start the server by running

```
$ uvicorn api:app --reload
```
