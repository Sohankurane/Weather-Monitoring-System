import React from 'react';
import { Dashboard } from '../components/Dashboard/Dashboard';

export const routes = [
  {
    path: '/',
    element: <Dashboard />,
  },
];

export const AppRouter = () => {
  return <Dashboard />;
};
