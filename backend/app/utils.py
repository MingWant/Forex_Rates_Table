"""
工具專用區，專門用黎處理匯率資料嘅工具
"""
from typing import Dict, Any
import math
from decimal import Decimal, ROUND_HALF_UP


# 題目硬性要求之一，檢查最後一個數字係唔係Even Number, 係就True, 唔係就False
def is_even_number(value, decimals: int = 6) -> bool:
    # 淨係從個API入面Get返黎嘅數據睇，會有幾個情況要處理，之後可能會有其他情況
    # 1. 整數(integer)
    # 2. 小數(decimal)
    # 3. 科學記數法(scientific notation)
    # 用Float同Double似乎都會有精度問題，所以一定要用Decimal來避免精度問題，避免出現奇怪嘅結果
    # 保證係String先，再轉換為Decimal，保持原始嘅精度，避免精度問題
    decimal_value = Decimal(str(value))
    # 根據用戶指定嘅小數位數進行四捨五入，由用戶話事，用戶話要幾多位小數位數就幾多位小數位數
    # 例如 decimals=4 -> '0.0001'，咁就四捨五入到小數點後4位，咁就唔會有精度問題
    quantize_precision = Decimal('0.' + '0' * (decimals - 1) + '1')
    decimal_value = decimal_value.quantize(quantize_precision, rounding=ROUND_HALF_UP)
    # 再將個decimal_value標準化，方便後面處理
    value_str = format(decimal_value, 'f')
    # 先分清楚原本係唔係整數先，如果係就唔需要處理，如果係小數就處理
    if '.' in value_str:
        # 有小數點就分開整數部分同小數部分
        integer_part, decimal_part = value_str.split('.')
        # 只移除小數部分嘅尾隨0
        decimal_part = decimal_part.rstrip('0')
        # 如果小數被清空咗，咁就唔需要小數點，直接用整數部分
        if not decimal_part:
                value_str = integer_part
        else:
                value_str = integer_part + decimal_part
    else:
        # 無小數點,即係一開始就係整數,咁就Pass
        pass

    # 淨係要最後一位數字，轉換為int，防止出現奇奇怪怪嘅結果
    last_digit = int(value_str[-1])
    # 檢查最後一位數字係唔係Even Number就搞掂，Perfect！
    return last_digit % 2 == 0



# 題目硬性要求之一，加10.0002到所有貨幣匯率
def add_increment_to_rates(rates: Dict[str, float], increment: float = 10.0002, decimals: int = 6) -> Dict[str, float]:
    updated_rates = {}
    # for loop 處理所有貨幣匯率
    for currency, rate in rates.items():
        # 加上指定數字10.0002
        new_rate = rate + increment
        # 四捨五入到指定的小數位數，避免浮點數精度問題
        new_rate = round(new_rate, decimals)
        # 新Dictionary，key係貨幣，value係新匯率
        updated_rates[currency] = new_rate
    return updated_rates



# 題目硬性要求之一，檢查係唔係Even Number 同埋 HKD貨幣, 係就True(要Highlight), 唔係就False(唔要Highlight)
# 前後端分離咗，所以唔需要係Frontend做，而且數據都係經過Backend先，所以直接Backend做埋
def should_highlight_cell(currency: str, value, decimals: int = 6) -> bool:
    return is_even_number(value, decimals) or currency == "HKD"



# 四捨五入用，有機會用到，所以寫住先
def format_rate_for_display(rate: float, decimals: int = 6) -> str:
    return f"{rate:.{decimals}f}"

