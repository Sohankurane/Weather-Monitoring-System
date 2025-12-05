import React from 'react';
import { useAlertsList } from './AlertsList.hook';
import { ALERT_TYPES } from '../../constants';
import './AlertsList.css';

export const AlertsList = () => {
  const { alerts, loading, error } = useAlertsList();

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleString('en-IN', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="alerts-container">
      <div className="alerts-header">
        <h3>⚠️ Weather Alerts</h3>
        <span className="alert-count">{alerts.length} alerts</span>
      </div>

      {loading && alerts.length === 0 && (
        <div className="alerts-loading">
          <div className="spinner-small"></div>
          <p>Loading alerts...</p>
        </div>
      )}

      {error && alerts.length === 0 && (
        <div className="alerts-error">
          <p>Failed to load alerts</p>
        </div>
      )}

      {alerts.length === 0 && !loading && !error && (
        <div className="no-alerts">
          <span className="no-alerts-icon">✅</span>
          <p>No weather alerts at the moment</p>
          <small>All conditions are normal</small>
        </div>
      )}

      <div className="alerts-list">
        {alerts.map((alert) => {
          const alertConfig = ALERT_TYPES[alert.alert_type] || {
            label: alert.alert_type,
            color: '#6b7280',
            icon: '⚠️',
          };

          return (
            <div
              key={alert.id}
              className="alert-item"
              style={{ borderLeftColor: alertConfig.color }}
            >
              <div className="alert-icon" style={{ background: alertConfig.color }}>
                {alertConfig.icon}
              </div>
              <div className="alert-content">
                <div className="alert-header-row">
                  <span className="alert-type">{alertConfig.label}</span>
                  <span className="alert-time">{formatTime(alert.created_at)}</span>
                </div>
                <p className="alert-message">{alert.message}</p>
                {alert.threshold_value && (
                  <div className="alert-values">
                    <span>Threshold: {alert.threshold_value}</span>
                    <span>Actual: {alert.actual_value}</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
