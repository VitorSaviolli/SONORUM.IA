import React, { useEffect, useRef, useState } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Camera, CameraOff } from 'lucide-react';

interface CameraFeedProps {
  onCameraStateChange?: (isActive: boolean) => void;
}

export function CameraFeed({ onCameraStateChange }: CameraFeedProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [isActive, setIsActive] = useState(false);
  const [error, setError] = useState<string>('');

  const startCamera = async () => {
    try {
      setError('');
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 },
        audio: false
      });
      
      setStream(mediaStream);
      setIsActive(true);
      onCameraStateChange?.(true);
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      setError('Erro ao acessar a câmera. Verifique as permissões.');
      console.error('Error accessing camera:', err);
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    } 
    setIsActive(false);
    onCameraStateChange?.(false);
    
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  };

  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [stream]);

  return (
    <Card className="p-6 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Câmera</h2>
        <Button
          onClick={isActive ? stopCamera : startCamera}
          variant={isActive ? "destructive" : "default"}
          size="sm"
        >
          {isActive ? (
            <>
              <CameraOff className="w-4 h-4 mr-2" />
              Parar
            </>
          ) : (
            <>
              <Camera className="w-4 h-4 mr-2" />
              Iniciar
            </>
          )}
        </Button>
      </div>

      <div className="flex-1 flex items-center justify-center bg-gray-100 rounded-lg overflow-hidden">
        {error ? (
          <div className="text-center p-8">
            <p className="text-red-600 mb-2">{error}</p>
            <Button onClick={startCamera} variant="outline">
              Tentar novamente
            </Button>
          </div>
        ) : isActive ? (
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="text-center p-8">
            <Camera className="w-16 h-16 mx-auto mb-4 text-gray-400" />
            <p className="text-gray-600 mb-4">
              Clique em "Iniciar" para ativar a câmera e começar a tocar violão
            </p>
          </div>
        )}
      </div>
    </Card>
  );
}