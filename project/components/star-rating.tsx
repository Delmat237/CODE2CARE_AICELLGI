"use client";

import { useState } from 'react';
import { Star } from 'lucide-react';

interface StarRatingProps {
  value: number;
  onChange: (rating: number) => void;
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  readonly?: boolean;
}

export function StarRating({ value, onChange, max = 5, size = 'md', readonly = false }: StarRatingProps) {
  const [hoverValue, setHoverValue] = useState(0);

  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8'
  };

  const handleClick = (rating: number) => {
    if (!readonly) {
      onChange(rating);
    }
  };

  const handleMouseEnter = (rating: number) => {
    if (!readonly) {
      setHoverValue(rating);
    }
  };

  const handleMouseLeave = () => {
    if (!readonly) {
      setHoverValue(0);
    }
  };

  return (
    <div className="flex items-center space-x-1">
      {Array.from({ length: max }, (_, index) => {
        const starValue = index + 1;
        const isActive = starValue <= (hoverValue || value);
        
        return (
          <button
            key={index}
            type="button"
            onClick={() => handleClick(starValue)}
            onMouseEnter={() => handleMouseEnter(starValue)}
            onMouseLeave={handleMouseLeave}
            disabled={readonly}
            className={`
              transition-all duration-200 
              ${readonly ? 'cursor-default' : 'cursor-pointer hover:scale-110'}
              ${isActive ? 'text-yellow-400' : 'text-gray-300'}
            `}
          >
            <Star 
              className={`${sizeClasses[size]} ${isActive ? 'fill-current' : ''}`}
            />
          </button>
        );
      })}
      <span className="ml-2 text-sm text-gray-600">
        {value}/{max}
      </span>
    </div>
  );
}