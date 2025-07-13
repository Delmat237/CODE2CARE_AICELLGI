"use client";

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { useLanguage } from '@/lib/language-context';
import { StarRating } from './star-rating';
import { VoiceRecorder } from './voice-recorder';
import { EmojiRating } from './emoji-rating';
import { NetworkStatus } from './network-status';
import { offlineStorage } from '@/lib/offline-storage';
import { networkManager } from '@/lib/network-utils';
import { PatientFeedback } from '@/lib/types';
import { Heart, Send, CheckCircle } from 'lucide-react';

const medicalConditions = [
  'Hypertension', 'Diabète', 'Migraine', 'Arthrite', 'Anxiété', 
  'Asthme', 'Dépression', 'Infection', 'Blessure', 'Autre'
];

export function FeedbackForm() {
  const { t, currentLanguage } = useLanguage();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  
  const [formData, setFormData] = useState({
    patient_name: '',
    age: '',
    gender: '',
    phone_number: '',
    condition: '',
    treatment_satisfaction: 0,
    communication_rating: 0,
    facility_rating: 0,
    overall_experience: 0,
    recommendation_likelihood: [5],
    comments: '',
    emoji_rating: ''
  });

  useEffect(() => {
    // Initialize offline storage
    offlineStorage.init();
  }, []);

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleAudioRecording = (blob: Blob) => {
    setAudioBlob(blob);
  };

  const validateForm = () => {
    const required = ['patient_name', 'age', 'gender', 'condition'];
    const ratings = ['treatment_satisfaction', 'communication_rating', 'facility_rating', 'overall_experience'];
    
    // Check required fields
    for (const field of required) {
      if (!formData[field as keyof typeof formData]) {
        return false;
      }
    }
    
    // Check at least one rating is provided
    for (const rating of ratings) {
      const value = formData[rating as keyof typeof formData];

      if (typeof value === "number" && value > 0) {
        return true;
      }
    }
    
    return false;
  };

  const submitFeedback = async (feedbackData: PatientFeedback) => {
    try {
      const response = await networkManager.makeRequest('/api/feedback', {
        method: 'POST',
        body: networkManager.compressData(feedbackData)
      });
      
      if (response.ok) {
        return await response.json();
      } else {
        throw new Error('Failed to submit feedback');
      }
    } catch (error) {
      console.error('Submission error:', error);
      throw error;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      alert(t('message.validation_error'));
      return;
    }

    setIsSubmitting(true);

    try {
      const feedbackData: PatientFeedback = {
        id: Date.now(), // Temporary ID
        patient_name: formData.patient_name,
        age: parseInt(formData.age),
        gender: formData.gender,
        phone_number: formData.phone_number || undefined,
        condition: formData.condition,
        treatment_satisfaction: formData.treatment_satisfaction,
        communication_rating: formData.communication_rating,
        facility_rating: formData.facility_rating,
        overall_experience: formData.overall_experience,
        recommendation_likelihood: formData.recommendation_likelihood[0],
        feedback_date: new Date().toISOString().split('T')[0],
        comments: formData.comments,
        language: currentLanguage,
        submission_method: 'web',
        emoji_rating: formData.emoji_rating,
        is_synced: false
      };

      if (networkManager.getConnectionStatus()) {
        // Try to submit online
        try {
          const result = await submitFeedback(feedbackData);
          feedbackData.id = result.id;
          feedbackData.is_synced = true;
          
          // Save audio if available
          if (audioBlob) {
            // In a real implementation, you would upload the audio file
            console.log('Audio recording saved locally');
          }
          
          setIsSubmitted(true);
        } catch (error) {
          // If online submission fails, save offline
          await saveOffline(feedbackData);
        }
      } else {
        // Save offline
        await saveOffline(feedbackData);
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert(t('message.error'));
    } finally {
      setIsSubmitting(false);
    }
  };

  const saveOffline = async (feedbackData: PatientFeedback) => {
    try {
      const id = await offlineStorage.saveFeedback(feedbackData);
      
      if (audioBlob) {
        await offlineStorage.saveAudioRecording(id, audioBlob);
      }
      
      setIsSubmitted(true);
      
      // Add to retry queue for when connection is restored
      networkManager.addToRetryQueue(async () => {
        const result = await submitFeedback(feedbackData);
        await offlineStorage.markAsSynced(id);
      });
    } catch (error) {
      console.error('Error saving offline:', error);
      alert(t('message.error'));
    }
  };

  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
        <Card className="w-full max-w-md text-center">
          <CardContent className="p-8">
            <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-green-800 mb-2">
              {t('message.success_title')}
            </h2>
            <p className="text-green-700 mb-6">
              {t('message.success')}
            </p>
            <Button 
              onClick={() => {
                setIsSubmitted(false);
                setFormData({
                  patient_name: '',
                  age: '',
                  gender: '',
                  phone_number: '',
                  condition: '',
                  treatment_satisfaction: 0,
                  communication_rating: 0,
                  facility_rating: 0,
                  overall_experience: 0,
                  recommendation_likelihood: [5],
                  comments: '',
                  emoji_rating: ''
                });
                setAudioBlob(null);
              }}
              className="w-full"
            >
              {t('button.submit_another')}
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <NetworkStatus />
      
      <div className="container mx-auto max-w-2xl">
        <Card className="shadow-xl">
          <CardHeader className="text-center bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-t-lg">
            <div className="flex items-center justify-center gap-2 mb-2">
              <Heart className="h-6 w-6" />
              <CardTitle className="text-2xl">{t('feedback.title')}</CardTitle>
            </div>
            <CardDescription className="text-blue-100">
              {t('feedback.subtitle')}
            </CardDescription>
          </CardHeader>
          
          <CardContent className="p-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Patient Information */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="patient_name">{t('feedback.patient_name')} *</Label>
                  <Input
                    id="patient_name"
                    value={formData.patient_name}
                    onChange={(e) => handleInputChange('patient_name', e.target.value)}
                    required
                    className="mt-1"
                  />
                </div>
                
                <div>
                  <Label htmlFor="age">{t('feedback.age')} *</Label>
                  <Input
                    id="age"
                    type="number"
                    min="1"
                    max="120"
                    value={formData.age}
                    onChange={(e) => handleInputChange('age', e.target.value)}
                    required
                    className="mt-1"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="gender">{t('feedback.gender')} *</Label>
                  <Select value={formData.gender} onValueChange={(value) => handleInputChange('gender', value)}>
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder={t('feedback.select_gender')} />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="male">{t('feedback.male')}</SelectItem>
                      <SelectItem value="female">{t('feedback.female')}</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="phone">{t('feedback.phone')}</Label>
                  <Input
                    id="phone"
                    type="tel"
                    value={formData.phone_number}
                    onChange={(e) => handleInputChange('phone_number', e.target.value)}
                    placeholder="+237 6XX XXX XXX"
                    className="mt-1"
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="condition">{t('feedback.condition')} *</Label>
                <Select value={formData.condition} onValueChange={(value) => handleInputChange('condition', value)}>
                  <SelectTrigger className="mt-1">
                    <SelectValue placeholder={t('feedback.select_condition')} />
                  </SelectTrigger>
                  <SelectContent>
                    {medicalConditions.map((condition) => (
                      <SelectItem key={condition} value={condition}>
                        {condition}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Ratings */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">{t('feedback.ratings_title')}</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <Label>{t('rating.treatment')}</Label>
                    <div className="mt-2">
                      <StarRating
                        value={formData.treatment_satisfaction}
                        onChange={(rating) => handleInputChange('treatment_satisfaction', rating)}
                      />
                    </div>
                  </div>

                  <div>
                    <Label>{t('rating.communication')}</Label>
                    <div className="mt-2">
                      <StarRating
                        value={formData.communication_rating}
                        onChange={(rating) => handleInputChange('communication_rating', rating)}
                      />
                    </div>
                  </div>

                  <div>
                    <Label>{t('rating.facility')}</Label>
                    <div className="mt-2">
                      <StarRating
                        value={formData.facility_rating}
                        onChange={(rating) => handleInputChange('facility_rating', rating)}
                      />
                    </div>
                  </div>

                  <div>
                    <Label>{t('rating.overall')}</Label>
                    <div className="mt-2">
                      <StarRating
                        value={formData.overall_experience}
                        onChange={(rating) => handleInputChange('overall_experience', rating)}
                      />
                    </div>
                  </div>
                </div>

                <div>
                  <Label>{t('rating.recommendation')}</Label>
                  <div className="mt-2 px-3">
                    <Slider
                      value={formData.recommendation_likelihood}
                      onValueChange={(value) => handleInputChange('recommendation_likelihood', value)}
                      max={10}
                      min={0}
                      step={1}
                      className="w-full"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>0</span>
                      <span className="font-medium">{formData.recommendation_likelihood[0]}</span>
                      <span>10</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Emoji Rating */}
              <EmojiRating
                value={formData.emoji_rating}
                onRatingChange={(rating) => handleInputChange('emoji_rating', rating)}
              />

              {/* Comments */}
              <div>
                <Label htmlFor="comments">{t('feedback.comments')}</Label>
                <Textarea
                  id="comments"
                  value={formData.comments}
                  onChange={(e) => handleInputChange('comments', e.target.value)}
                  placeholder={t('feedback.comments_placeholder')}
                  rows={4}
                  className="mt-1"
                />
              </div>

              {/* Voice Recording */}
              <VoiceRecorder onRecordingComplete={handleAudioRecording} />

              {/* Submit Button */}
              <Button
                type="submit"
                disabled={isSubmitting || !validateForm()}
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
              >
                {isSubmitting ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    {t('button.submitting')}
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <Send className="h-4 w-4" />
                    {t('button.submit')}
                  </div>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}