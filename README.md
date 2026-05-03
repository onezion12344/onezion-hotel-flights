# 🏨 onezion-hotel-flights

> **AI 酒店搜索与比价工具** — 整合 4 个数据源，一句话找到最合适的酒店。

通过自然语言与 AI 助手对话，即可完成从搜索、比价到预订的全流程。支持国内酒店（按地铁站/景点/区域搜索）和海外酒店搜索，所有价格实时更新。

---

## ✨ 核心功能

| 功能 | 描述 |
|------|------|
| 🗣️ **自然语言搜索** | 用日常语言描述需求，AI 自动理解意图并搜索 |
| 🔍 **多源比价** | 同时查询多个数据源，交叉验证价格和可用性 |
| 📍 **地理位置搜索** | 支持按地铁站、景点、商圈、地址搜索 |
| ⭐ **智能筛选** | 按星级、价格范围、设施条件自动过滤 |
| 📏 **距离计算** | 搜索结果包含距搜索地点的距离信息 |
| 🔗 **一键预订** | 通过 Jinko 生成支付链接，直接完成预订 |

### 数据源概览

| 数据源 | 覆盖范围 | 实时价格 | 可预订 | 定位能力 |
|--------|----------|:--------:|:------:|:--------:|
| **AIGoHotel** | 🇨🇳 国内酒店（最全） | ✅ | ❌ | ✅ 地铁站/景点/地址 |
| **Jinko** | 🌍 全球 200万+ 酒店 | ✅ | ✅ | ✅ |
| **Booking.com** | 🌍 海外酒店 | ✅ | ❌ | ✅ |
| **高德地图** | 🇨🇳 国内 POI | ❌ | ❌ | ✅ 景点/地铁坐标 |

---

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户输入                              │
│    "深圳龙岗宝龙地铁站附近四星酒店，明天一晚"              │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│               onezion-hotel-flights Skill                │
│                                                         │
│    ┌─────────────┐  ┌─────────────┐  ┌───────────────┐  │
│    │ 意图理解模块 │  │ 数据源路由  │  │ 结果聚合模块  │  │
│    │ - 提取地点  │→ │ - 优先级选择│→ │ - 价格排序    │  │
│    │ - 日期解析  │  │ - 并行查询  │  │ - 距离标记    │  │
│    │ - 星级筛选  │  │ - 错误降级  │  │ - 推荐输出    │  │
│    └─────────────┘  └──────┬──────┘  └───────────────┘  │
└────────────────────────────┼─────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐   ┌──────────────┐   ┌─────────────────┐
│  AIGoHotel    │   │    Jinko     │   │  Booking.com    │
│  MCP Server   │   │  MCP Server  │   │   MCP Server    │
│ (HTTP/远程)   │   │ (npx/本地)   │   │ (Python/本地)   │
├───────────────┤   ├──────────────┤   ├─────────────────┤
│ • 国内酒店最全│   │ • 全球覆盖   │   │ • 海外酒店最全  │
│ • 地铁站搜索  │   │ • 可预订支付 │   │ • 通过RapidAPI │
│ • 实时价格    │   │ • 200万+     │   │ • 住宿评论      │
└───────┬───────┘   └──────┬───────┘   └────────┬────────┘
        │                  │                    │
        └──────────────────┼────────────────────┘
                           ▼
                ┌──────────────────┐
                │  高德地图 API    │
                │  (POI 辅助定位)  │
                ├──────────────────┤
                │ • 景点坐标       │
                │ • 地铁站定位     │
                │ • 地理编码       │
                └──────────────────┘
```

### 数据源选择逻辑

| 场景 | 首选 | 备选 | 说明 |
|------|------|------|------|
| 国内酒店搜索 | **AIGoHotel** | Jinko | AIGoHotel 国内覆盖最全 |
| 国内酒店预订 | **Jinko** | — | 唯一支持在线支付的渠道 |
| 海外酒店搜索 | **Booking.com** | Jinko | Booking 海外房源最丰富 |
| 海外酒店预订 | **Jinko** | — | 支持全球酒店预订 |
| 地标/地铁定位 | **高德地图** | — | 辅助获取精确坐标 |
| 实时比价 | **AIGoHotel** | Jinko | 两个渠道相互验证 |

---

## 📦 安装指南

### 前置要求

- **Python 3.8+**（运行搜索脚本）
- **Node.js 16+**（运行 Jinko MCP）
- **WorkBuddy** 或支持 MCP 的客户端（Cursor、Claude Desktop 等）

### 安装步骤

```bash
# 1. 克隆项目（如果还没有）
# 项目已安装在 WorkBuddy Skills 目录中：
ls ~/.workbuddy/skills/onezion-hotel-flights/

# 2. 安装 AIGoHotel MCP
pip install aigohotel-mcp

# 3. 安装 Jinko MCP
npx jinko-mcp-dev@latest

# 4. 复制环境变量配置
cp .env.example .env
```

### 环境变量配置

编辑 `.env` 文件，填入你的 API Key：

```bash
# 必填（至少一个）
AIGOHOTEL_API_KEY=your_aigohotel_key
JINKO_API_KEY=your_jinko_key
RAPIDAPI_KEY=your_rapidapi_key
AMAP_API_KEY=your_amap_key
```

> 💡 **提示**：AIGoHotel 国内酒店效果最佳，建议优先申请。获取 API Key 后只需一个环境变量即可开始使用。

---

## 🚀 使用方法

### 方式一：自然语言对话（推荐）

直接对 AI 助手说出需求，无需记命令：

**搜索酒店**
> "帮我搜深圳龙岗宝龙地铁站附近的四星酒店，明天住一晚"

**按景点搜索**
> "上海迪士尼附近3公里内，价格500以下的酒店"

**指定日期**
> "北京故宫附近，5月5日入住，住两晚"

**海外酒店**
> "东京新宿附近评分8分以上的酒店，5月10日入住"

### 方式二：命令行脚本

```bash
cd ~/.workbuddy/skills/onezion-hotel-flights/scripts

