---
name: onezion-hotel-flights
version: "2.0.0"
author: onezion
updated: "2026-05-03"
triggers:
  - "酒店"
  - "订酒店"
  - "hotel"
  - "booking"
  - "住宿"
  - "比价"
  - "酒店推荐"
  - "酒店搜索"
  - "海景酒店"
description: "AI 酒店搜索与比价工具，整合3个有效数据源（携程问道、AIGoHotel MCP、agent-browser 实时抓取），支持自然语言搜索实时价格、海景/公园筛选、品牌对比。"
---

# onezion-hotel-flights 🏨

AI 酒店搜索与比价工具。三个有效数据源 + 浏览器实时抓取，自然语言即搜即出结果。

## 架构

```
用户自然语言 → 智能路由 → 数据源
                        ├── 携程问道（官方直连，价格最准）✅
                        ├── AIGoHotel MCP（批发渠道价）✅
                        ├── agent-browser 浏览器抓取（携程/美团实时价）✅
                        └── FlyAI 飞猪（需申请API_KEY）⚠️ 未验证
```

## 数据源详情

### 1. 携程问道（首选 ⭐⭐⭐⭐⭐）✅ 已验证

**数据来源**：携程官方直连，实时价格，支持预订跳转

**获取 Token**：https://www.ctrip.com/wendao/openclaw → 登录后复制 API token
**环境变量**：`WENDAO_API_KEY`
**当前 Token**：37f753e39abe428dbb4a5ec5f2369a5d（到期 2027-05-04）

**使用方式**：
```bash
cd ~/.workbuddy/skills/携程问道
WENDAO_API_KEY="你的token" node scripts/wendao_query.js "用户自然语言问题"
```

**适用场景**：酒店搜索、机票、火车票、景点、行程规划

### 2. AIGoHotel MCP（备选 ⭐⭐⭐）✅ 已验证

**数据来源**：深圳道旅科技（阿里投资，14年B2B批发商），批发渠道价
**获取 API_KEY**：https://mcp.agentichotel.cn/apply
**当前状态**：✅ 已配置，已验证

**使用方式**：
```bash
# 搜索 API
curl -s -X POST "https://mcp.aigohotel.com/mcp/hotelsearch" \
  -H "Authorization: Bearer $AIGOHOTEL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"originQuery":"...","place":"...","placeType":"城市/景点/地铁站","countryCode":"CN","checkInParam":{"checkInDate":"2026-05-04","stayNights":1,"adultCount":2},"filterOptions":{"starRatings":[3.5,5]},"size":8}'

# 详情 API（真实房型+价格）
curl -s -X POST "https://mcp.aigohotel.com/mcp/hoteldetail" \
  -H "Authorization: Bearer $AIGOHOTEL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"hotelId":12345,"dateParam":{"checkInDate":"2026-05-04","checkOutDate":"2026-05-05"}}'
```

**关键注意**：
- httpx 请求需 `trust_env=False`（绕过系统代理）
- 搜索价 ≠ 实际可订价，必须用详情 API 查真实价格
- GitHub: https://github.com/longcreat/aigohotel-mcp

### 3. agent-browser 浏览器抓取（最强 ⭐⭐⭐⭐⭐）

**原理**：用 agent-browser 打开携程/美团/飞猪，像真人一样操作，反爬风险最低

**使用场景**：
- 携程/美团已登录态下获取最终消费者价格
- 抓取截图（海报素材）
- 验证 AIGoHotel 数据

**命令**：
```bash
agent-browser connect 9222
agent-browser open "https://hotels.ctrip.com/hotel/shenzhen30/?checkin=2026/05/04&checkout=2026/05/05&starlist=4"
agent-browser snapshot
agent-browser screenshot --output /tmp/ctrip_result.png
```

### 4. FlyAI 飞猪（未验证 ⚠️）

**获取 API_KEY**：https://flyai.open.fliggy.com/console
**配置**：`flyai config set FLYAI_API_KEY "你的Key"`
**当前 Key**：sk-xyD4epj-aKAtshcHM05cTyhWLxufxive
**状态**：⚠️ 配置后仍 401 未解决

## 数据源选择逻辑

| 场景 | 首选 | 备选 |
|------|------|------|
| 国内酒店搜索（最准） | 携程问道 | AIGoHotel |
| 海外酒店 | Booking MCP | - |
| 最终消费者价格 | agent-browser 携程 | - |
| 比价参考 | AIGoHotel | - |

## 环境变量配置

```bash
# ~/.workbuddy/skills/onezion-hotel-flights/.env
WENDAO_API_KEY=37f753e39abe428dbb4a5ec5f2369a5d
AIGOHOTEL_API_KEY=mcp_8bfbf705ee55485396b4eec1f32291c4
FLYAI_API_KEY=sk-xyD4epj-aKAtshcHM05cTyhWLxufxive
```

## MCP 配置（~/.workbuddy/mcp.json）

```json
{
  "aigohotel-mcp": {
    "url": "https://mcp.aigohotel.com/mcp",
    "type": "http",
    "headers": {
      "Authorization": "Bearer mcp_8bfbf705ee55485396b4eec1f32291c4",
      "Content-Type": "application/json"
    }
  }
}
```

## 文件结构

```
onezion-hotel-flights/
├── SKILL.md           # 本文件
├── README.md          # 项目文档
├── .env.example       # 环境变量模板
├── .env               # 真实 Key（不上传）
├── .gitignore         # 忽略 .env
├── scripts/
│   └── search_hotels.py    # AIGoHotel 搜索脚本
├── mcp-servers/
│   ├── aigohotel.json      # AIGoHotel MCP 配置模板
│   └── jinko.json          # Jinko MCP 配置模板
└── references/
    ├── aigohotel-application.md   # 申请材料
    ├── api-docs.md                # API 文档参考
    └── ctrip-wendao-token.md      # 携程问道 token 信息
```

## 安全审计结果（2026-05-03）

| 数据源 | 风险 | 个人可用 | 说明 |
|--------|------|---------|------|
| 携程问道 | 🟢 低 | ✅ | 携程官方，需申请token |
| AIGoHotel | 🟡 中 | ✅ | 道旅科技14年+阿里投资，MCP产品2星 |
| Booking MCP | 🟠 中高 | ⚠️ | 底层是第三方爬虫，非官方API |
| FlyAI飞猪 | ⚠️ 未验证 | ✅ | 阿里飞猪官方，需申请Key |
| 高德地图API | 🔴 中高 | ❌ | 个人开发者被清退，5万/年 |
| Jinko MCP | 🟡 中 | ⚠️ | GitHub原始仓库已删除🚩 |

## 版本历史

- v1.0: 初始版本（AIGoHotel + Booking + Jinko + 高德）
- v2.0: 重写（去掉无效数据源，加入携程问道 + agent-browser + FlyAI）
