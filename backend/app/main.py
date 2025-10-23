"""
Main FastAPI Application.
主要用黎做API Endpoint，用FastAPI做，方便之後擴展同埋維護，而且FastAPI有自動Gen API Doc功能，方便睇
"""
from unittest import result
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging

from .config import settings
from .services import fixer_service

# Configure logging, 用黎記錄Log，方便之後Debug同埋睇Error
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Initialize 個 FastAPI app
app = FastAPI(
    title="Forex Rates API",
    description="Professional backend API for forex rates visualization",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    app_author="HUI Siu Ming | siu-ming.hui@connect.polyu.hk"
)

# 配置 CORS (要嚮雲端部署時使用)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Endpoint, 用來檢查API係唔係正常運作緊
@app.get("/")
async def root() -> Dict[str, str]:
    return {
        "status": "healthy",
        "message": "Siu Ming's Forex Rates API is running",
        "version": "1.0.0"
    }


# 主要Endpoint, 用來獲取匯率資料
@app.get("/api/rates")
async def get_forex_rates( 
    base: Optional[str] = None, # 非必要項，可以唔填，但係冇得決定Base Currency
    symbols: Optional[str] = None, # 暫時用唔到，但寫定先，方便之後用
    decimals: Optional[int] = 6  # 最多20位小數位數, Default Set 6位
) -> JSONResponse:
    # 如果decimals有填，就檢查佢係唔係1-20之間，如果唔係就Throw Error
    if decimals is not None:
        if decimals < 1 or decimals > 20:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Siu Ming's Tips: Invalid decimals parameter !!!",
                    "message": "decimals must be between 1 and 20 !!!"
                }
            )
    
    logger.info(f"Fetching forex rates from Fixer API (base={base}, symbols={symbols}, decimals={decimals})")
    data = await fixer_service.get_processed_rates(base=base, symbols=symbols, decimals=decimals)
    return JSONResponse(status_code=200, content=data)

# 額外功能，用黎獲取所有可用貨幣
# 其實嚮Frontend都可以有返一個Dropdown俾用戶自己揀，不過貨幣太多，所以係Backend做埋
# 之所以Backend做埋，唔嚮Frontend做，因為唔想Frontend寫太複雜，而且數據都係經過Backend先，所以直接Backend做埋
@app.get("/api/currencies")
async def get_available_currencies() -> Dict[str, Any]:
    try:
        logger.info("Fetching available currencies from Fixer API")
        data = await fixer_service.fetch_all_currencies()
        
        if data.get("success"):
            symbols = data.get("symbols", {})
            return {
                "success": True,
                "count": len(symbols),
                "currencies": symbols
            }
        else:
            raise Exception("Failed to fetch currencies from API")
        
    except Exception as e:
        logger.error(f"Error fetching currencies: {str(e)}")
        # Fallback to a common list of currencies
        common_currencies = {
            "USD": "United States Dollar",
            "EUR": "Euro",
            "GBP": "British Pound Sterling",
            "JPY": "Japanese Yen",
            "CNY": "Chinese Yuan",
            "HKD": "Hong Kong Dollar",
            "AUD": "Australian Dollar",
            "CAD": "Canadian Dollar",
            "CHF": "Swiss Franc",
            "SGD": "Singapore Dollar",
            "KRW": "South Korean Won",
            "TWD": "Taiwan Dollar",
        }
        return {
            "success": True,
            "count": len(common_currencies),
            "currencies": common_currencies,
            "fallback": True
        }




# 屬於我自己寫嘅 Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Siu Ming's Tips: Not Found !!!",
            "message": "The requested resource was not found !!!"
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler."""
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Siu Ming's Tips: Internal Server Error !!!",
            "message": "An unexpected error occurred !!!"
        }
    )





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )

