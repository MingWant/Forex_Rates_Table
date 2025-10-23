// 由於硬性要求唔比用GenAI幫手設計UI，用咗https://ant.design/components黎設計UI
// 因為上面好多Template同Example可以參考，咁樣可以快D設計, 但係唔可以完全"Copy & Paste"，要Adapt埋自己嘅需求
import React, { useState, useEffect, useCallback } from 'react';
import { Table, Select, Button, message, Card, Space, Typography } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';
import * as forexApi from './api/forexService';
import { shouldHighlightRow, formatNumber, getCurrencyFilters } from './utils/helpers';
import './App.css';

const { Title } = Typography;
const { Option } = Select;

function App() {
  const [currencies, setCurrencies] = useState([]);
  const [baseCurrency, setBaseCurrency] = useState('EUR');
  const [decimals, setDecimals] = useState(6);
  const [ratesData, setRatesData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Load 個 available currencies
  const loadCurrencies = useCallback(async () => {
    try {
      const data = await forexApi.fetchCurrencies();
      if (data.success) {
        const currencyList = Object.keys(data.currencies).map(code => ({
          code,
          name: data.currencies[code]
        }));
        setCurrencies(currencyList);
      }
    } catch (error) {
      message.error('Get Currencies Failed');
      console.error('Error fetching currencies:', error);
    }
  }, []);

  // Load 個 Forex Rates
  const loadRates = useCallback(async () => {
    setLoading(true);
    try {
      const data = await forexApi.fetchRates(baseCurrency, decimals);
      if (data.success) {
        setRatesData(data);
        message.success(`Forex rates data fetched successfully (${decimals} decimals)`);
      }
    } catch (error) {
      message.error('Get Rates Failed');
      console.error('Error fetching rates:', error);
    } finally {
      setLoading(false);
    }
  }, [baseCurrency, decimals]);

  // Load 個 available currencies On Mount, 每次Mount都會Load一次
  useEffect(() => {
    loadCurrencies();
  }, [loadCurrencies]);

  // Load 個 default EUR rates
  useEffect(() => {
    if (currencies.length > 0) {
      loadRates();
    }
  }, [currencies, loadRates]);

  // Handle Table Data
  const getTableData = () => {
    if (!ratesData) return [];

    const { original_rates, incremented_rates, metadata } = ratesData;
    
    return Object.keys(original_rates).map((currency, index) => ({
      key: index,
      currency,
      currencyName: currencies.find(c => c.code === currency)?.name || currency,
      originalRate: original_rates[currency],
      incrementedRate: incremented_rates[currency],
      highlightOriginal: metadata[currency]?.highlight_original,
      highlightIncremented: metadata[currency]?.highlight_incremented
    }));
  };

  // Table Columns,其中包括Currency Code, Currency Name, Original Rate, Modified Rate，有Sorting同Filtering功能
  const columns = [
    {
      title: 'Currency Code',
      dataIndex: 'currency',
      key: 'currency',
      sorter: (a, b) => a.currency.localeCompare(b.currency),
      filters: getCurrencyFilters(ratesData?.original_rates),
      onFilter: (value, record) => record.currency === value,
      filterSearch: true,
      width: 150,
    },
    {
      title: 'Currency Name',
      dataIndex: 'currencyName',
      key: 'currencyName',
      sorter: (a, b) => a.currencyName.localeCompare(b.currencyName),
    },
    {
      title: 'Original Rate',
      dataIndex: 'originalRate',
      key: 'originalRate',
      sorter: (a, b) => a.originalRate - b.originalRate,
      onCell: (record) => ({
        style: {
          border: record.highlightOriginal ? '1px solid red' : undefined,
          backgroundColor: record.highlightOriginal ? '#fff1f0' : undefined,
        }
      }),
      render: (value) => formatNumber(value),
      width: 180,
    },
    {
      title: 'Modified Rate (+10.0002)',
      dataIndex: 'incrementedRate',
      key: 'incrementedRate',
      sorter: (a, b) => a.incrementedRate - b.incrementedRate,
      onCell: (record) => ({
        style: {
          border: record.highlightIncremented ? '3px solid red' : undefined,
          backgroundColor: record.highlightIncremented ? '#fff1f0' : undefined,
        }
      }),
      render: (value) => formatNumber(value),
      width: 200,
    },
  ];

  // Return 個 App Component
  return (
    <div className="App">
      <div className="container">
        <Title level={2} style={{ textAlign: 'center', marginBottom: '30px' }}>
          Forex Rates Table by Siu Ming
        </Title>

        <Card style={{ marginBottom: '20px' }}>
          <Space size="large" wrap>
            <div>
              <label style={{ marginRight: '10px', fontWeight: 'bold' }}>Select Base Currency:</label>
              <Select
                showSearch
                value={baseCurrency}
                onChange={setBaseCurrency}
                style={{ width: 250 }}
                placeholder="Select or search currency"
                filterOption={(input, option) => {
                  // 可以打字或者選擇Currency Code
                  const searchText = option.label || '';
                  return searchText.toLowerCase().includes(input.toLowerCase());
                }}
              >
                {currencies.map(curr => (
                  <Option key={curr.code} value={curr.code} label={`${curr.code} - ${curr.name}`}>
                    {curr.code} - {curr.name}
                  </Option>
                ))}
              </Select>
            </div>

            <div>
              <label style={{ marginRight: '10px', fontWeight: 'bold' }}>Decimal Places in Maximum::</label>
              <Select
                value={decimals}
                onChange={setDecimals}
                style={{ width: 120 }}
                placeholder="Select decimals"
              >
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20].map(num => (
                  <Option key={num} value={num}>
                    {num} {num === 1 ? 'digit' : 'digits'} 
                  </Option>
                ))}
              </Select>
            </div>
            
            <Button
              type="primary"
              icon={<ReloadOutlined />}
              onClick={loadRates}
              loading={loading}
              size="large"
            >
              Get Forex Rates Data
            </Button>
          </Space>

          {ratesData && (
            <div style={{ marginTop: '20px' }}>
              <p><strong>Base Currency:</strong> {ratesData.base_currency}</p>
              <p><strong>Date:</strong> {ratesData.date}</p>
              <p><strong>Decimal Places in Maximum:</strong> {ratesData.decimals} digits</p>
            </div>
          )}
        </Card>

        <Card>
          <Table
            columns={columns}
            dataSource={getTableData()}
            loading={loading}
            rowClassName={(record) => shouldHighlightRow(record) ? 'highlight-row' : ''}
            pagination={{
              defaultPageSize: 10,
              showSizeChanger: true,
              pageSizeOptions: ['10', '20', '50', '100', '200'],
              showTotal: (total) => `${total} records`,
            }}
            scroll={{ x: 800 }}
            bordered
          />
        </Card>

        <div style={{ marginTop: '20px', padding: '15px', background: '#f0f2f5', borderRadius: '8px' }}>
          <Title level={5}>Description by Siu Ming:</Title>
          <ul style={{ listStyleType: 'square', padding: '10px' }}>
            <li>If you cannot get the currency list or see the table, check https://api.apilayer.com/ is working or not first or my apikey is invalid, contact me if you have any questions.</li>
            <li>Border colour of Red: Even Number or HKD currency</li>
            <li>Modified Rate = Original Rate + 10.0002</li>
            <li>Can sort by clicking the column title</li>
            <li>Use the filter icon in Currency Code column to filter specific currencies</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;
