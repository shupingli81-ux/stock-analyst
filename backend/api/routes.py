"""
API 路由
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from data.stock_service import stock_service
from llm.analyzer import llm_analyzer

router = APIRouter()


# ============ 请求/响应模型 ============

class AnalyzeNewsRequest(BaseModel):
    news: List[Dict[str, Any]]


class AnalyzeFinancialRequest(BaseModel):
    stock_code: str
    financial_data: Dict[str, Any]


class DailyReportRequest(BaseModel):
    stock_code: str


# ============ 股票数据 API ============

@router.get("/stock/quote/{code}")
async def get_stock_quote(code: str):
    """获取个股实时行情"""
    result = stock_service.get_realtime_quote(code)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/stock/history/{code}")
async def get_stock_history(
    code: str,
    period: str = "daily",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """获取历史K线数据"""
    result = stock_service.get_history_kline(code, period, start_date, end_date)
    if result and "error" in result[0]:
        raise HTTPException(status_code=404, detail=result[0]["error"])
    return {"code": code, "data": result}


@router.get("/stock/search")
async def search_stocks(keyword: str):
    """搜索股票"""
    results = stock_service.search_stocks(keyword)
    return {"results": results}


@router.get("/stock/info/{code}")
async def get_stock_info(code: str):
    """获取股票基本信息"""
    result = stock_service.get_stock_basic_info(code)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/stock/news")
async def get_news():
    """获取财经新闻"""
    news = stock_service.get_news()
    return {"news": news}


# ============ LLM 分析 API ============

@router.post("/analyze/news")
async def analyze_news_sentiment(request: AnalyzeNewsRequest):
    """分析新闻情绪"""
    result = llm_analyzer.analyze_sentiment(request.news)
    return result


@router.post("/analyze/financial")
async def analyze_financial(request: AnalyzeFinancialRequest):
    """分析财报"""
    result = llm_analyzer.analyze_financial_report(
        request.stock_code,
        request.financial_data
    )
    return result


@router.post("/report/daily")
async def generate_daily_report(request: DailyReportRequest):
    """生成每日投资日报"""
    code = request.stock_code

    # 获取今日行情
    quote = stock_service.get_realtime_quote(code)
    if "error" in quote:
        raise HTTPException(status_code=404, detail=quote["error"])

    # 获取相关新闻
    news = stock_service.get_news()

    # 生成日报
    report = llm_analyzer.generate_daily_report(code, quote, news)

    return {
        "stock_code": code,
        "report": report,
        "generated_at": quote.get("timestamp")
    }


# ============ 股票列表 ============

@router.get("/stocks/list")
async def get_stocks_list():
    """获取沪深股票列表（常用股票）"""
    # 返回一些常用股票
    return {
        "stocks": [
            {"code": "000001", "name": "平安银行"},
            {"code": "000002", "name": "万科A"},
            {"code": "600036", "name": "招商银行"},
            {"code": "600519", "name": "贵州茅台"},
            {"code": "601318", "name": "中国平安"},
            {"code": "601888", "name": "中国中免"},
            {"code": "000858", "name": "五粮液"},
            {"code": "600887", "name": "伊利股份"},
        ]
    }
