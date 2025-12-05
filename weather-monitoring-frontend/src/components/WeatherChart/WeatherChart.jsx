import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { useWeatherChart } from './WeatherChart.hook';
import './WeatherChart.css';

export const WeatherChart = ({ data }) => {
  const { chartData } = useWeatherChart(data);

  if (!data || chartData.length === 0) {
    return (
      <div className="chart-container">
        <h3>📈 Temperature & Humidity Trends</h3>
        <div className="chart-empty">
          <p>No trend data available yet</p>
          <small>Data will appear after hourly summary computation</small>
        </div>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <h3>📈 Temperature & Humidity Trends</h3>
      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart
            data={chartData}
            margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="time"
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
            />
            <YAxis
              yAxisId="left"
              stroke="#ef4444"
              style={{ fontSize: '12px' }}
              label={{ value: 'Temperature (°C)', angle: -90, position: 'insideLeft' }}
            />
            <YAxis
              yAxisId="right"
              orientation="right"
              stroke="#3b82f6"
              style={{ fontSize: '12px' }}
              label={{ value: 'Humidity (%)', angle: 90, position: 'insideRight' }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                fontSize: '12px',
              }}
            />
            <Legend
              wrapperStyle={{ fontSize: '14px' }}
              iconType="line"
            />
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="temperature"
              stroke="#ef4444"
              strokeWidth={3}
              dot={{ fill: '#ef4444', r: 4 }}
              activeDot={{ r: 6 }}
              name="Temperature (°C)"
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="humidity"
              stroke="#3b82f6"
              strokeWidth={3}
              dot={{ fill: '#3b82f6', r: 4 }}
              activeDot={{ r: 6 }}
              name="Humidity (%)"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
