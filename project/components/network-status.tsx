"use client";

import { useState, useEffect } from 'react';
import { Wifi, WifiOff, AlertCircle } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { networkManager } from '@/lib/network-utils';
import { useLanguage } from '@/lib/language-context';

export function NetworkStatus() {
  const { t } = useLanguage();
  const [isOnline, setIsOnline] = useState(true);
  const [connectionQuality, setConnectionQuality] = useState<'high' | 'medium' | 'low'>('high');
  const [showAlert, setShowAlert] = useState(false);

  useEffect(() => {
    const removeListener = networkManager.addListener((online) => {
      setIsOnline(online);
      setShowAlert(!online);
      
      if (online) {
        // Check connection quality when coming back online
        networkManager.checkConnectionQuality().then(setConnectionQuality);
        // Hide alert after 3 seconds when back online
        setTimeout(() => setShowAlert(false), 3000);
      }
    });

    // Initial connection quality check
    networkManager.checkConnectionQuality().then(setConnectionQuality);

    return removeListener;
  }, []);

  if (!showAlert && isOnline) return null;

  return (
    <div className="fixed top-4 right-4 z-50 max-w-sm">
      <Alert className={`${isOnline ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50'}`}>
        <div className="flex items-center gap-2">
          {isOnline ? (
            <Wifi className={`h-4 w-4 ${
              connectionQuality === 'high' ? 'text-green-600' :
              connectionQuality === 'medium' ? 'text-yellow-600' : 'text-red-600'
            }`} />
          ) : (
            <WifiOff className="h-4 w-4 text-red-600" />
          )}
          <AlertCircle className="h-4 w-4" />
        </div>
        <AlertDescription className="mt-2">
          {isOnline ? (
            <div>
              <p className="font-medium text-green-800">{t('network.back_online')}</p>
              <p className="text-sm text-green-700">
                {t('network.connection_quality')}: {t(`network.${connectionQuality}`)}
              </p>
            </div>
          ) : (
            <div>
              <p className="font-medium text-red-800">{t('network.offline')}</p>
              <p className="text-sm text-red-700">{t('message.offline')}</p>
            </div>
          )}
        </AlertDescription>
      </Alert>
    </div>
  );
}