import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Send, User, Bot, Languages, Settings, Trash2, Plus,
  History, AlertTriangle, Wifi, WifiOff, Crosshair,
  Thermometer, HeartPulse, Pill, Activity, Brain, Shield,
  Globe, Clock, Zap, ChevronDown, ChevronUp, Loader2,
  MessageCircle
} from 'lucide-react';
import TransparentHeader from './components/Header';

// Types et interfaces
type MessageRole = 'user' | 'assistant';
type ConnectionStatus = 'online' | 'offline' | 'checking';

interface Message {
  id: string;
  content: string;
  role: MessageRole;
  timestamp: Date;
  language: string;
  isEmergency?: boolean;
  isOffline?: boolean;
}

interface UserProfile {
  name: string;
  age: number;
  gender: string;
  location: string;
  medicalHistory: string;
}

interface ChatResponse {
  response: string;
  session_id: string;
  language: string;
  confidence: number;
  suggestions: string[];
  isEmergency?: boolean;
}

// Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const OFFLINE_TIMEOUT = 5000; // 5 secondes pour le timeout API

const SUPPORTED_LANGUAGES = [
  { code: 'fr', name: 'Français', icon: '🇫🇷' },
  { code: 'en', name: 'English', icon: '🇬🇧' },
  { code: 'wo', name: 'Wolof', icon: '🇸🇳' },
  { code: 'ha', name: 'Hausa', icon: '🇳🇬' },
  { code: 'sw', name: 'Swahili', icon: '🇰🇪' }
];

const OFFLINE_RESPONSES: Record<string, string> = {
  'fièvre': "Pour une fièvre :\n1. Reposez-vous dans un endroit frais\n2. Hydratez-vous abondamment\n3. Prenez un antipyrétique si nécessaire\n\nConsultez si >39°C ou persiste >3 jours.",
  'mal de tête': "Pour un mal de tête :\n1. Repos dans un endroit calme\n2. Hydratation\n3. Analgésique léger si nécessaire\n\nConsultez si sévère ou persistant.",
  'toux': "Pour une toux :\n1. Boissons chaudes au miel\n2. Évitez les irritants\n3. Humidifiez l'air\n\nConsultez si persiste >1 semaine ou avec fièvre.",
  'diarrhée': "Pour une diarrhée :\n1. Solution de réhydratation\n2. Évitez lait et fibres\n3. Repos intestinal\n\nConsultez si sang ou persiste >2 jours.",
  'urgence': "⚠️ URGENCE MÉDICALE ⚠️\n\n1. Composez le 15 (SAMU)\n2. Restez calme\n3. Suivez les instructions\n\nNe prenez pas de médicaments sans avis médical.",
  'default': "Je suis en mode hors ligne. Mes réponses sont limitées.\n\nPour des conseils précis :\n1. Connectez-vous à internet\n2. Contactez un professionnel de santé\n3. En urgence, composez le 15"
};

const QUICK_ACTIONS = [
  { icon: <Thermometer size={18} />, label: "Symptômes", keywords: ['fièvre', 'douleur', 'toux'] },
  { icon: <Pill size={18} />, label: "Médicaments", keywords: ['paracétamol', 'ibuprofène', 'traitement'] },
  { icon: <HeartPulse size={18} />, label: "Premiers soins", keywords: ['blessure', 'brûlure', 'saignement'] },
  { icon: <Activity size={18} />, label: "Maladies", keywords: ['paludisme', 'typhoïde', 'infection'] },
  { icon: <Brain size={18} />, label: "Santé mentale", keywords: ['stress', 'anxiété', 'dépression'] }
];

