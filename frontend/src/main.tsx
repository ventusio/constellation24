import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './index.css';

import L from 'leaflet';
import { DefaultIcon } from './components/icons/DefaultIcon';

L.Marker.prototype.options.icon = DefaultIcon;

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);