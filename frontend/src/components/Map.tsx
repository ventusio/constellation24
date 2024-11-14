import { useEffect } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import 'leaflet.heat';
import { generateRandomPoints } from '../mock';
import { useQuery } from 'react-query';

const API_BASE_URL ='http://localhost:8000'

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

  const { data: reports, isLoading, error } = useQuery('reports', async () => {
    const response = await fetch(`${API_BASE_URL}/reports`);
    if (!response.ok) {
      console.log(response)
      throw new Error('Network response was not ok');
    }
    return response.json();
  });
  
  if (isLoading) return <div className="flex items-center justify-center h-screen">Loading...</div>;
  
  if (error) return <div className="flex items-center justify-center h-screen text-red-500">Something went wrong</div>;
  
  console.log(reports)

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