// Composant principal
const App: React.FC = () => {
  // États
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('fr');
  const [sessionId] = useState(() => crypto.randomUUID());
  const [showSidebar, setShowSidebar] = useState(true);
  const [userProfile, setUserProfile] = useState<UserProfile>({
    name: '',
    age: 30,
    gender: 'Non spécifié',
    location: '',
    medicalHistory: ''
  });
  const [activeTab, setActiveTab] = useState<'chat' | 'resources' | 'emergency'>('chat');
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('checking');
  const [apiHealthy, setApiHealthy] = useState(false);
  const [showLanguageDropdown, setShowLanguageDropdown] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Vérification de la connexion et santé API
  const checkConnection = useCallback(async () => {
    const online = navigator.onLine;
    setConnectionStatus(online ? 'online' : 'offline');
    
    if (online) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), OFFLINE_TIMEOUT);
        
        const response = await fetch(`${API_BASE_URL}/health`, {
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        setApiHealthy(response.ok);
      } catch (error) {
        setApiHealthy(false);
      }
    } else {
      setApiHealthy(false);
    }
  }, []);

  // Effets
  useEffect(() => {
    const handleOnline = () => checkConnection();
    const handleOffline = () => {
      setConnectionStatus('offline');
      setApiHealthy(false);
    };

    // Vérification initiale
    checkConnection();

    // Écouteurs d'événements
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Vérification périodique (toutes les 2 minutes)
    const intervalId = setInterval(checkConnection, 120000);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      clearInterval(intervalId);
    };
  }, [checkConnection]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Fonctions utilitaires
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat('fr-FR', {
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  // Gestion des messages
  const generateOfflineResponse = (messageText: string): string => {
    const lowerCaseMessage = messageText.toLowerCase();
    
    // Détection d'urgence
    if (/(urgence|emergency|15|18|112)/i.test(lowerCaseMessage)) {
      return OFFLINE_RESPONSES['urgence'];
    }
    
    // Recherche par mot-clé
    for (const [keyword, response] of Object.entries(OFFLINE_RESPONSES)) {
      if (keyword !== 'default' && new RegExp(keyword, 'i').test(lowerCaseMessage)) {
        return response;
      }
    }
    
    return OFFLINE_RESPONSES['default'];
  };

  const sendMessageToApi = async (messageText: string): Promise<ChatResponse> => {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), OFFLINE_TIMEOUT);

      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('med_token')}`
        },
        body: JSON.stringify({
          message: messageText,
          language: selectedLanguage,
          session_id: sessionId,
          user_context: {
            ...userProfile,
            connection_status: connectionStatus
          }
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API call failed:', error);
      throw error;
    }
  };

  const handleSendMessage = async (messageText: string) => {
    if (!messageText.trim()) return;

    // Ajout du message utilisateur
    const userMessage: Message = {
      id: crypto.randomUUID(),
      content: messageText,
      role: 'user',
      timestamp: new Date(),
      language: selectedLanguage
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setInputMessage('');

    try {
      let botMessage: Message;

      if (connectionStatus === 'online' && apiHealthy) {
        // Mode en ligne - Appel API
        const apiResponse = await sendMessageToApi(messageText);
        
        botMessage = {
          id: crypto.randomUUID(),
          content: apiResponse.response,
          role: 'assistant',
          timestamp: new Date(),
          language: apiResponse.language,
          isEmergency: apiResponse.isEmergency
        };
      } else {
        // Mode hors ligne
        await new Promise(resolve => setTimeout(resolve, 800)); // Simulation délai
        const responseText = generateOfflineResponse(messageText);
        
        botMessage = {
          id: crypto.randomUUID(),
          content: responseText,
          role: 'assistant',
          timestamp: new Date(),
          language: selectedLanguage,
          isOffline: true,
          isEmergency: /urgence/i.test(messageText)
        };
      }

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: crypto.randomUUID(),
        content: "Désolé, une erreur s'est produite. Veuillez réessayer.",
        role: 'assistant',
        timestamp: new Date(),
        language: selectedLanguage,
        isOffline: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSendMessage(inputMessage);
  };

  const handleQuickAction = (keywords: string[]) => {
    const randomKeyword = keywords[Math.floor(Math.random() * keywords.length)];
    handleSendMessage(`Je cherche des informations sur ${randomKeyword}`);
  };

  const clearConversation = () => {
    setMessages([]);
  };

  // Rendu
  return (
    <div className="flex h-screen bg-gray-50 text-gray-900">
      
      {/* Sidebar */}
      <div className={`${showSidebar ? 'translate-x-0' : '-translate-x-full'} 
        fixed lg:relative z-20 w-72 h-full bg-white shadow-xl transition-transform duration-300 ease-in-out flex flex-col`}>
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold flex items-center">
              <MessageCircle className="h-5 w-5 mr-2 text-green-600" />
              <span>Assistant Médical</span>
            </h2>
            <button 
              onClick={() => setShowSidebar(false)}
              className="p-1 rounded-lg hover:bg-gray-100 lg:hidden"
            >
              <Crosshair className="h-4 w-4 text-gray-500" />
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4">
          <div className="space-y-6">
            {/* Statut de connexion */}
            <div className={`p-3 rounded-lg flex items-start ${
              connectionStatus === 'online' && apiHealthy
                ? 'bg-green-50 text-green-800'
                : 'bg-yellow-50 text-yellow-800'
            }`}>
              <div className="mr-2 mt-0.5">
                {connectionStatus === 'online' && apiHealthy ? (
                  <Wifi className="h-4 w-4" />
                ) : (
                  <WifiOff className="h-4 w-4" />
                )}
              </div>
              <div>
                <p className="font-medium">
                  {connectionStatus === 'online'
                    ? apiHealthy
                      ? 'Connecté au serveur médical'
                      : 'Serveur indisponible'
                    : 'Mode hors ligne'}
                </p>
                <p className="text-xs mt-1">
                  {connectionStatus === 'online' && apiHealthy
                    ? 'Conseils médicaux complets disponibles'
                    : 'Fonctionnalités limitées - certaines réponses peuvent être génériques'}
                </p>
              </div>
            </div>

            {/* Nouvelle conversation */}
            <div className="space-y-2">
              <button
                onClick={clearConversation}
                className="w-full flex items-center justify-center space-x-2 bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 transition-colors"
              >
                <Plus className="h-4 w-4" />
                <span>Nouvelle conversation</span>
              </button>
            </div>

            {/* Profil médical */}
            <div className="space-y-3">
              <h3 className="font-medium text-sm text-gray-500">PROFIL MÉDICAL</h3>
              <div className="space-y-3">
                <div>
                  <label className="block text-xs text-gray-500 mb-1">Nom complet</label>
                  <input
                    type="text"
                    value={userProfile.name}
                    onChange={(e) => setUserProfile({...userProfile, name: e.target.value})}
                    className="w-full p-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="Votre nom"
                  />
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block text-xs text-gray-500 mb-1">Âge</label>
                    <input
                      type="number"
                      value={userProfile.age}
                      onChange={(e) => setUserProfile({...userProfile, age: parseInt(e.target.value) || 0})}
                      className="w-full p-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      min="0"
                      max="120"
                    />
                  </div>
                  <div>
                    <label className="block text-xs text-gray-500 mb-1">Sexe</label>
                    <select
                      value={userProfile.gender}
                      onChange={(e) => setUserProfile({...userProfile, gender: e.target.value})}
                      className="w-full p-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    >
                      <option value="Non spécifié">Non spécifié</option>
                      <option value="Homme">Homme</option>
                      <option value="Femme">Femme</option>
                      <option value="Autre">Autre</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-xs text-gray-500 mb-1">Localisation</label>
                  <input
                    type="text"
                    value={userProfile.location}
                    onChange={(e) => setUserProfile({...userProfile, location: e.target.value})}
                    className="w-full p-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="Ville, Pays"
                  />
                </div>

                <div>
                  <label className="block text-xs text-gray-500 mb-1">Antécédents médicaux</label>
                  <textarea
                    value={userProfile.medicalHistory}
                    onChange={(e) => setUserProfile({...userProfile, medicalHistory: e.target.value})}
                    className="w-full p-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    rows={3}
                    placeholder="Allergies, conditions existantes..."
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer sidebar */}
        <div className="p-4 border-t border-gray-200">
          <div className="bg-red-50 rounded-lg p-3">
            <div className="flex items-start">
              <AlertTriangle className="h-4 w-4 mt-0.5 mr-2 text-red-500" />
              <div>
                <p className="text-xs font-medium text-red-800">URGENCE MÉDICALE</p>
                <p className="text-xs text-red-600 mt-1">
                  En cas d'urgence, contactez immédiatement les services locaux :
                  SAMU 15 | Pompiers 18 | Urgence Européenne 112
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Overlay pour mobile */}
      {showSidebar && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-10 lg:hidden"
          onClick={() => setShowSidebar(false)}
        />
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        

        <header className="bg-white border-b border-gray-200">
          <div className="flex items-center justify-between p-4">
            <div className="flex items-center">
              {!showSidebar && (
                <button 
                  onClick={() => setShowSidebar(true)}
                  className="p-2 mr-2 rounded-lg hover:bg-gray-100"
                >
                  <Crosshair className="h-5 w-5 text-gray-600" />
                </button>
              )}
              <h1 className="text-xl font-bold">
                <span className="text-green-600">Assistant</span> Médical Africain
              </h1>
            </div>

            <div className="flex items-center space-x-2">
              {/* Sélecteur de langue */}
              <div className="relative">
                <button
                  onClick={() => setShowLanguageDropdown(!showLanguageDropdown)}
                  className="flex items-center space-x-1 bg-gray-100 hover:bg-gray-200 py-2 px-3 rounded-lg transition-colors"
                >
                  <span>
                    {SUPPORTED_LANGUAGES.find(lang => lang.code === selectedLanguage)?.icon}
                  </span>
                  <span className="text-sm">
                    {SUPPORTED_LANGUAGES.find(lang => lang.code === selectedLanguage)?.name}
                  </span>
                  {showLanguageDropdown ? (
                    <ChevronUp className="h-4 w-4" />
                  ) : (
                    <ChevronDown className="h-4 w-4" />
                  )}
                </button>

                {showLanguageDropdown && (
                  <div className="absolute right-0 mt-1 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-10">
                    {SUPPORTED_LANGUAGES.map((lang) => (
                      <button
                        key={lang.code}
                        onClick={() => {
                          setSelectedLanguage(lang.code);
                          setShowLanguageDropdown(false);
                        }}
                        className={`w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center space-x-2 ${
                          selectedLanguage === lang.code ? 'bg-gray-50' : ''
                        }`}
                      >
                        <span>{lang.icon}</span>
                        <span>{lang.name}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>

              <button className="p-2 rounded-lg hover:bg-gray-100">
                <Settings className="h-5 w-5 text-gray-600" />
              </button>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('chat')}
              className={`flex-1 py-3 text-sm font-medium ${
                activeTab === 'chat' 
                  ? 'text-green-600 border-b-2 border-green-600' 
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Conversation
            </button>
            <button
              onClick={() => setActiveTab('resources')}
              className={`flex-1 py-3 text-sm font-medium ${
                activeTab === 'resources' 
                  ? 'text-green-600 border-b-2 border-green-600' 
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Ressources
            </button>
            <button
              onClick={() => setActiveTab('emergency')}
              className={`flex-1 py-3 text-sm font-medium ${
                activeTab === 'emergency' 
                  ? 'text-green-600 border-b-2 border-green-600' 
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Urgences
            </button>
          </div>
        </header>
        
        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto bg-white">
          {activeTab === 'chat' && (
            <div className="h-full flex flex-col">
              {messages.length === 0 ? (
                <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
                  <div className={`p-5 rounded-full mb-6 ${
                    connectionStatus === 'online' && apiHealthy
                      ? 'bg-green-100 text-green-600'
                      : 'bg-yellow-100 text-yellow-600'
                  }`}>
                    {connectionStatus === 'online' && apiHealthy ? (
                      <Wifi className="h-10 w-10" />
                    ) : (
                      <WifiOff className="h-10 w-10" />
                    )}
                  </div>
                  <h2 className="text-xl font-bold mb-2">
                    {connectionStatus === 'online' && apiHealthy
                      ? 'Assistant médical connecté'
                      : 'Mode hors ligne activé'}
                  </h2>
                  <p className="text-gray-500 max-w-md mb-8">
                    {connectionStatus === 'online' && apiHealthy
                      ? 'Posez vos questions médicales et recevez des conseils personnalisés adaptés au contexte africain.'
                      : 'Vous pouvez poser des questions basiques. Pour des conseils complets, connectez-vous à internet.'}
                  </p>
                  
                  <div className="grid grid-cols-2 gap-3 w-full max-w-md">
                    {QUICK_ACTIONS.map((action, index) => (
                      <button
                        key={index}
                        onClick={() => handleQuickAction(action.keywords)}
                        className="flex flex-col items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                      >
                        <div className="bg-gray-100 p-2 rounded-full mb-2">
                          {action.icon}
                        </div>
                        <span className="text-sm">{action.label}</span>
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="p-4 space-y-4">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[90%] lg:max-w-[70%] rounded-2xl p-4 relative ${
                          message.role === 'user'
                            ? 'bg-green-600 text-white'
                            : message.isEmergency
                              ? 'bg-red-100 border-l-4 border-red-500'
                              : message.isOffline
                                ? 'bg-gray-100 border-l-4 border-yellow-500'
                                : 'bg-gray-100'
                        }`}
                      >
                        {/* Badge hors ligne */}
                        {message.isOffline && (
                          <div className="absolute -top-2 -left-2 bg-yellow-500 text-white text-xs px-2 py-1 rounded-full flex items-center">
                            <Clock className="h-3 w-3 mr-1" />
                            <span>Hors ligne</span>
                          </div>
                        )}
                        
                        {/* En-tête du message */}
                        <div className="flex items-center mb-1">
                          {message.role === 'user' ? (
                            <User className="h-4 w-4 mr-2" />
                          ) : (
                            <Bot className="h-4 w-4 mr-2" />
                          )}
                          <span className="text-xs opacity-75">
                            {formatTime(message.timestamp)}
                          </span>
                        </div>
                        
                        {/* Contenu du message */}
                        <p className={`text-sm leading-relaxed whitespace-pre-wrap ${
                          message.isEmergency ? 'text-red-800' : ''
                        }`}>
                          {message.content}
                        </p>
                      </div>
                    </div>
                  ))}
                  
                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="bg-gray-100 px-4 py-3 rounded-2xl">
                        <div className="flex items-center space-x-2">
                          <Loader2 className="h-4 w-4 text-gray-500 animate-spin" />
                          <span className="text-sm text-gray-500">
                            {connectionStatus === 'online' && apiHealthy
                              ? "Recherche d'informations..."
                              : "Analyse en cours..."}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  <div ref={messagesEndRef} />
                </div>
              )}
            </div>
          )}

          {activeTab === 'resources' && (
            <div className="p-6">
              <h2 className="text-xl font-bold mb-6">Ressources médicales</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* Carte Symptômes */}
                <div className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow">
                  <div className="bg-green-100 p-4 flex items-center">
                    <Thermometer className="h-6 w-6 text-green-600 mr-3" />
                    <h3 className="font-medium">Symptômes courants</h3>
                  </div>
                  <div className="p-4">
                    <p className="text-sm text-gray-600 mb-3">
                      Guide des symptômes fréquents et conseils de premiers soins
                    </p>
                    <button className="text-sm text-green-600 font-medium hover:underline">
                      Voir la liste complète →
                    </button>
                  </div>
                </div>
                
                {/* Carte Médicaments */}
                <div className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow">
                  <div className="bg-blue-100 p-4 flex items-center">
                    <Pill className="h-6 w-6 text-blue-600 mr-3" />
                    <h3 className="font-medium">Médicaments essentiels</h3>
                  </div>
                  <div className="p-4">
                    <p className="text-sm text-gray-600 mb-3">
                      Liste des médicaments de base recommandés par l'OMS
                    </p>
                    <button className="text-sm text-blue-600 font-medium hover:underline">
                      Consulter la liste →
                    </button>
                  </div>
                </div>
                
                {/* Carte Premiers secours */}
                <div className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow">
                  <div className="bg-red-100 p-4 flex items-center">
                    <HeartPulse className="h-6 w-6 text-red-600 mr-3" />
                    <h3 className="font-medium">Premiers secours</h3>
                  </div>
                  <div className="p-4">
                    <p className="text-sm text-gray-600 mb-3">
                      Procédures d'urgence pour les situations critiques
                    </p>
                    <button className="text-sm text-red-600 font-medium hover:underline">
                      Apprendre les gestes →
                    </button>
                  </div>
                </div>
                
                {/* Carte Centres de santé */}
                <div className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow">
                  <div className="bg-purple-100 p-4 flex items-center">
                    <Globe className="h-6 w-6 text-purple-600 mr-3" />
                    <h3 className="font-medium">Centres de santé</h3>
                  </div>
                  <div className="p-4">
                    <p className="text-sm text-gray-600 mb-3">
                      Localisation des centres médicaux et hôpitaux proches
                    </p>
                    <button className="text-sm text-purple-600 font-medium hover:underline">
                      Trouver un centre →
                    </button>
                  </div>
                </div>
                
                {/* Carte Santé mentale */}
                <div className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow">
                  <div className="bg-yellow-100 p-4 flex items-center">
                    <Brain className="h-6 w-6 text-yellow-600 mr-3" />
                    <h3 className="font-medium">Santé mentale</h3>
                  </div>
                  <div className="p-4">
                    <p className="text-sm text-gray-600 mb-3">
                      Ressources et conseils pour le bien-être psychologique
                    </p>
                    <button className="text-sm text-yellow-600 font-medium hover:underline">
                      Accéder aux ressources →
                    </button>
                  </div>
                </div>
                
                {/* Carte Prévention */}
                <div className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow">
                  <div className="bg-orange-100 p-4 flex items-center">
                    <Shield className="h-6 w-6 text-orange-600 mr-3" />
                    <h3 className="font-medium">Prévention</h3>
                  </div>
                  <div className="p-4">
                    <p className="text-sm text-gray-600 mb-3">
                      Conseils pour prévenir les maladies courantes
                    </p>
                    <button className="text-sm text-orange-600 font-medium hover:underline">
                      Voir les conseils →
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'emergency' && (
            <div className="p-6">
              <h2 className="text-xl font-bold mb-6">Informations d'urgence</h2>
              
              <div className="space-y-6">
                {/* Section Numéros d'urgence */}
                <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-r-lg">
                  <div className="flex items-start">
                    <AlertTriangle className="h-5 w-5 text-red-500 mr-3 mt-0.5" />
                    <div>
                      <h3 className="font-medium text-red-800 mb-2">NUMÉROS D'URGENCE</h3>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                        <div className="bg-white p-3 rounded-lg">
                          <p className="font-bold text-red-600">SAMU (Urgences médicales)</p>
                          <p className="text-2xl font-bold">15</p>
                        </div>
                        <div className="bg-white p-3 rounded-lg">
                          <p className="font-bold text-red-600">Pompiers</p>
                          <p className="text-2xl font-bold">18</p>
                        </div>
                        <div className="bg-white p-3 rounded-lg">
                          <p className="font-bold text-red-600">Urgence Européenne</p>
                          <p className="text-2xl font-bold">112</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* Section Signes d'urgence */}
                <div>
                  <h3 className="font-medium text-lg mb-3">Signes nécessitant une intervention urgente</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {[
                      "Difficultés respiratoires importantes",
                      "Douleur thoracique intense",
                      "Perte de connaissance",
                      "Saignement abondant",
                      "Signes d'AVC (visage asymétrique, trouble de la parole)",
                      "Brûlures étendues",
                      "Intoxication suspectée",
                      "Traumatisme crânien avec perte de connaissance"
                    ].map((sign, index) => (
                      <div key={index} className="flex items-start">
                        <div className="bg-red-100 p-1 rounded-full mr-3 mt-0.5">
                          <AlertTriangle className="h-3 w-3 text-red-500" />
                        </div>
                        <p className="text-sm">{sign}</p>
                      </div>
                    ))}
                  </div>
                </div>
                
                {/* Section Premiers gestes */}
                <div>
                  <h3 className="font-medium text-lg mb-3">Premiers gestes en attendant les secours</h3>
                  <div className="space-y-3">
                    {[
                      "Allonger la personne si inconsciente",
                      "Ne pas donner à boire",
                      "Protéger du froid ou de la chaleur",
                      "Pratiquer les gestes de premiers secours si formé",
                      "Ne pas déplacer en cas de traumatisme",
                      "Rester calme et rassurer la victime"
                    ].map((gesture, index) => (
                      <div key={index} className="flex items-start">
                        <div className="bg-green-100 p-1 rounded-full mr-3 mt-0.5">
                          <HeartPulse className="h-3 w-3 text-green-500" />
                        </div>
                        <p className="text-sm">{gesture}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>

        {/* Input Area (only for chat tab) */}
        {activeTab === 'chat' && (
          <div className="border-t border-gray-200 bg-white p-4">
            <form onSubmit={handleSubmit} className="relative">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder={
                  connectionStatus === 'online' && apiHealthy
                    ? "Posez votre question médicale..."
                    : "Mode hors ligne - Questions basiques seulement..."
                }
                className="w-full p-4 pr-12 border border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent shadow-sm disabled:bg-gray-100"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !inputMessage.trim()}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-green-600 text-white p-2 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <Send className="h-5 w-5" />
                )}
              </button>
            </form>
            
            {(!apiHealthy || connectionStatus === 'offline') && (
              <div className="mt-2 flex items-center text-yellow-600 text-sm">
                <Zap className="h-4 w-4 mr-2" />
                <span>
                  {connectionStatus === 'offline'
                    ? 'Connectez-vous à internet pour des conseils complets'
                    : 'Le serveur médical est temporairement indisponible'}
                </span>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;