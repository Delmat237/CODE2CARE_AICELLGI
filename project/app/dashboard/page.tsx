"use client";

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { StarRating } from '@/components/star-rating';
import { LanguageSelector } from '@/components/language-selector';
import { NetworkStatus } from '@/components/network-status';
import { useLanguage } from '@/lib/language-context';
import { PatientFeedback } from '@/lib/types';
import { 
  Star, Search, Filter, TrendingUp, Users, MessageSquare, Calendar,
  Heart, Globe, BarChart3, PieChart, Activity, Clock
} from 'lucide-react';
import Link from 'next/link';

export const dynamic = "force-dynamic";

export default  function DashboardPage() {
  const { t } = useLanguage();
  const [feedbacks, setFeedbacks] = useState<PatientFeedback[]>([]);
  const [filteredFeedbacks, setFilteredFeedbacks] = useState<PatientFeedback[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCondition, setSelectedCondition] = useState('all');
  const [selectedGender, setSelectedGender] = useState('all');
  const [selectedLanguage, setSelectedLanguage] = useState('all');
  const [loading, setLoading] = useState(true);
  

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    filterFeedbacks();
  }, [searchTerm, selectedCondition, selectedGender, selectedLanguage, feedbacks]);

  const loadData = async () => {
    try {
      // Mock data for demonstration - replace with actual API call
      const mockData: PatientFeedback[] = [
        {
          id: 1,
          patient_name: "EYENGA BALA",
          age: 45,
          gender: "female",
          condition: "Hypertension",
          treatment_satisfaction: 4,
          communication_rating: 5,
          facility_rating: 4,
          overall_experience: 4,
          recommendation_likelihood: 8,
          feedback_date: "2024-01-15",
          comments: "Excellent service, personnel très attentionné. Temps d'attente raisonnable.",
          language: "fr",
          submission_method: "web",
          sentiment: "positive",
          is_synced: true
        },
        {
          id: 2,
          patient_name: "BALA ANDEGUE",
          age: 62,
          gender: "male",
          condition: "Diabète",
          treatment_satisfaction: 5,
          communication_rating: 4,
          facility_rating: 5,
          overall_experience: 5,
          recommendation_likelihood: 9,
          feedback_date: "2024-01-14",
          comments: "Very satisfied with medical follow-up. Professional and caring team.",
          language: "en",
          submission_method: "web",
          sentiment: "positive",
          is_synced: true
        },
        {
          id: 3,
          patient_name: "Sophie MENGUE",
          age: 34,
          gender: "female",
          condition: "Migraine",
          treatment_satisfaction: 3,
          communication_rating: 3,
          facility_rating: 3,
          overall_experience: 3,
          recommendation_likelihood: 6,
          feedback_date: "2024-01-13",
          comments: "Service correct mais temps d'attente un peu long. Traitement efficace.",
          language: "fr",
          submission_method: "sms",
          sentiment: "neutral",
          is_synced: true
        },
        {
          id: 4,
          patient_name: "BATCHAKOUI PIERRE",
          age: 58,
          gender: "male",
          condition: "Arthrite",
          treatment_satisfaction: 4,
          communication_rating: 5,
          facility_rating: 4,
          overall_experience: 4,
          recommendation_likelihood: 8,
          feedback_date: "2024-01-12",
          comments: "Médecin très à l'écoute. Explications claires sur le traitement.",
          language: "fr",
          submission_method: "web",
          sentiment: "positive",
          is_synced: true
        },
        {
          id: 5,
          patient_name: "MAGNE ISABELLE",
          age: 29,
          gender: "female",
          condition: "Anxiété",
          treatment_satisfaction: 5,
          communication_rating: 5,
          facility_rating: 4,
          overall_experience: 5,
          recommendation_likelihood: 10,
          feedback_date: "2024-01-11",
          comments: "Prise en charge exceptionnelle. Je recommande vivement cette clinique.",
          language: "fr",
          submission_method: "web",
          emoji_rating: "very_happy",
          sentiment: "positive",
          is_synced: true
        }
      ];
      
      setFeedbacks(mockData);
      setLoading(false);
    } catch (error) {
      console.error('Error loading data:', error);
      setLoading(false);
    }
  };

  const filterFeedbacks = () => {
    let filtered = feedbacks;

    if (searchTerm) {
      filtered = filtered.filter(feedback =>
        feedback.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        feedback.condition.toLowerCase().includes(searchTerm.toLowerCase()) ||
        feedback.comments.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (selectedCondition !== 'all') {
      filtered = filtered.filter(feedback => feedback.condition === selectedCondition);
    }

    if (selectedGender !== 'all') {
      filtered = filtered.filter(feedback => feedback.gender === selectedGender);
    }

    if (selectedLanguage !== 'all') {
      filtered = filtered.filter(feedback => feedback.language === selectedLanguage);
    }

    setFilteredFeedbacks(filtered);
  };

  const getAverageRating = (field: keyof PatientFeedback): string => {
  if (feedbacks.length === 0) return "0.0";
  const sum = feedbacks.reduce((acc, feedback) => acc + (feedback[field] as number), 0);
  return (sum / feedbacks.length).toFixed(1);
};


  const getConditions = () => {
    return [...new Set(feedbacks.map(f => f.condition))];
  };

  const getGenders = () => {
    return [...new Set(feedbacks.map(f => f.gender))];
  };

  const getLanguages = () => {
    return [...new Set(feedbacks.map(f => f.language))];
  };

  const getRecommendationScore = () => {
    if (feedbacks.length === 0) return 0;
    const sum = feedbacks.reduce((acc, feedback) => acc + feedback.recommendation_likelihood, 0);
    return Math.round((sum / feedbacks.length) * 10);
  };

  const getSentimentDistribution = () => {
    const distribution = { positive: 0, neutral: 0, negative: 0 };
    feedbacks.forEach(feedback => {
      if (feedback.sentiment) {
        distribution[feedback.sentiment]++;
      }
    });
    return distribution;
  };

  const getSubmissionMethodDistribution = () => {
    const distribution: { [key: string]: number } = {};
    feedbacks.forEach(feedback => {
      distribution[feedback.submission_method] = (distribution[feedback.submission_method] || 0) + 1;
    });
    return distribution;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">{t('common.loading')}</p>
        </div>
      </div>
    );
  }

  const sentimentDistribution = getSentimentDistribution();
  const submissionMethods = getSubmissionMethodDistribution();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <NetworkStatus />
      
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <Heart className="h-8 w-8 text-red-500" />
              <h1 className="text-4xl font-bold text-gray-900">
                {t('dashboard.title')}
              </h1>
            </div>
            <p className="text-gray-600 text-lg">
              {t('dashboard.subtitle')}
            </p>
          </div>
          <div className="flex items-center gap-4 mt-4 md:mt-0">
            <LanguageSelector />
            <Link href="/feedback">
              <Button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700">
                {t('nav.feedback')}
              </Button>
            </Link>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{t('stats.total_patients')}</CardTitle>
              <Users className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">{feedbacks.length}</div>
              <p className="text-xs text-muted-foreground">{t('stats.feedbacks_collected')}</p>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{t('stats.average_satisfaction')}</CardTitle>
              <Star className="h-4 w-4 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">
                {getAverageRating('overall_experience')}/5
              </div>
              <p className="text-xs text-muted-foreground">{t('stats.global_experience')}</p>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{t('stats.nps_score')}</CardTitle>
              <TrendingUp className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{getRecommendationScore()}%</div>
              <p className="text-xs text-muted-foreground">{t('stats.recommendation')}</p>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{t('stats.communication')}</CardTitle>
              <MessageSquare className="h-4 w-4 text-purple-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600">
                {getAverageRating('communication_rating')}/5
              </div>
              <p className="text-xs text-muted-foreground">{t('stats.average_rating')}</p>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card className="mb-8 bg-white shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Filter className="h-5 w-5" />
              {t('nav.filters')}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  placeholder={t('filter.search')}
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              
              <Select value={selectedCondition} onValueChange={setSelectedCondition}>
                <SelectTrigger>
                  <SelectValue placeholder={t('filter.condition')} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">{t('filter.all_conditions')}</SelectItem>
                  {getConditions().map(condition => (
                    <SelectItem key={condition} value={condition}>{condition}</SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Select value={selectedGender} onValueChange={setSelectedGender}>
                <SelectTrigger>
                  <SelectValue placeholder={t('filter.gender')} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">{t('filter.all_genders')}</SelectItem>
                  <SelectItem value="male">{t('feedback.male')}</SelectItem>
                  <SelectItem value="female">{t('feedback.female')}</SelectItem>
                </SelectContent>
              </Select>

              <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
                <SelectTrigger>
                  <SelectValue placeholder={t('filter.language')} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">{t('filter.all_languages')}</SelectItem>
                  {getLanguages().map(lang => (
                    <SelectItem key={lang} value={lang}>{lang.toUpperCase()}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Main Content */}
        <Tabs defaultValue="feedbacks" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 lg:w-[600px]">
            <TabsTrigger value="feedbacks">{t('nav.feedback_details')}</TabsTrigger>
            <TabsTrigger value="analytics">{t('nav.analytics')}</TabsTrigger>
            <TabsTrigger value="insights">{t('nav.insights')}</TabsTrigger>
          </TabsList>

          <TabsContent value="feedbacks" className="space-y-6">
            <div className="grid gap-6">
              {filteredFeedbacks.map((feedback) => (
                <Card key={feedback.id} className="bg-white shadow-lg hover:shadow-xl transition-shadow">
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-lg">{feedback.patient_name}</CardTitle>
                        <CardDescription className="flex items-center gap-4 mt-1">
                          <span>{feedback.age} {t('common.years')} • {t(`feedback.${feedback.gender}`)}</span>
                          <Badge variant="secondary">{feedback.condition}</Badge>
                          <Badge variant="outline" className="flex items-center gap-1">
                            <Globe className="h-3 w-3" />
                            {feedback.language.toUpperCase()}
                          </Badge>
                          <Badge variant="outline" className="flex items-center gap-1">
                            <Activity className="h-3 w-3" />
                            {feedback.submission_method}
                          </Badge>
                          <span className="flex items-center gap-1">
                            <Calendar className="h-3 w-3" />
                            {new Date(feedback.feedback_date).toLocaleDateString()}
                          </span>
                        </CardDescription>
                      </div>
                      <div className="text-right">
                        <div className="text-sm text-gray-600 mb-1">{t('stats.global_score')}</div>
                        <div className="flex items-center gap-1">
                          <StarRating value={feedback.overall_experience} onChange={() => {}} readonly size="sm" />
                        </div>
                        {feedback.sentiment && (
                          <Badge 
                            variant={feedback.sentiment === 'positive' ? 'default' : 
                                   feedback.sentiment === 'negative' ? 'destructive' : 'secondary'}
                            className="mt-1"
                          >
                            {t(`sentiment.${feedback.sentiment}`)}
                          </Badge>
                        )}
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                      <div>
                        <div className="text-sm text-gray-600 mb-1">{t('rating.treatment')}</div>
                        <StarRating value={feedback.treatment_satisfaction} onChange={() => {}} readonly size="sm" />
                      </div>
                      <div>
                        <div className="text-sm text-gray-600 mb-1">{t('rating.communication')}</div>
                        <StarRating value={feedback.communication_rating} onChange={() => {}} readonly size="sm" />
                      </div>
                      <div>
                        <div className="text-sm text-gray-600 mb-1">{t('rating.facility')}</div>
                        <StarRating value={feedback.facility_rating} onChange={() => {}} readonly size="sm" />
                      </div>
                      <div>
                        <div className="text-sm text-gray-600 mb-1">{t('rating.recommendation')}</div>
                        <div className="flex items-center gap-3">
                          <Progress value={feedback.recommendation_likelihood * 10} className="flex-1" />
                          <span className="font-semibold">{feedback.recommendation_likelihood}/10</span>
                        </div>
                      </div>
                    </div>

                    {feedback.emoji_rating && (
                      <div className="mb-4">
                        <div className="text-sm text-gray-600 mb-1">{t('feedback.emoji_rating')}</div>
                        <span className="text-2xl">
                          {feedback.emoji_rating === 'very_sad' && '😢'}
                          {feedback.emoji_rating === 'sad' && '😞'}
                          {feedback.emoji_rating === 'neutral' && '😐'}
                          {feedback.emoji_rating === 'happy' && '😊'}
                          {feedback.emoji_rating === 'very_happy' && '😍'}
                        </span>
                      </div>
                    )}

                    {feedback.comments && (
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <div className="text-sm text-gray-600 mb-1">{t('feedback.comments')}</div>
                        <p className="text-gray-800 italic">"{feedback.comments}"</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-white shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <PieChart className="h-5 w-5" />
                    {t('analytics.condition_distribution')}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {getConditions().map(condition => {
                      const count = feedbacks.filter(f => f.condition === condition).length;
                      const percentage = (count / feedbacks.length) * 100;
                      return (
                        <div key={condition} className="flex items-center justify-between">
                          <span className="text-sm font-medium">{condition}</span>
                          <div className="flex items-center gap-2">
                            <Progress value={percentage} className="w-20" />
                            <span className="text-sm text-gray-600 w-8">{count}</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5" />
                    {t('analytics.criteria_averages')}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium">{t('rating.treatment')}</span>
                        <span className="text-sm font-bold">{getAverageRating('treatment_satisfaction')}/5</span>
                      </div>
                      <Progress value={parseFloat(getAverageRating('treatment_satisfaction')) * 20} />
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium">{t('rating.communication')}</span>
                        <span className="text-sm font-bold">{getAverageRating('communication_rating')}/5</span>
                      </div>
                      <Progress value={parseFloat(getAverageRating('communication_rating')) * 20} />
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium">{t('rating.facility')}</span>
                        <span className="text-sm font-bold">{getAverageRating('facility_rating')}/5</span>
                      </div>
                      <Progress value={parseFloat(getAverageRating('facility_rating')) * 20} />
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium">{t('rating.overall')}</span>
                        <span className="text-sm font-bold">{getAverageRating('overall_experience')}/5</span>
                      </div>
                      <Progress value={parseFloat(getAverageRating('overall_experience')) * 20} />
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Activity className="h-5 w-5" />
                    {t('analytics.sentiment_analysis')}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-green-600">{t('sentiment.positive')}</span>
                      <div className="flex items-center gap-2">
                        <Progress value={(sentimentDistribution.positive / feedbacks.length) * 100} className="w-20" />
                        <span className="text-sm text-gray-600 w-8">{sentimentDistribution.positive}</span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-600">{t('sentiment.neutral')}</span>
                      <div className="flex items-center gap-2">
                        <Progress value={(sentimentDistribution.neutral / feedbacks.length) * 100} className="w-20" />
                        <span className="text-sm text-gray-600 w-8">{sentimentDistribution.neutral}</span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-red-600">{t('sentiment.negative')}</span>
                      <div className="flex items-center gap-2">
                        <Progress value={(sentimentDistribution.negative / feedbacks.length) * 100} className="w-20" />
                        <span className="text-sm text-gray-600 w-8">{sentimentDistribution.negative}</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Globe className="h-5 w-5" />
                    {t('analytics.submission_methods')}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {Object.entries(submissionMethods).map(([method, count]) => {
                      const percentage = (count / feedbacks.length) * 100;
                      return (
                        <div key={method} className="flex items-center justify-between">
                          <span className="text-sm font-medium capitalize">{method}</span>
                          <div className="flex items-center gap-2">
                            <Progress value={percentage} className="w-20" />
                            <span className="text-sm text-gray-600 w-8">{count}</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="insights" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-white shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-green-600" />
                    {t('insights.positive_trends')}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="p-3 bg-green-50 rounded-lg">
                      <p className="text-sm text-green-800">
                        <strong>{((sentimentDistribution.positive / feedbacks.length) * 100).toFixed(1)}%</strong> {t('insights.positive_feedback')}
                      </p>
                    </div>
                    <div className="p-3 bg-blue-50 rounded-lg">
                      <p className="text-sm text-blue-800">
                        {t('insights.high_communication')} <strong>{getAverageRating('communication_rating')}/5</strong>
                      </p>
                    </div>
                    <div className="p-3 bg-purple-50 rounded-lg">
                      <p className="text-sm text-purple-800">
                        {t('insights.nps_score')} <strong>{getRecommendationScore()}%</strong>
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Clock className="h-5 w-5 text-orange-600" />
                    {t('insights.improvement_areas')}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {parseFloat(getAverageRating('facility_rating')) < 4 && (
                      <div className="p-3 bg-orange-50 rounded-lg">
                        <p className="text-sm text-orange-800">
                          {t('insights.improve_facilities')} ({getAverageRating('facility_rating')}/5)
                        </p>
                      </div>
                    )}
                    {parseFloat(getAverageRating('treatment_satisfaction')) < 4 && (
                      <div className="p-3 bg-red-50 rounded-lg">
                        <p className="text-sm text-red-800">
                          {t('insights.improve_treatment')} ({getAverageRating('treatment_satisfaction')}/5)
                        </p>
                      </div>
                    )}
                    {sentimentDistribution.negative > 0 && (
                      <div className="p-3 bg-yellow-50 rounded-lg">
                        <p className="text-sm text-yellow-800">
                          {sentimentDistribution.negative} {t('insights.negative_feedback_attention')}
                        </p>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}