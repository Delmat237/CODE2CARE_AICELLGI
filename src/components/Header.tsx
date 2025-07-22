// components/Header.tsx

import Image from 'next/image';

const TransparentHeader = () => {
  return (
    <header className="fixed top-0 left-0 w-full py-3 px-4 sm:px-8 md:px-12 lg:px-20 flex justify-between items-center bg-white bg-opacity-90 backdrop-blur-sm shadow-sm z-50 border-b border-gray-100">
      <div className="flex items-center space-x-3 sm:space-x-4">
        {/* Logo */}
        <div className="relative w-10 h-10 sm:w-12 sm:h-12">
          <Image
            src="/images/logo-hopital-douala.png"
            alt="Logo Hôpital Général de Douala"
            fill
            className="object-contain"
          />
        </div>
        
        <div>
          <h1 className="text-sm sm:text-base md:text-lg font-bold text-blue-800 tracking-tight">
            HÔPITAL GÉNÉRAL DE DOUALA
          </h1>
          <p className="text-xs sm:text-sm text-gray-700 mt-0.5">
            Assistant Médical Virtuel
          </p>
        </div>
      </div>

      {/* Badge d'assistance */}
      <div className="flex items-center">
        <span className="relative flex h-2 w-2 mr-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-red-600"></span>
        </span>
        <span className="text-xs sm:text-sm font-semibold text-red-600">
          Assistance 24/7
        </span>
      </div>
    </header>
  );
};

export default TransparentHeader;