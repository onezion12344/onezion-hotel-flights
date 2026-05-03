# FlyAI 飞猪 Token 信息

## Token
- **API Key**: sk-xyD4epj-aKAtshcHM05cTyhWLxufxive
- **申请地址**: https://flyai.open.fliggy.com/console
- **环境变量**: FLYAI_API_KEY
- **状态**: ⚠️ 已配置但 401 未解决

## 使用方式
```bash
# 配置
flyai config set FLYAI_API_KEY "sk-xyD4epj-aKAtshcHM05cTyhWLxufxive"

# 搜索酒店
flyai search-hotel --dest-name "深圳大梅沙" --check-in-date 2026-05-04 --check-out-date 2026-05-05 --hotel-stars "4,5" --hotel-bed-types "twin,king" --sort price_asc
```

## 问题
- 2026-05-03: 配置后所有命令均返回 401 Authorization verification failed
- 可能原因：Key 未激活/权限不足/飞猪服务端策略变更
