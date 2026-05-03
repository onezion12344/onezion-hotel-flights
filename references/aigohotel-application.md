# AIGoHotel API_KEY 申请材料

> 用于向 AIGoHotel 提交 MCP API 接入申请。

---

## 📝 申请信息

| 项目 | 内容 |
|------|------|
| **产品名称** | onezion-hotel-flights（个人 AI 助手 - 酒店搜索模块） |
| **申请平台** | AIGoHotel MCP 服务 |
| **申请链接** | https://mcp.agentichotel.cn/apply |
| **申请人身份** | 香港大学（HKU）人工智能方向学生 |
| **使用场景** | 个人效率提升工具（非商业） |

---

## 🌐 应用场景描述

> 我是一名香港大学（HKU）的人工智能方向学生，正在开发集成 AI Agent 的个人助手系统（基于 WorkBuddy 平台）。我需要接入 AIGoHotel 的酒店搜索 MCP 服务，以实现以下功能：
>
> 1. **自然语言酒店搜索**：通过 AI 助手以自然语言描述需求（如"深圳龙岗宝龙地铁站附近四星酒店，明天一晚"），实时获取符合条件的酒店列表和价格
> 2. **多源比价**：将 AIGoHotel 的搜索结果与其他数据源（高德地图 POI、Booking.com 等）进行交叉验证，为用户提供最优选择
> 3. **出行规划自动化**：结合 AI Agent 的其他能力（日历管理、行程规划），为用户提供端到端的出行体验
>
> 主要用户群体为个人用户和平时的社交圈内分享。使用场景是非商业的个人效率提升工具。

---

## 🔗 使用证明

本项目开源在 GitHub，提供完整的 Skill 文档和 MCP 配置模板，相关资源包括：

### 项目代码

- **项目名称**：onezion-hotel-flights
- **仓库地址**：托管于 GitHub 个人仓库
- **编程语言**：Python 3 + MCP 协议
- **许可证**：MIT

### 完整性证明

项目包含以下文件，证明已具备完整的技术方案和使用能力：

```
onezion-hotel-flights/
├── SKILL.md                # 完整的 Skill 定义文档（含架构、触发词、使用方式）
├── README.md               # 项目说明文档
├── .env.example            # 环境变量模板（含 AIGOHOTEL_API_KEY）
├── scripts/
│   └── search_hotels.py    # 已实现的 AIGoHotel API 调用脚本
├── mcp-servers/
│   └── aigohotel.json      # AIGoHotel MCP 配置文件（HTTP 远程模式）
└── references/
    ├── api-docs.md         # API 文档参考
    └── aigohotel-application.md  # 本申请材料
```

### MCP 配置模板

文件 `mcp-servers/aigohotel.json` 内容：

```json
{
  "aigohotel-mcp": {
    "url": "https://mcp.aigohotel.com/mcp",
    "type": "http",
    "headers": {
      "Authorization": "Bearer ${AIGOHOTEL_API_KEY}"
    }
  }
}
```

### 调用代码示例

文件 `scripts/search_hotels.py` 中的核心调用逻辑：

```python
def search_aigohotel(place, checkin=None, stay_nights=1, star_min=3, star_max=5, size=5):
    """AIGoHotel 酒店搜索"""
    api_key = os.environ.get('AIGOHOTEL_API_KEY', '')
    if not api_key:
        return {"error": "AIGOHOTEL_API_KEY not set"}
    
    payload = json.dumps({
        "place": place,
        "checkIn": checkin or (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "stayNights": stay_nights,
        "starRatings": [star_min, star_max],
        "size": size,
        "withHotelAmenities": True,
        "withRoomAmenities": False
    }).encode()
    
    req = urllib.request.Request(
        "https://mcp.aigohotel.com/api/find-hotels",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())
```

---

## 💡 技术方案亮点

### 1. MCP 协议标准化

采用 MCP（Model Context Protocol）作为 AI 工具的标准接口协议，AIGoHotel MCP 作为 HTTP 远程服务接入，与 AI Agent 框架天然兼容。

### 2. 多源数据融合

AIGoHotel 作为**国内酒店搜索首选**数据源，与其他三个数据源形成互补：

| 场景 | 首选数据源 |
|------|-----------|
| 国内按地铁站/景点搜索 | ✅ **AIGoHotel** |
| 国内实时价格查询 | ✅ **AIGoHotel** |
| 国内酒店预订 | Jinko |
| 海外酒店搜索 | Booking.com |
| 位置信息补充 | 高德地图 |

### 3. 自然语言交互

用户无需学习任何命令或操作流程，直接用日常语言描述需求，AI 自动完成意图理解、地点提取、参数填充、数据查询和结果呈现的全流程。

---

## 🎯 预期效果

接入 AIGoHotel API 后，系统将能够：

1. **实时查询**国内主要城市的酒店价格和房态
2. 按**地铁站名称**进行精准位置搜索（如"宝龙地铁站"）
3. 按**景点/商圈**进行周边搜索（如"上海迪士尼"、"北京故宫"）
4. 按**星级**进行筛选过滤
5. 同时获取酒店**设施信息**，辅助决策
6. 在 AI 对话中**多轮交互**（先搜酒店、再查详情、再比价）

---

## 📮 联系方式

| 项目 | 内容 |
|------|------|
| **申请人** | 香港大学 人工智能方向学生 |
| **项目名称** | onezion-hotel-flights |
| **使用性质** | 个人非商业用途 |

---

<p align="center">
  <sub>感谢 AIGoHotel 团队提供优质的 MCP 服务 🙏</sub>
</p>
