import { useMemo } from 'react';

export const useWeatherChart = (data) => {
  const chartData = useMemo(() => {
    if (!data || !data.trend_data || !data.trend_data.hourly_temps) {
      return [];
    }

    return data.trend_data.hourly_temps.map((item) => ({
      time: new Date(item.time).toLocaleTimeString('en-IN', {
        hour: '2-digit',
        minute: '2-digit',
      }),
      temperature: Math.round(item.temperature * 10) / 10,
      humidity: item.humidity,
    }));
  }, [data]);

  return { chartData };
};
