import { useEffect, useMemo } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import 'leaflet.heat';
import { useQuery } from 'react-query';
import { env } from '../env';

declare module 'leaflet' {
  export function heatLayer(latlngs: [number, number, number][], options?: {
    radius: number,
    blur: number,
    maxZoom: number,
    max: number,
    gradient: Record<number, string>
  }): {addTo: (map: L.Map) => L.Layer};
}

interface Report {
  id: number
  location: L.LatLng
  timestamp: string
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

const Map = () => {
  const { data: reports, isLoading, error } = useQuery<Report[]>('reports', async () => {
    const response = await fetch(`${env.API_BASE_URL}/reports`);
    if (!response.ok) {
      console.log(response)
      throw new Error('Network response was not ok');
    }
    return response.json();
  });

  const heatmapData = useMemo(() => {
    return reports?.map(r => [r.location.lat, r.location.lng, 0.8]) as [number,number,number][]
  },[reports])
  
  if (isLoading) return <div className="flex items-center justify-center h-screen">Loading...</div>;
  
  if (error) return <div className="flex items-center justify-center h-screen text-red-500">Something went wrong</div>;

  return (
    <MapContainer
      center={[-26.086233, 28.086953]}
      zoom={13}
      className="h-full w-full rounded-lg"
      style={{ height: "calc(100vh - 2rem)", zIndex: 1 }}
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