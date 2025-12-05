import { useState, useEffect } from 'react';
import { weatherAPI } from '../../services/api';
import { REFRESH_INTERVAL } from '../../constants';

export const useDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await weatherAPI.getDashboardData();
      setDashboardData(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    
    // Auto-refresh every 5 minutes
    const interval = setInterval(fetchDashboardData, REFRESH_INTERVAL);
    
    return () => clearInterval(interval);
  }, []);

  return {
    dashboardData,
    loading,
    error,
    refetch: fetchDashboardData,
  };
};
