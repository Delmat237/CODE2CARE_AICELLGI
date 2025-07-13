"use client";

import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Mic, MicOff, Play, Pause, Trash2 } from 'lucide-react';
import { useLanguage } from '@/lib/language-context';

interface VoiceRecorderProps {
  onRecordingComplete: (audioBlob: Blob) => void;
  maxDuration?: number; // in seconds
}

export function VoiceRecorder({ onRecordingComplete, maxDuration = 10 }: VoiceRecorderProps) {
  const { t } = useLanguage();
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 16000 // Lower sample rate for smaller file size
        } 
      });

      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus' // Efficient codec for low bandwidth
      });

      const chunks: Blob[] = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        setAudioBlob(blob);
        const url = URL.createObjectURL(blob);
        setAudioUrl(url);
        onRecordingComplete(blob);
        
        // Stop all tracks to release microphone
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setIsRecording(true);
      setRecordingTime(0);

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => {
          if (prev >= maxDuration) {
            stopRecording();
            return prev;
          }
          return prev + 1;
        });
      }, 1000);

    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Unable to access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    }
  };

  const playRecording = () => {
    if (audioUrl && !isPlaying) {
      const audio = new Audio(audioUrl);
      audioRef.current = audio;
      
      audio.onended = () => {
        setIsPlaying(false);
      };
      
      audio.play();
      setIsPlaying(true);
    } else if (audioRef.current && isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    }
  };

  const deleteRecording = () => {
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
    }
    setAudioBlob(null);
    setAudioUrl(null);
    setRecordingTime(0);
    setIsPlaying(false);
    
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <Card className="w-full">
      <CardContent className="p-4">
        <div className="flex flex-col items-center space-y-4">
          <div className="text-center">
            <h3 className="font-medium text-sm mb-1">{t('feedback.voice_note')}</h3>
            <p className="text-xs text-gray-500">
              {isRecording 
                ? `${t('button.recording')}... ${formatTime(recordingTime)}/${formatTime(maxDuration)}`
                : audioBlob 
                  ? `${t('common.recorded')} ${formatTime(recordingTime)}`
                  : `${t('common.max_duration')}: ${formatTime(maxDuration)}`
              }
            </p>
          </div>

          <div className="flex items-center space-x-2">
            {!audioBlob ? (
              <Button
                type="button"
                variant={isRecording ? "destructive" : "default"}
                size="sm"
                onClick={isRecording ? stopRecording : startRecording}
                className="flex items-center gap-2"
              >
                {isRecording ? (
                  <>
                    <MicOff className="h-4 w-4" />
                    {t('button.stop')}
                  </>
                ) : (
                  <>
                    <Mic className="h-4 w-4" />
                    {t('button.record')}
                  </>
                )}
              </Button>
            ) : (
              <>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={playRecording}
                  className="flex items-center gap-2"
                >
                  {isPlaying ? (
                    <>
                      <Pause className="h-4 w-4" />
                      {t('button.pause')}
                    </>
                  ) : (
                    <>
                      <Play className="h-4 w-4" />
                      {t('button.play')}
                    </>
                  )}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={deleteRecording}
                  className="flex items-center gap-2"
                >
                  <Trash2 className="h-4 w-4" />
                  {t('button.delete')}
                </Button>
                <Button
                  type="button"
                  variant="default"
                  size="sm"
                  onClick={startRecording}
                  className="flex items-center gap-2"
                >
                  <Mic className="h-4 w-4" />
                  {t('button.record_new')}
                </Button>
              </>
            )}
          </div>

          {isRecording && (
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-red-500 h-2 rounded-full transition-all duration-1000"
                style={{ width: `${(recordingTime / maxDuration) * 100}%` }}
              />
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}