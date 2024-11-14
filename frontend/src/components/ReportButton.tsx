import React, { useState } from 'react';
import { useMutation, useQueryClient } from 'react-query';
import { env } from '../env';

const ReportButton: React.FC = () => {
  const queryClient = useQueryClient()
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState<{ lat: number, lng: number }>({
    lat: -26.086233,
    lng: 28.086953
  });

  const {mutate: submitReport} = useMutation((newReport: { lat: number, lng: number, description: string }) =>
    fetch(`${env.API_BASE_URL}/report`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newReport),
    }), {onSettled: () => {
      queryClient.invalidateQueries('reports')
    }}
  );

  const openModal = () => {
    setIsModalOpen(true);

    // mocking the location in case the browser's geolocation does not work. This is for the demo
    setLocation(loc => ({
      lat: loc.lat + (Math.random() - 0.5) / 20,
      lng: loc.lng
    }));

    navigator.geolocation.getCurrentPosition((position) => {
      setLocation({
        lat: position.coords.latitude,
        lng: position.coords.longitude
      });
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (location) {
      submitReport({
        lat: location.lat,
        lng: location.lng,
        description
      });
    }
    setIsModalOpen(false);
    setDescription('');
  };

  return (
    <>
      <button onClick={openModal} className="bg-blue-500 text-white px-4 py-2 rounded">
        Report incident
      </button>
      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75">
          <div className="bg-white p-6 rounded shadow-lg">
            <h2 className="text-xl font-bold mb-4">Report Incident</h2>
            <p className="mb-4">Please provide a description of the incident you are reporting.</p>
            <form onSubmit={handleSubmit}>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe the incident"
                autoFocus
                required
                className="w-full p-2 border border-gray-300 rounded mb-4"
                style={{ height: '150px' }}
              />
              <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
                Submit
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  );
};

export default ReportButton;
