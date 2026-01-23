<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=blur&height=300&color=gradient&text=land%20page%20analysis&textBg=false&animation=fadeIn&fontColor=3271ff" />

  <h1>App Landing Page Analyzer</h1>

  <p align="center">
    <strong>一款移动应用商店资源分析工具，助力市场运营一键解析竞品落地页素材与不同国家地区本地化策略。</strong>
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" />
    <img src="https://img.shields.io/badge/Element_Plus-latest-409EFF?style=for-the-badge&logo=element-plus&logoColor=white" />
    <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  </p>

  <p align="center">
    <a href="#-快速开始">快速开始</a> •
    <a href="#-核心特性">核心特性</a> •
    <a href="#-架构设计">架构设计</a> •
    <a href="./tutorials/README.md">深度教程</a>
  </p>
</div>

---

## 核心特性

<table width="100%">
  <tr>
    <td width="50%" style="border: none; vertical-align: top;">
      <h3>全球化商店适配</h3>
      <p>内置 <strong>Region-Language</strong> 联动引擎，支持一键切换国家代码与语言偏好，深度捕获不同文化背景下的本地化商店素材，助力全球市场调研。</p>
    </td>
    <td width="50%" style="border: none; vertical-align: top;">
      <h3>实时同步解析</h3>
      <p>采用<strong>双重请求架构</strong>：后端实时抓取配合数据库 7 天有效期校验。在保证素材新鲜度的同时，实现秒级响应，告别漫长的异步任务等待。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" style="border: none; vertical-align: top;">
      <h3>高保真链接清洗</h3>
      <p>针对 Google Play 复杂的 <code>srcset</code> 逻辑，系统自动剥离 <code>2x</code>、<code>512w</code> 等冗余描述符，直取 <strong>HD 原图链接</strong>，确保存储的每张素材均为最高清晰度。</p>
    </td>
    <td width="50%" style="border: none; vertical-align: top;">
      <h3>多维可视化对比</h3>
      <p>基于 Vue3 构建 <strong>Icon-to-Screen</strong> 画廊。支持多包名、多地区的横向排版对比，让应用图标与截图的视觉差异一目了然，提升分析效率。</p>
    </td>
  </tr>
</table>

---

## 架构设计

本项目采用前后端分离的**生产级架构**，确保了高并发场景下的稳定性。

```mermaid
graph LR
    A[Vue3 Frontend] -- REST API --> B[Flask Server]
    B -- Query/Check --> C[(MySQL DB)]
    B -- Execute Task --> D[Crawler Engine]
    D -- Parse --> E[Google/Apple Store]
    E -- Result --> D
    D -- Persist --> C
```

## 快速开始

---

<div align="center"> <p>如果您觉得这个项目有帮助，请给一个 ⭐️</p> <p>© 2026 Ivory Gate. Built with ❤️ for Marketing.</p> </div>