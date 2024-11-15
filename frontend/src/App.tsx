import { QueryClient, QueryClientProvider } from 'react-query';
import Map from './components/Map';
import ChatBot from './components/ChatBot';
import ReportButton from './components/ReportButton';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-100 p-4">
        <div className='relative'>
          <div className='absolute top-2 right-2 z-50'>
            <ReportButton />
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 h-[calc(100vh-2rem)]">
          <div className="lg:col-span-3 bg-white rounded-lg shadow-lg overflow-hidden">
            <Map />
          </div>
          <div className="lg:col-span-1">
            <ChatBot />
          </div>
        </div>
      </div>
    </QueryClientProvider>
  );
}

export default App;