---
name: onezion-hotel-flights
description: "AI 酒店搜索与比价工具，整合4个数据源（AIGoHotel MCP、Jinko MCP、Booking.com MCP、高德地图POI），支持按城市/景点/地铁站搜索实时价格、星级筛选、距离过滤。触发词：酒店搜索、订酒店、酒店比价、hotel search、booking、住宿、酒店推荐。"
triggers:
  - "酒店"
  - "订酒店"
  - "hotel"
  - "booking"
  - "住宿"
  - "比价"
  - "酒店推荐"
  - "酒店搜索"
version: "1.0.0"
author: onezion
---

# onezion-hotel-flights 🏨✈️

AI 酒店搜索与比价工具，整合 4 个数据源，一个 Skill 解决所有酒店搜索需求。

## 架构

```
用户自然语言 → Skill 路由 → 数据源
                        ├── AIGoHotel MCP（国内酒店首选，实时价格）
                        ├── Jinko MCP（全球200万+酒店，可预订）
                        ├── Booking.com MCP（海外酒店，通过RapidAPI）
                        └── 高德地图 API（国内POI搜索，辅助定位）
```

## 数据源详情

### 1. AIGoHotel MCP（国内首选 ⭐⭐⭐⭐⭐）

**状态**：已安装（pip install aigohotel-mcp）

- 深圳道旅科技，国家级高新技术企业
- 国内酒店数据最全，支持按地铁站/景点/地址搜索
- 返回实时价格、星级、设施、距离
- 远程模式：`https://mcp.aigohotel.com/mcp`

**API_KEY 申请**：https://mcp.agentichotel.cn/apply
**环境变量**：`AIGOHOTEL_API_KEY`

### 2. Jinko MCP（全球覆盖 ⭐⭐⭐⭐）

**状态**：已安装（npx jinko-mcp-dev@latest）

- 全球 200万+ 酒店，支持搜索+预订+支付
- 返回支付链接，可直接完成预订
- 生产权限需申请：https://www.jinko.so/

**环境变量**：`JINKO_API_KEY`（生产环境）

### 3. Booking.com MCP（海外 ⭐⭐⭐）

**状态**：已安装（~/wechat-tools/hotels_mcp_server）

- 基于 Booking.com API，通过 RapidAPI 接入
- 海外酒店最全，国内也有覆盖
- 需要 RapidAPI Key

**RapidAPI 申请**：https://rapidapi.com/apidojo/api/booking-com/
**环境变量**：`RAPIDAPI_KEY`

### 4. 高德地图 API（辅助定位 ⭐⭐）

**状态**：纯 REST API，无需安装

- 国内 POI 搜索，用于辅助定位景点/地铁站坐标
- 个人免费配额：通用 5000次/天，POI搜索 100次/天
- 无实时价格，仅位置信息

**API_KEY 申请**：https://lbs.amap.com/api/webservice/guide/create-project/get-key
**环境变量**：`AMAP_API_KEY`

## 使用方式

### 方式一：自然语言（推荐）

直接告诉 AI 助手你的需求：
- "帮我搜深圳龙岗宝龙地铁站附近的四星酒店，明天住一晚"
- "上海迪士尼附近3公里内，价格500以下的酒店"
- "北京故宫附近明天入住两晚"

### 方式二：MCP 直接调用

在支持 MCP 的客户端（Cursor、Windsurf、Claude Desktop）中配置后直接调用。

## 环境变量配置

在 `~/.workbuddy/skills/onezion-hotel-flights/.env` 中配置：

```bash
# 必填（至少一个）
AIGOHOTEL_API_KEY=your_aigohotel_key
JINKO_API_KEY=your_jinko_key
RAPIDAPI_KEY=your_rapidapi_key
AMAP_API_KEY=your_amap_key

# 优先级：AIGoHotel > Jinko > Booking.com（按国内酒店效果排序）
```

## 数据源选择逻辑

| 场景 | 首选 | 备选 |
|------|------|------|
| 国内酒店搜索 | AIGoHotel | Jinko |
| 国内酒店预订 | Jinko | - |
| 海外酒店搜索 | Booking.com | Jinko |
| 海外酒店预订 | Jinko | - |
| POI/地标定位 | 高德地图 | - |
| 实时价格比价 | AIGoHotel | Jinko |

## 申请指南

### AIGoHotel API_KEY 申请

1. 访问 https://mcp.agentichotel.cn/apply
2. 填写申请信息
3. 应用场景描述（参考 below）
4. 获取 API_KEY

### 应用场景描述（可直接使用）

> 我是一名香港大学的学生，正在开发个人 AI 助手（基于 WorkBuddy 平台），用于提升日常生活和旅行规划的效率。我希望接入 AIGoHotel 的酒店搜索能力，让我可以通过自然语言搜索国内酒店的实时价格和信息，用于：
> 1. 个人旅行规划：通过自然语言搜索酒店，按城市、景点、地铁站等维度筛选
> 2. 比价辅助：获取多家酒店的实时价格进行对比
> 3. 数据分析：研究国内酒店市场的价格分布和趋势
>
> 使用场景主要是个人使用，不涉及商业分发。主要用户是我本人，偶尔会分享给朋友。

### Booking.com RapidAPI 申请

1. 访问 https://rapidapi.com/ 注册账号
2. 搜索 "Booking.com"，订阅免费套餐
3. 获取 RapidAPI Key

## 文件结构

```
onezion-hotel-flights/
├── SKILL.md           # 本文件
├── .env.example       # 环境变量模板
├── scripts/
│   ├── search_hotels.py    # 统一搜索脚本
│   └── setup.py            # 初始化脚本
├── mcp-servers/
│   ├── aigohotel.json      # AIGoHotel MCP 配置模板
│   ├── jinko.json          # Jinko MCP 配置模板
│   └── booking.json        # Booking.com MCP 配置模板
└── references/
    └── api-docs.md         # API 文档参考
```
