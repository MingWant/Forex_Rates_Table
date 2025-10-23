// 檢查Row應該Highlight
export const shouldHighlightRow = (record) => {
    return record.currency === 'HKD' || 
           record.highlightOriginal || 
           record.highlightIncremented;
  };
  
  // Format Number, 直接顯示Backend Return嘅Number
  export const formatNumber = (value) => {
    return value;
  };
  
  // Currency Filters, 當Currency Code Column有Filtering功能時，會有以下Function
  export const getCurrencyFilters = (rates) => {
    if (!rates) return [];
    return Object.keys(rates).map(currency => ({
      text: currency,
      value: currency,
    }));
  };