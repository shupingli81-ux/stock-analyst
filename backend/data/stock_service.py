"""
股票数据服务
使用 AKShare 获取 A 股数据
"""
import akshare as ak
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any


class StockService:
    """股票数据服务类"""

    @staticmethod
    def get_realtime_quote(code: str) -> Dict[str, Any]:
        """
        获取个股实时行情
        code: 股票代码，如 '000001' (平安银行)
        """
        try:
            df = ak.stock_zh_a_spot_em()
            # 筛选指定股票
            stock = df[df['代码'] == code]
            if stock.empty:
                return {"error": f"未找到股票 {code}"}

            row = stock.iloc[0]
            return {
                "code": row['代码'],
                "name": row['名称'],
                "price": float(row['最新价']),
                "change_pct": float(row['涨跌幅']),
                "change": float(row['涨跌额']),
                "volume": float(row['成交量']),
                "amount": float(row['成交额']),
                "open": float(row['今开']),
                "high": float(row['最高']),
                "low": float(row['最低']),
                "prev_close": float(row['昨收']),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_history_kline(code: str, period: str = "daily",
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None) -> List[Dict]:
        """
        获取历史K线数据
        period: daily/weekly/monthly
        """
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")

            df = ak.stock_zh_a_hist(symbol=code, period=period,
                                    start_date=start_date, end_date=end_date)

            result = []
            for _, row in df.iterrows():
                result.append({
                    "date": row['日期'],
                    "open": float(row['开盘']),
                    "high": float(row['最高']),
                    "low": float(row['最低']),
                    "close": float(row['收盘']),
                    "volume": float(row['成交量']),
                    "amount": float(row['成交额']),
                    "change_pct": float(row['涨跌幅']) if '涨跌幅' in row else 0
                })
            return result
        except Exception as e:
            return [{"error": str(e)}]

    @staticmethod
    def get_stock_basic_info(code: str) -> Dict[str, Any]:
        """获取股票基本信息"""
        try:
            df = ak.stock_individual_info_em(symbol=code)
            info = {}
            for _, row in df.iterrows():
                info[row['item']] = row['value']
            return info
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def search_stocks(keyword: str) -> List[Dict[str, str]]:
        """搜索股票"""
        try:
            df = ak.stock_zh_a_spot_em()
            # 按名称或代码搜索
            mask = df['名称'].str.contains(keyword, na=False) | \
                   df['代码'].str.contains(keyword, na=False)
            results = df[mask][['代码', '名称']].head(10)
            return results.to_dict('records')
        except Exception as e:
            return [{"error": str(e)}]

    @staticmethod
    def get_news() -> List[Dict[str, Any]]:
        """获取财经新闻"""
        try:
            df = ak.stock_news_em()
            news = []
            for _, row in df.head(20).iterrows():
                news.append({
                    "title": row['新闻标题'],
                    "url": row['新闻链接'],
                    "datetime": row['发布时间'],
                    "source": row['文章来源']
                })
            return news
        except Exception as e:
            return [{"error": str(e)}]


# 全局实例
stock_service = StockService()
