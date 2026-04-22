"""
LLM 分析器
使用 Deepseek / Qwen API 进行股票分析
"""
import os
import json
from typing import Dict, Any, Optional, List
from datetime import datetime


class LLMAnalyzer:
    """LLM 分析器基类"""

    def __init__(self, api_key: Optional[str] = None,
                 model: str = "deepseek-chat"):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        self.model = model

    def analyze_sentiment(self, news_list: List[Dict]) -> Dict[str, Any]:
        """
        分析新闻情绪
        返回：情感倾向（positive/negative/neutral）、关键点摘要
        """
        if not self.api_key:
            # 模拟分析（实际使用时接入真实 API）
            return self._mock_sentiment_analysis(news_list)

        # TODO: 实现真实的 Deepseek API 调用
        prompt = self._build_sentiment_prompt(news_list)
        response = self._call_llm(prompt)
        return self._parse_sentiment_response(response)

    def analyze_financial_report(self, stock_code: str,
                                financial_data: Dict) -> Dict[str, Any]:
        """
        分析财报数据
        返回：关键指标解读、风险点、机会点
        """
        if not self.api_key:
            return self._mock_financial_analysis(stock_code, financial_data)

        prompt = self._build_financial_prompt(stock_code, financial_data)
        response = self._call_llm(prompt)
        return self._parse_financial_response(response)

    def generate_daily_report(self, stock_code: str,
                            quote: Dict,
                            news_list: List[Dict]) -> str:
        """
        生成每日投资日报
        """
        if not self.api_key:
            return self._mock_daily_report(stock_code, quote, news_list)

        prompt = self._build_daily_report_prompt(stock_code, quote, news_list)
        return self._call_llm(prompt)

    def _build_sentiment_prompt(self, news_list: List[Dict]) -> str:
        """构建情绪分析 Prompt"""
        news_text = "\n".join([
            f"- {n.get('title', '')} ({n.get('datetime', '')})"
            for n in news_list[:10]
        ])
        return f"""请分析以下财经新闻的整体情绪和关键信息：

{news_text}

请返回 JSON 格式：
{{
  "sentiment": "positive/negative/neutral",
  "confidence": 0.0-1.0,
  "key_points": ["要点1", "要点2", "要点3"],
  "summary": "整体概述"
}}"""

    def _build_financial_prompt(self, stock_code: str,
                                financial_data: Dict) -> str:
        """构建财报分析 Prompt"""
        return f"""请分析股票 {stock_code} 的财务状况：

财务数据：
{json.dumps(financial_data, ensure_ascii=False, indent=2)}

请返回 JSON 格式：
{{
  "overall_score": 0-100,
  "key_metrics": {{
    "盈利能力": "分析",
    "成长性": "分析",
    "偿债能力": "分析",
    "运营效率": "分析"
  }},
  "risks": ["风险点1", "风险点2"],
  "opportunities": ["机会点1", "机会点2"],
  "recommendation": "买入/持有/卖出"
}}"""

    def _build_daily_report_prompt(self, stock_code: str,
                                   quote: Dict,
                                   news_list: List[Dict]) -> str:
        """构建日报 Prompt"""
        news_text = "\n".join([
            f"- {n.get('title', '')}"
            for n in news_list[:5]
        ])
        return f"""请为股票 {stock_code} 生成每日投资分析报告：

今日行情：
- 最新价：{quote.get('price', 'N/A')}
- 涨跌幅：{quote.get('change_pct', 'N/A')}%
- 成交量：{quote.get('volume', 'N/A')}

相关新闻：
{news_text}

请生成一份简洁的日报，包含：
1. 今日行情概述
2. 重要新闻解读
3. 短期走势判断
4. 风险提示

格式要求：使用 Markdown，控制在 500 字以内。
"""

    def _call_llm(self, prompt: str) -> str:
        """调用 LLM API"""
        # TODO: 实现真实的 API 调用
        # import httpx
        # response = httpx.post(...)
        return ""

    def _parse_sentiment_response(self, response: str) -> Dict[str, Any]:
        """解析情绪分析响应"""
        try:
            return json.loads(response)
        except:
            return {"error": "解析失败"}

    def _parse_financial_response(self, response: str) -> Dict[str, Any]:
        """解析财报分析响应"""
        try:
            return json.loads(response)
        except:
            return {"error": "解析失败"}

    def _mock_sentiment_analysis(self,
                                 news_list: List[Dict]) -> Dict[str, Any]:
        """模拟情绪分析（无 API Key 时使用）"""
        return {
            "sentiment": "neutral",
            "confidence": 0.65,
            "key_points": [
                "市场整体平稳",
                "关注政策面消息",
                "资金面有所收紧"
            ],
            "summary": "今日财经新闻整体偏中性，建议关注明日宏观数据发布。"
        }

    def _mock_financial_analysis(self, stock_code: str,
                                 financial_data: Dict) -> Dict[str, Any]:
        """模拟财报分析"""
        return {
            "overall_score": 72,
            "key_metrics": {
                "盈利能力": "毛利率稳定在 25% 左右",
                "成长性": "营收同比增长 15%",
                "偿债能力": "资产负债率适中",
                "运营效率": "应收账款周转加快"
            },
            "risks": [
                "行业竞争加剧",
                "原材料成本波动"
            ],
            "opportunities": [
                "市场份额持续扩大",
                "新产品线布局"
            ],
            "recommendation": "持有"
        }

    def _mock_daily_report(self, stock_code: str,
                          quote: Dict,
                          news_list: List[Dict]) -> str:
        """模拟日报生成"""
        price = quote.get('price', 'N/A')
        change_pct = quote.get('change_pct', 0)

        return f"""# {stock_code} 每日投资报告

**日期**：{datetime.now().strftime('%Y-%m-%d')}

## 今日行情

- 最新价：{price}
- 涨跌幅：{change_pct}%

## 重要新闻

{chr(10).join([f'- {n.get("title", "")}' for n in news_list[:3]])}

## 简评

今日市场情绪较为平稳，建议关注明日经济数据发布。

---
*本报告由 AI 自动生成，仅供参考，不构成投资建议。*
"""


# 全局实例
llm_analyzer = LLMAnalyzer()
