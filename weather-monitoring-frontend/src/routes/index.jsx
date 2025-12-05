import React from 'react';
import { Dashboard } from '../components/Dashboard/Dashboard';

export const routes = [
  {
    path: '/',
    element: <Dashboard />,
  },
];

// Simple router component (no need for react-router for single page)
export const AppRouter = () => {
  return <Dashboard />;
};
