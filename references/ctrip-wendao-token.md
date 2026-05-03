# 携程问道 Token 信息

## Token
- **API Token**: 37f753e39abe428dbb4a5ec5f2369a5d
- **申请地址**: https://www.ctrip.com/wendao/openclaw
- **过期时间**: 2027-05-04 05:38:40
- **环境变量**: WENDAO_API_KEY
- **状态**: ✅ 已验证可用

## 使用方式
```bash
cd ~/.workbuddy/skills/携程问道
WENDAO_API_KEY="37f753e39abe428dbb4a5ec5f2369a5d" node scripts/wendao_query.js "你的问题"
```

## 注意事项
- Token 会过期，注意续期
- 携程问道不支持图片展示，只能返回文字
