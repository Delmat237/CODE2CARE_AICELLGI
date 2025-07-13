import { TranslationKey } from "./translations";

export interface PatientFeedback {
  id: number;
  patient_id?: string;
  patient_name: string;
  age: number;
  gender: string;
  phone_number?: string;
  condition: string;
  treatment_satisfaction: number;
  communication_rating: number;
  facility_rating: number;
  overall_experience: number;
  recommendation_likelihood: number;
  feedback_date: string;
  comments: string;
  language: string;
  submission_method: 'web' | 'sms' | 'ussd' | 'ivr' | 'voice';
  sentiment?: 'positive' | 'negative' | 'neutral';
  audio_url?: string;
  emoji_rating?: string;
  is_synced: boolean;
}

export interface Language {
  code: string;
  name: string;
  nativeName: string;
}

export interface Translation {
  [key: string]: {
    [languageCode: string]: string;
  };
}

export interface ReminderSettings {
  id: string;
  patient_id: string;
  reminder_type: 'sms' | 'call' | 'email';
  message: string;
  scheduled_time: string;
  language: string;
  status: 'pending' | 'sent' | 'failed';
}

