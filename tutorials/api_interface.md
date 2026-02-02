# Landing Page Analyser API Documentation

> [!NOTE]
>
> 本项目提供了一套完整的 API 接口，用于抓取、对比全球各地区的移动应用 Landing Page 素材，并管理查询历史。

## 📌 基础信息

- **Base URL**: `http://<your-server-ip>:<port>/api`
- **跨域支持**: 已开启 CORS (flask-cors)
- **数据交互格式**: `application/json`
- **流式传输格式**: `application/x-ndjson` (仅限 `/compare` 接口)

## 📂 接口详述

### 1. 查询历史管理

#### 1.1 获取最近查询历史

获取最近 10 条查询过的应用包名。

URL: `/history`

Method: `GET`

响应示例:

```json
[
    "com.instagram.android",
    "com.zhiliaoapp.musically",
    "com.spotify.music"
]
```
#### 1.2 更新/保存查询历史

将新查询的包名存入持久化记录中（后端自动执行去重和排重逻辑）。

URL: `/history`

Method: `POST`

请求体: 

```json
{
    "package": "com.example.app"
}
```
响应: 返回更新后的完整历史数组 200 OK。

### 2. 核心抓取接口

#### 2.1 获取单地区记录 (立即查询) 

抓取并返回指定应用在单一国家/语言下的素材。如果数据库已有有效缓存，则直接返回。

URL: `/get`

Method: `POST`

请求参数: 
| 参数名 | 类型 | 必选 | 描述 | 默认值 |
| :--- | :--- | :--- | :--- | :--- | 
| package | string | 是 | 应用包名 (Bundle ID) | - |
| platform | string | 是 | 平台: google_play 或 apple_store | - |
| region | string | 否 | 国家代码 (ISO 3166-1 alpha-2) | us |
| lang | string | 否 | 语言代码 | en |

 成功响应:

```json
{
  "status": "success",
  "task_id": "8a7b6c5d4e...",
  "region": "us",
  "images": [
    { "type": "icon", "url": "https://..." },
    { "type": "other", "url": "https://..." }
  ]
}
```

#### 2.2 全地区同步对比 (流式接口)

针对指定应用，并发触发全球所有主流地区的抓取任务。该接口采用 **NDJSON (Newline Delimited JSON)** 格式，每完成一个地区即实时推送一条数据。

URL: `/compare`

Method: `POST`

Content-Type: `application/x-ndjson`

请求参数: 

| 参数名 | 类型 | 必选 | 描述 |
| :--- | :--- | :--- | :--- |
| `package` | string | 是   | 应用包名 |
| `platform` | string | 是 | 平台类型 |

流式响应示例 (逐行返回):

```json
{"status": "success", "task_id": 1, "region": "cn", "images": [...]}
{"status": "success", "task_id": 2, "region": "jp", "images": [...]}
```

## 🛠 错误处理

接口统一使用 HTTP 状态码表示请求结果：

- **200**: 请求成功。
- **400**: 参数缺失。请检查 `package` 或 `platform` 字段。
- **500**: 服务器内部错误。通常是爬虫引擎超时或数据库写入异常。

## 💡 注意事项

1. **缓存机制**: 后端 `TaskService` 会优先检索数据库，若素材在有效期内，抓取任务会瞬间完成。
2. **前端解析**: 处理 `/compare` 接口时，建议使用 `fetch` 的 `reader.read()` 逐行解析，以实现 UI 上的瀑布流加载效果。
3. **数据持久化**: 后端 `search_history.json` 自动处理持久化，无需手动初始化文件。