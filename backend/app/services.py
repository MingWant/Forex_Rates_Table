"""
Business logic and external API services.
Demonstrates separation of concerns and error handling.
"""
import httpx
from typing import Dict, Any, Optional
from .config import settings
from .utils import add_increment_to_rates, should_highlight_cell, format_rate_for_display


# Fixer API Service Class, 用黎處理Fixer API嘅Request同Response
class FixerAPIService:
    def __init__(self):
        self.api_key = settings.fixer_api_key
        self.api_url = settings.fixer_api_url
        self.timeout = 10.0
        



    # 題目硬性要求之一，獲取最新匯率資料。可以自定義Base Currency同Symbols（我自己認為應該要填，唔填就會用原本個預設值）
    async def fetch_latest_rates(
        self,
        # 非必要項，可以唔填，但係唔可以冇，唔填就會用原本個Default Values
        base: Optional[str] = None, 
        symbols: Optional[str] = None
    ) -> Dict[str, Any]:
        headers = {
            "apikey": self.api_key
        }
        params = {}

        if base:
            params["base"] = base
        if symbols:
            params["symbols"] = symbols
        
        symbols_url = self.api_url + "/latest"

        # Async Client
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                symbols_url,
                headers=headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
    



    # 獲取所有可用貨幣,額外功能，用黎確認有咩貨幣係可以用嘅，咁就可以比用戶自己選擇Base啦
    # 其實嚮Frontend都可以有返一個Dropdown俾用戶自己揀，不過貨幣太多，所以係Backend做埋
    async def fetch_all_currencies(self) -> Dict[str, Any]:
        headers = {
            "apikey": self.api_key
        }

        symbols_url = self.api_url + "/symbols"

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                symbols_url,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
    



    # 直接處理所有數據，包括原始匯率、增量匯率、Base Currency、Metadata，隨時可以改動返個Function黎做其他野
    async def get_processed_rates(
        self, 
        base: Optional[str] = None, 
        symbols: Optional[str] = None,
        decimals: int = 6
    ) -> Dict[str, Any]:
        api_data = await self.fetch_latest_rates(base=base, symbols=symbols)
        
        original_rates = {
            currency: round(rate, decimals) 
            for currency, rate in api_data.get("rates", {}).items()
        }
        
        incremented_rates = add_increment_to_rates(original_rates, decimals=decimals)
        
        base_currency = api_data.get("base", "EUR")
        
        # 確保Base Currency係嚮original_rates入面，如果唔係就加返入去
        if base_currency not in original_rates:
            original_rates[base_currency] = 1.0
            incremented_rates[base_currency] = round(11.0002, decimals)
        
        # 直接整個Dictionary出黎，用黎Highlight係唔係Even Number同埋係唔係HKD貨幣
        # 之所以Backend做埋，唔嚮Frontend做，因為唔想Frontend寫太複雜，而且數據都係經過Backend先，所以直接Backend做埋
        metadata = {}
        for currency in original_rates.keys():
            metadata[currency] = {
                "highlight_original": should_highlight_cell(currency, original_rates[currency], decimals),
                "highlight_incremented": should_highlight_cell(currency, incremented_rates[currency], decimals)
            }
        
        return {
            "success": True,
            "base_currency": base_currency,
            "timestamp": api_data.get("timestamp"),
            "date": api_data.get("date"),
            "decimals": decimals,
            "original_rates": original_rates,
            "incremented_rates": incremented_rates,
            "metadata": metadata
        }


# Global Service Instance
fixer_service = FixerAPIService()

