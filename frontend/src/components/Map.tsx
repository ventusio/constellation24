import { useEffect } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import 'leaflet.heat';
import { generateRandomPoints } from '../mock';

declare module 'leaflet' {
  export function heatLayer(latlngs: [number, number, number][], options?: {
    radius: number,
    blur: number,
    maxZoom: number,
    max: number,
    gradient: Record<number, string>
  }): {addTo: (map: L.Map) => L.Layer};
}

const HeatmapLayer = ({ data }: { data: [number, number, number][] }) => {
  const map = useMap();

  useEffect(() => {
    const heat = L.heatLayer(data, {
      radius: 25,
      blur: 15,
      maxZoom: 10,
      max: 1.0,
      gradient: { 0.4: 'blue', 0.65: 'lime', 1: 'red' }
    }).addTo(map);

    return () => {
      map.removeLayer(heat);
    };
  }, [map, data]);

  return null;
};

const heatmapData = generateRandomPoints(100, [-26.086233, 28.086953], 0.1);

const Map = () => {

  return (
    <MapContainer
      center={[-26.086233, 28.086953]}
      zoom={13}
      className="h-full w-full rounded-lg"
      style={{ height: "calc(100vh - 2rem)" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <HeatmapLayer data={heatmapData} />
    </MapContainer>
  );
};

export default Map;