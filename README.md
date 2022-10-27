# data-visualization-final
FDU DATA130012 Data Visualization - final project | 数据可视化期末project

I referred to the implementation in https://github.com/reval59/HKUST-VisLab-Coding-Challenge

## Description | 说明
The topic I choose is China pollution/污染物追踪（大气污染数据）, data source:

[ChinaVis 2021数据可视化竞赛](http://chinavis.org/2021/challenge.html)

[2013–2018年中国高分辨率大气污染再分析开放数据集](http://naq.cicidata.top:10443/chinavis/opendata)

The final project contains 4 views, which can be devided into two groups:

1. China Pollution Data of All Places on a Certain Day
   - A colored map of China showing values of the selected variant
   - A table view of the data
   
2. China Pollution Data at a Certain Place in a Certain Date Interval
   - A line plot of the selected variant in the selected interval
   
   - A table view of the data

All of the views are fully interactive, you can select any date/place/variant to show.

Note: As the size of the data is huge (about 13 MB for each day's data, and more than 17 GB in total), I decide not to implement an animated view for a stable performance.

## Technology Stacks | 技术栈
### Frontend | 前端
* D3.js
* lodash.js
* Vue.js
* Vuetify.js

### Backend | 后端
* Python
* FastAPI + uvicorn
* mongoDB
