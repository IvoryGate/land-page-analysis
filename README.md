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
| platform     | VARCHAR(20)  | 'google_play', 'app_store' | 否       |                                                 |
| region       | VARCHAR(10)  | INDEX                      | 否       |                                                 |
| language     | VARCHAR(10)  | INDEX                      | 否       |                                                 |
| status       | VARCHAR(20)  | DEFAULT 'pending'          | 否       | 状态: `pending`, `running`, `success`, `failed` |
| erro_log     | TEXT         |                            | 否       |                                                 |
| create_at    | DATETIME     | DEFAULT NOW()              | 否       |                                                 |
| update_at    | DATETIME     | DEFAULT NOW()              | 否       |                                                 |

### 图片资源列表

Images

| 字段       | 类型        | 约束/默认值           | 允许为空 | 描述         |
| ---------- | ----------- | --------------------- | -------- | ------------ |
| id         | INT         | PRIMARY KEY, AUTO_INC | 否       |              |
| task_id    | INT         | FOREIGN KEY           | 否       | 关联tasks.id |
| Image_type | VARCHAR(20) | 'icon', 'other'       | 否       |              |
| url        | TEXT        |                       | 否       | 图片链接     |