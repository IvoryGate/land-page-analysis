# Landing Page Analysis 接口文档

本项目后端基于 Flask 开发，提供应用商店（Google Play/App Store）落地页数据的抓取与管理功能。

## 基础信息
- **Base URL**: `http://127.0.0.1:5050/api`
- **Content-Type**: `application/json`
- **CORS**: 已启用（允许跨域访问）

## 接口详情

### 1. 创建/触发抓取任务
提交应用包名，系统将检查缓存或启动爬虫引擎抓取图片。

- **URL**: `/crawl`
- **Method**: `POST`
- **请求参数**:

| 参数名 | 类型 | 必选 | 说明 | 示例 |
| :--- | :--- | :--- | :--- | :--- |
| `package` | String | 是 | 应用包名或 ID | `com.whatsapp` |
| `platform` | String | 是 | 平台类型 | `android` 或 `ios` |
| `region` | String | 否 | 地区代码 (默认 `us`) | `cn`, `jp`, `us` |
| `lang` | String | 否 | 语言代码 (默认 `en`) | `zh`, `en` |

- **请求体示例**:
```json
{
    "package": "com.whatsapp",
    "platform": "android",
    "region": "us"
}