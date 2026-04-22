# AI 智能股票分析系统 - 任务规范

## 📋 项目概述

**目标**：构建一款 AI 驱动的股票分析工具，通过 LLM 解读财报、生成投资日报

## 🎯 核心功能

### v1.0.1 数据基础
- [ ] A股实时行情查询
- [ ] 个股历史K线数据
- [ ] 财经新闻爬取
- [ ] 基础技术指标计算

### v1.0.2 LLM 智能分析
- [ ] 财报关键指标提取
- [ ] 新闻舆情情感分析
- [ ] Prompt 工程调优
- [ ] Deepseek/Qwen API 接入

### v1.0.3 报告生成
- [ ] 每日投资日报自动生成
- [ ] 个股深度分析报告
- [ ] 可视化图表展示

## 🛠️ 技术架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   数据层    │ ──▶ │   LLM 分析层 │ ──▶ │   前端展示  │
│ AKShare    │     │ Deepseek API │     │   Vue3     │
│ 财经新闻   │     │ Prompt 工程  │     │   ECharts  │
└─────────────┘     └─────────────┘     └─────────────┘
```

## 📁 目录结构

```
stock-analyst/
├── backend/
│   ├── main.py           # FastAPI 入口
│   ├── requirements.txt  # 依赖
│   ├── data/
│   │   └── stock_service.py  # 股票数据服务
│   ├── llm/
│   │   └── analyzer.py   # LLM 分析器
│   └── api/
│       └── routes.py     # API 路由
├── frontend/             # Vue3 前端 (后续)
└── docs/
    ├── TASK.md
    └── CHANGELOG.md
```

## 🔧 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.11+ / FastAPI |
| 数据 | AKShare、Tushare |
| LLM | Deepseek API / Qwen API |
| 前端 | Vue3 + TypeScript + ECharts |
| 部署 | Docker |

## 📝 API 设计

### 股票数据
- `GET /api/stock/quote/{code}` - 获取实时行情
- `GET /api/stock/history/{code}` - 获取历史K线
- `GET /api/stock/news` - 获取财经新闻

### LLM 分析
- `POST /api/analyze/news` - 分析新闻情绪
- `POST /api/analyze/financial` - 分析财报
- `POST /api/report/daily` - 生成日报

## ⚠️ 注意事项

- 投资有风险，AI 分析仅供参考
- 实时行情数据需使用付费 API 获取
- 遵守各大平台的数据使用条款
