# 落地页分析

## 需求分析

### 爬虫

构建url输入->抓取网页->提取图片url（icon和其他img要做区分）->返回图片url，存储在数据库中待查，记录异常信息

- 多线程
- 生产者-消费者模式

### 前端

可视化界面，能够发送查询请求

能够展示对比不同包名国家落地页的图片

### 数据库

储存包名，国家，地区信息，以及对应的icon和其他图片的url

### 后端

对需要的查询进行封装，将api提供给前端

### 日志系统

用python的模块实现，记录异常信息

## 技术准备

- python -- flask
- vue3 + ts + eleme
- mysql

## 详细设计

### 数据库表设计

### 任务列表

tasks

| 字段         | 类型         | 约束/默认值                | 允许为空 | 描述                                            |
| ------------ | ------------ | -------------------------- | -------- | ----------------------------------------------- |
| id           | INT          | PRIMARY KEY, AUTO_INC      | 否       |                                                 |
| package_name | VARCHAR(255) | INDEX                      | 否       |                                                 |
| platform     | ENUM         | 'google_play', 'app_store' | 否       |                                                 |
| region       | VARCHAR(10)  | INDEX                      | 否       |                                                 |
| language     | VARCHAR(10)  | INDEX                      | 否       |                                                 |
| status       | VARCHAR(20)  | DEFAULT 'pending'          | 否       | 状态: `pending`, `running`, `success`, `failed` |
| erro_log     | TEXT         |                            | 否       |                                                 |
| create_at    | DATETIME     | DEFAULT NOW()              | 否       |                                                 |
| update_at    | DATETIME     | DEFAULT NOW()              | 否       |                                                 |

### 图片资源列表

Images

| 字段       | 类型 | 约束/默认值           | 允许为空 | 描述         |
| ---------- | ---- | --------------------- | -------- | ------------ |
| id         | INT  | PRIMARY KEY, AUTO_INC | 否       |              |
| task_id    | INT  | FOREIGN KEY           | 否       | 关联tasks.id |
| Image_type | ENUM | 'icon', 'other'       | 否       |              |
| url        | TEXT |                       | 否       | 图片链接     |

## 请求逻辑

1. 前端发起单条请求，通常是发送包名，语言，地区，后端检查数据库中是否存在任务，如果存在成功的任务则直接返回图片列表

2. 多条请求，



## 文件划分

- `crawler_engine.py` : 创建线程池，根据传入参数，爬取数据
- `db_manager` : 仅负责对数据库的增删改查
- `api_server` : 负责管理接口
- `task_service` : 负责处理业务，包括数据加工处理等
- `page_parser` : 解析抓取到的html文件，提取图片链接