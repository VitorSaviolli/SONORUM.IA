import { useState } from 'react';
import { CameraFeed } from './components/CameraFeed';
import { NotesPanel } from './components/NotesPanel';

export default function App() {
  const [cameraActive, setCameraActive] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            SONORUM
          </h1>
          <p className="text-gray-600">
            Ative a câmera, toque seu violão e veja as notas sendo detectadas em tempo real
          </p>
        </div>

        {/* Main Content */}
        <div className="flex gap-4 h-[calc(100vh-150px)]">
          {/* Camera Feed - Maior espaço */}
          <div className="flex-1" style={{width: '75%'}}>
            <CameraFeed onCameraStateChange={setCameraActive} />
          </div>

          {/* Notes Panel - Menor espaço */}
          <div className="flex-shrink-0" style={{width: '25%'}}>
            <NotesPanel cameraActive={cameraActive} />
          </div>
        </div>


      </div>
    </div>
  );
}