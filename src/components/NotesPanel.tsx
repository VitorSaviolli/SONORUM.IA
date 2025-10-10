import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Music, RotateCcw } from 'lucide-react';

interface Note {
  id: string;
  name: string;
  fullName: string;
  detected: boolean;
  lastDetected?: Date;
}

interface NotesPanelProps {
  cameraActive: boolean;
}

const initialNotes: Note[] = [
  { id: 'C', name: 'C', fullName: 'Dó maior', detected: false },
  { id: 'D', name: 'D', fullName: 'Ré maior', detected: false },
  { id: 'A', name: 'A', fullName: 'Lá maior', detected: false },
  { id: 'E', name: 'E', fullName: 'Mi maior', detected: false },
  { id: 'G', name: 'G', fullName: 'Sol maior', detected: false },
  { id: 'F', name: 'F', fullName: 'Fá maior', detected: false },
];

export function NotesPanel({ cameraActive }: NotesPanelProps) {
  const [notes, setNotes] = useState<Note[]>(initialNotes);
  const [recentlyDetected, setRecentlyDetected] = useState<string[]>([]);

  // Simula detecção de notas quando a câmera está ativa
  useEffect(() => {
    if (!cameraActive) return;

    const interval = setInterval(() => {
      // Simula detecção aleatória de notas
      if (Math.random() > 0.7) {
        const randomNote = initialNotes[Math.floor(Math.random() * initialNotes.length)];
        
        setNotes(prev => prev.map(note => 
          note.id === randomNote.id 
            ? { ...note, detected: true, lastDetected: new Date() }
            : note
        ));

        setRecentlyDetected(prev => {
          const updated = [randomNote.id, ...prev.filter(id => id !== randomNote.id)].slice(0, 3);
          return updated;
        });

        // Remove a detecção após 2 segundos
        setTimeout(() => {
          setNotes(prev => prev.map(note => 
            note.id === randomNote.id 
              ? { ...note, detected: false }
              : note
          ));
        }, 2000);
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [cameraActive]);

  const resetDetection = () => {
    setNotes(initialNotes);
    setRecentlyDetected([]);
  };

  const handleNoteClick = (noteId: string) => {
    // Permite ativação manual para demonstração
    setNotes(prev => prev.map(note => 
      note.id === noteId 
        ? { ...note, detected: !note.detected, lastDetected: new Date() }
        : note
    ));

    if (!notes.find(n => n.id === noteId)?.detected) {
      setRecentlyDetected(prev => {
        const updated = [noteId, ...prev.filter(id => id !== noteId)].slice(0, 3);
        return updated;
      });
    }
  };

  return (
    <Card className="p-4 h-full bg-white shadow-lg flex flex-col" style={{border: '3px solid #3b82f6'}}>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <Music className="w-5 h-5 text-blue-600" />
          <h2 className="font-semibold">Notas</h2>
        </div>
        <Button
          onClick={resetDetection}
          variant="outline"
          size="sm"
        >
          <RotateCcw className="w-3 h-3" />
        </Button>
      </div>

      <Badge 
        variant={cameraActive ? "default" : "secondary"}
        className="w-full justify-center py-2 mb-1"
      >
        {cameraActive ? "🎵 Detectando..." : "📷 Câmera desligada"}
      </Badge>

      <div className="flex-1 overflow-hidden">
        <h3 className="text-sm font-medium mb-2 text-gray-600">Todas as Notas</h3>
        <div className="grid gap-2 overflow-y-auto max-h-48">
          {notes.map((note) => (
            <Button
              key={note.id}
              variant={note.detected ? "default" : "outline"}
              className={`p-2 h-auto justify-between transition-all text-left text-xs ${
                note.detected ? 'bg-green-600 hover:bg-green-700 shadow-md' : 'hover:bg-gray-50'
              }`}
              onClick={() => handleNoteClick(note.id)}
            >
              <div className="flex items-center gap-2 w-full">
                <div className="flex-1">
                  <div className="font-semibold text-xs">{note.name}</div>
                  <div className="text-xs opacity-75">{note.fullName}</div>
                </div>
                {note.detected && (
                  <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
                )}
              </div>
            </Button>
          ))}
        </div>
      </div>

     {/*  <div className="mt-2 p-2 bg-blue-50 rounded-lg text-xs text-blue-700">
        <p className="font-medium mb-1">💡 Dica:</p>
        <p>Clique nas notas para simular detecção ou use a câmera para detecção automática.</p>
      </div> */}
    </Card>
  );
}