# 基本用法
python search_hotels.py "深圳龙岗宝龙地铁站"

# 指定入住日期和星级
python search_hotels.py "深圳龙岗宝龙地铁站" 2026-05-04 1 4 5
```

### 方式三：MCP 配置

在支持 MCP 的客户端中，配置以下 JSON：

```json
{
  "mcpServers": {
    "aigohotel-mcp": {
      "url": "https://mcp.aigohotel.com/mcp",
      "type": "http",
      "headers": {
        "Authorization": "Bearer ${AIGOHOTEL_API_KEY}"
      }
    },
    "jinko-mcp": {
      "command": "npx",
      "args": ["jinko-mcp-dev@latest"]
    }
  }
}
```

---

## 🔑 数据源申请指南

### AIGoHotel API_KEY

| 项目 | 内容 |
|------|------|
| 申请链接 | https://mcp.agentichotel.cn/apply |
| 提供商 | 深圳道旅科技（国家级高新技术企业） |
| 覆盖 | 国内酒店最全，支持地铁站/景点搜索 |
| 费用 | 申请审核制 |

**应用场景描述模板**：

> 我是一名香港大学（HKU）的人工智能方向学生，正在开发集成 AI Agent 的个人助手系统（基于 WorkBuddy 平台）。我需要接入 AIGoHotel 的酒店搜索 MCP 服务，以实现以下功能：
>
> 1. **自然语言酒店搜索**：通过 AI 助手以自然语言描述需求（如"深圳龙岗宝龙地铁站附近四星酒店，明天一晚"），实时获取符合条件的酒店列表和价格
> 2. **多源比价**：将 AIGoHotel 的搜索结果与其他数据源（高德地图 POI、Booking.com 等）进行交叉验证，为用户提供最优选择
> 3. **出行规划自动化**：结合 AI Agent 的其他能力（日历管理、行程规划），为用户提供端到端的出行体验
>
> 主要用户群体为个人用户和平时的社交圈内分享。使用场景是非商业的个人效率提升工具。

> 📌 **使用证明**：本项目开源在 GitHub，提供完整的 Skill 文档和 MCP 配置模板。

### Jinko API_KEY

| 项目 | 内容 |
|------|------|
| 申请链接 | https://www.jinko.so/ |
| 覆盖 | 全球 200万+ 酒店 |
| 特点 | 支持搜索 + 预订 + 支付 |
| 费用 | 开发版免费，生产需申请 |

### Booking.com (RapidAPI)

| 项目 | 内容 |
|------|------|
| 申请链接 | https://rapidapi.com/apidojo/api/booking-com/ |
| 覆盖 | 全球酒店，海外房源最全 |
| 接入方式 | 通过 RapidAPI Hub |
| 费用 | 免费套餐可用 |

### 高德地图 API

| 项目 | 内容 |
|------|------|
| 申请链接 | https://lbs.amap.com/ |
| 功能 | POI 搜索、地理编码 |
| 免费配额 | 通用 5000 次/天，POI 搜索 100 次/天 |
| 用途 | 辅助定位景点/地铁站坐标 |

---

## 📋 数据源对比

| 维度 | AIGoHotel | Jinko | Booking.com | 高德地图 |
|------|:---------:|:-----:|:-----------:|:--------:|
| **国内覆盖** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **海外覆盖** | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| **实时价格** | ✅ | ✅ | ✅ | ❌ |
| **可预订** | ❌ | ✅ | ❌ | ❌ |
| **地铁站搜索** | ✅ | ❌ | ❌ | ✅ |
| **景点搜索** | ✅ | ✅ | ✅ | ✅ |
| **POI 定位** | — | — | — | ✅ |
| **响应速度** | 快 | 中 | 中 | 快 |
| **安装方式** | pip | npx | Python 脚本 | REST API |
| **免费额度** | 审核制 | 开发免费 | 免费套餐 | 5000次/天 |

---

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| **Python 3** | 搜索脚本、MCP 本地服务 |
| **Node.js** | Jinko MCP 运行环境 |
| **MCP 协议** | 标准化 AI 工具接口 |
| **AIGoHotel MCP** | 国内酒店搜索数据源 |
| **Jinko MCP** | 全球酒店搜索与预订 |
| **RapidAPI** | Booking.com 数据接入 |
| **高德地图 API** | POI 辅助定位 |

### 文件结构

```
onezion-hotel-flights/
├── README.md               # 📖 本文件
├── SKILL.md                # ⚙️ Skill 定义与文档
├── .env.example            # 🔐 环境变量模板
├── .gitignore              # 🙈 Git 忽略规则
├── scripts/
│   ├── search_hotels.py    # 🔍 统一搜索脚本
│   └── setup.py            # 🔧 初始化脚本
├── mcp-servers/
│   ├── aigohotel.json      # 🏨 AIGoHotel MCP 配置
│   ├── jinko.json          # 🌍 Jinko MCP 配置
│   └── booking.json        # 🏖️ Booking.com MCP 配置
└── references/
    ├── api-docs.md         # 📚 API 文档参考
    └── aigohotel-application.md  # 📝 申请材料模板
```

---

## 📄 许可证

本项目基于 **MIT 许可证** 开源。

```
MIT License

Copyright (c) 2026 onezion

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...

[完整内容见 LICENSE 文件]
```

---

<p align="center">
  <sub>Built with ❤️ by onezion · Powered by MCP · 让旅行规划更简单</sub>
</p>
