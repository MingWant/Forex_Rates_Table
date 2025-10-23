# Forex Rates Table - Code Exercise
**作者**: Siu Ming  
**目的**: Code Exercise
**Demo URL**: https://hsm.mingwant.com/
---

## 目標
以滿足用戶需求為準，盡量不畫蛇添足

### ✅ 滿足項
- ✅ 可以GET到到外匯Data
- ✅ 有一個Function專門識別Even Number
- ✅ 新Variables + 10.0002
- ✅ Show到Table
- ✅ Even Num和HKD用紅色框顯示

### 🌟 合理額外（為更好體驗）
- ✅ 可以選擇Base Currency
- ✅ 可以Filter Table內容
- ✅ 可以選擇小數位數 (1-20位)
- ✅ 表格可以排序 (Sort)
- ✅ Docker 容器化部署
---

## 技術選擇

### 架構設計
**前後端分離**：可以分開使用，而且未來可以對API進行修改例如加密、接駁其他Frontend等，並且可以展示我的Skills

### Backend使用: Python
**使用Python原因**：
- 單從該Exercise的要求以及效率上來說，Node.js的確是更好的選擇
- 但這個Exercise是為了展示我的Skills，而我更熟悉Python，用起來更得心應手
- Python更好拓展其他功能，而且對我來說處理數字也更熟手

### Frontend使用: React
**使用React原因**：
- 職位需求中有React
- React在網上可以找到豐富的Template作為參考，UI也較為美觀
- 使用Ant Design (antd) 作為UI Framework，因為有豐富的Components同Example可以參考
- 更輕便設計，Component化令代碼更易維護


## 實現方法

### Backend實現 (Python FastAPI)

#### 1. Backend核心

**`utils.py`**
- `is_even_number()`: 識別雙數的專門Function，處理了各種等情況
  - 使用 `Decimal` 避免浮點數精度問題
  - 支持用戶自己選擇小數位數 (1-20位)
  - 只檢查最後一位數字是否為Even Number
  
- `add_increment_to_rates()`: 給所有匯率加 10.0002
  - 自動處理所有Currencies + 10.0002

- `should_highlight_cell()`: 判斷是否需要紅框顯示
  - Even Num → 紅框
  - HKD → 紅框

**`services.py`**
- `FixerAPIService` Class：專門處理Fixer API的Request
  - `fetch_latest_rates()`: 獲取最新匯率
  - `fetch_all_currencies()`: 所有可用Currency List
  - `get_processed_rates()`: 處理所有Data，包括Original匯率、+10.0002後的匯率、Metadata

**`main.py` - API Endpoints**
- `GET /`: 健康檢查
- `GET /api/rates`: 獲取匯率數據（可選參數: base, symbols, decimals）
- `GET /api/currencies`: 獲取所有可用貨幣
- FAST API自動Gen API Doc: `/api/docs`

#### 2. 為什麼Backend做這麼多處理？
- **前後端分離的好處**: Backend處理所有Logic，Frontend只負責做展示
- **減輕Frontend負擔**: 因為自己比較熟悉Backend,複雜計算（識別Even Num、+10.0002、判斷紅框）在Backend做好
- **數據一致性**: 統一在Backend處理，避免不同Frontend有不同結果
- **未來擴展性**: 容易加入其他功能（例如：數據緩存、用戶認證等）

### Frontend實現 (React)

#### 1. 核心功能

**`App.js`**
- 使用React Hooks (useState, useEffect, useCallback)
- Ant Design Components (Table, Select, Button, Card)
- 自動Load可用Currency List
- 支持Select和Filter Base Currency
- 支持選擇小數位數 (1-20位)
- 表格功能:
  - 排序 (Sort by column)
  - 過濾 (Filter by currency)
  - 分頁 (Pagination)
  - 紅框顯示Even Num和HKD

**`forexService.js`**
- 統一管理所有API Request
- 

**`helpers.js`**
- Formatting Number
- Filter

#### 2. UI/UX考慮
- 使用Ant Design保證UI美觀和現代化
- 清晰的視覺提示（紅框顯示）
- Loading、Success/Error
- Responsive Design
- 操作說明

---

## Project結構

```
Forex_Rates_Table/
├── backend/                    
│   ├── app/
│   │   ├── __init__.py          
│   │   ├── main.py              
│   │   ├── services.py          # 處理Fixer API
│   │   ├── utils.py             # Function（識別Even Number、+10.0002等）
│   │   └── config.py            # Settings
│   ├── Dockerfile               # Backend Docker
│   ├── requirements.txt         # Python Requirements
│   ├── run.py                   # Run Server用
│   └── test.py                  
│
├── frontend/                   
│   └── forex-rates-table/
│       ├── src/
│       │   ├── App.js           # 主要React Component
│       │   ├── App.css          # Style
│       │   ├── api/
│       │   │   └── forexService.js    # Call API
│       │   └── utils/
│       │       └── helpers.js          # 顯示用相關的Function
│       ├── public/              
│       ├── Dockerfile           # Frontend Docker
│       └── package.json         # package
│
├── docker-compose.yml           # Docker-compose
└── README.md                    # 你正在在閱讀的文檔本檔
```

## API文檔

### 1. 獲取匯率Data
```
GET /api/rates?base=EUR&decimals=6
```
**Params**:
- `base` (可選): Base Currency，Default是EUR
- `symbols` (可選): 指定Currencies，用逗號分隔（暫時未用）
- `decimals` (可選): 小數後幾多個位，1-20之間，Default是6

**Response Example**:
```json
{
  "success": true,
  "base_currency": "EUR",
  "date": "2025-10-23",
  "decimals": 6,
  "original_rates": {
    "USD": 1.105,
    "HKD": 8.62,
    ...
  },
  "incremented_rates": {
    "USD": 11.1052,
    "HKD": 18.6202,
    ...
  },
  "metadata": {
    "USD": {
      "highlight_original": false,
      "highlight_incremented": true
    },
    "HKD": {
      "highlight_original": true,
      "highlight_incremented": true
    }
  }
}
```

### 2. 獲取所有可用的Currencies
```
GET /api/currencies
```

**Response示例**:
```json
{
  "success": true,
  "count": 170,
  "currencies": {
    "USD": "United States Dollar",
    "EUR": "Euro",
    "HKD": "Hong Kong Dollar",
    ...
  }
}
```


## 功能
### 主要功能
1. **選擇Base Currency**: 支持Search，從170+多個 Currencies 中選擇
2. **選擇小數位數**: 1-20位，根據需求調整
3. **表格展示**: 
   - Currency Code 和 Name
   - Original匯率
   - 修改後的匯率 (+10.0002)
4. **紅框顯示**: 
   - Even Num → 紅框
   - HKD → 紅框
5. **排序**: 點擊Column可以排序
6. **過濾**: 可以Filter特定Currencies
7. **分頁**: 支持10/20/50/100/200條記錄每頁
---
## 注意事項
1. **API Key**: 
   - 目前使用的是我的個人Fixer API Key
   - 如果無法獲取數據，可能是API Key失效或達到限額，有時候可能是apilayer的Server壞了，已經試過很多次。
---

## 聯繫方式
**Siu Ming**  
Email: siu-ming.hui@connect.polyu.hk  