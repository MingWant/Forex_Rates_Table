import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

// Fetch All Available Currencies
export const fetchCurrencies = async () => {
  const response = await axios.get(`${API_BASE_URL}/api/currencies`);
  return response.data;
};

// Fetch Forex Rates
export const fetchRates = async (baseCurrency, decimals) => {
  const response = await axios.get(`${API_BASE_URL}/api/rates`, {
    params: { 
      base: baseCurrency,
      decimals: decimals
    }
  });
  return response.data;
};