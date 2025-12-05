import { useState, useEffect } from 'react';
import { weatherAPI } from '../../services/api';
import { REFRESH_INTERVAL } from '../../constants';

export const useAlertsList = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const response = await weatherAPI.getAlerts();
      setAlerts(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
    
    // Auto-refresh every 5 minutes
    const interval = setInterval(fetchAlerts, REFRESH_INTERVAL);
    
    return () => clearInterval(interval);
  }, []);

  return {
    alerts,
    loading,
    error,
    refetch: fetchAlerts,
  };
};
