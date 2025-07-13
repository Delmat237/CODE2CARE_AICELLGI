"use client";

import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { useLanguage } from '@/lib/language-context';

interface EmojiRatingProps {
  onRatingChange: (rating: string) => void;
  value?: string;
}

const emojiOptions = [
  { emoji: '😢', value: 'very_sad', label: 'Very Sad' },
  { emoji: '😞', value: 'sad', label: 'Sad' },
  { emoji: '😐', value: 'neutral', label: 'Neutral' },
  { emoji: '😊', value: 'happy', label: 'Happy' },
  { emoji: '😍', value: 'very_happy', label: 'Very Happy' }
];

export function EmojiRating({ onRatingChange, value }: EmojiRatingProps) {
  const { t } = useLanguage();
  const [selectedEmoji, setSelectedEmoji] = useState(value || '');

  const handleEmojiClick = (emojiValue: string) => {
    setSelectedEmoji(emojiValue);
    onRatingChange(emojiValue);
  };

  return (
    <Card className="w-full">
      <CardContent className="p-4">
        <div className="text-center mb-4">
          <h3 className="font-medium text-sm mb-1">{t('feedback.emoji_rating')}</h3>
        </div>
        
        <div className="flex justify-center space-x-2">
          {emojiOptions.map((option) => (
            <button
              key={option.value}
              type="button"
              onClick={() => handleEmojiClick(option.value)}
              className={`
                p-3 rounded-lg border-2 transition-all duration-200 hover:scale-110
                ${selectedEmoji === option.value 
                  ? 'border-blue-500 bg-blue-50 shadow-md' 
                  : 'border-gray-200 hover:border-gray-300'
                }
              `}
              title={option.label}
            >
              <span className="text-2xl">{option.emoji}</span>
            </button>
          ))}
        </div>
        
        {selectedEmoji && (
          <div className="text-center mt-3">
            <p className="text-sm text-gray-600">
              {t(`emoji.${selectedEmoji}`)}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}