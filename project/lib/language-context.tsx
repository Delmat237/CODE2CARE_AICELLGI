"use client";

import React, { createContext, useContext, useState, useEffect } from 'react';
import { translations, languages, TranslationKey, LanguageCode } from './translations';

interface LanguageContextType {
  currentLanguage: string;
  setLanguage: (lang: string) => void;
  t: (key: string) => string; // Gardez string pour l'interface publique
  languages: typeof languages;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [currentLanguage, setCurrentLanguage] = useState<LanguageCode>('en'); // Typé comme LanguageCode

  useEffect(() => {
    const savedLanguage = localStorage.getItem('dgh-language');
    const browserLanguage = navigator.language.split('-')[0];
    
    if (savedLanguage && languages.find(l => l.code === savedLanguage)) {
      setCurrentLanguage(savedLanguage as LanguageCode);
    } else if (languages.find(l => l.code === browserLanguage)) {
      setCurrentLanguage(browserLanguage as LanguageCode);
    }
  }, []);

  const setLanguage = (lang: string) => {
    if (languages.some(l => l.code === lang)) {
      setCurrentLanguage(lang as LanguageCode);
      localStorage.setItem('dgh-language', lang);
    }
  };

  // Implémentation interne stricte
  const tInternal = (key: TranslationKey): string => {
    const translation = translations[key];
    return translation[currentLanguage] || translation.en || key;
  };

  // Fonction publique qui accepte string
  const t = (key: string): string => {
    if (key in translations) {
      return tInternal(key as TranslationKey);
    }
    return key; // Fallback pour les clés invalides
  };

  return (
    <LanguageContext.Provider value={{ currentLanguage, setLanguage, t, languages }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}