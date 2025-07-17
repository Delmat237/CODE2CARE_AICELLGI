"use client";

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Calendar, Clock, Pill, User, AlertCircle, CheckCircle2, Search } from 'lucide-react';
import { useLanguage } from '@/lib/language-context';
import { LanguageSelector } from '@/components/language-selector';
import { NetworkStatus } from '@/components/network-status';
import Link from 'next/link';

// Define interfaces for appointments and medication reminders
interface Appointment {
  id: number;
  patient_name: string;
  doctor_name: string;
  specialty: string;
  date: string;
  time: string;
  status: 'upcoming' | 'completed' | 'cancelled';
  location: string;
}

interface MedicationReminder {
  id: number;
  medication_name: string;
  dosage: string;
  frequency: string;
  time: string;
  start_date: string;
  end_date: string;
  status: 'active' | 'completed';
}

export default function PatientPortalPage() {
  const { t } = useLanguage();
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [medicationReminders, setMedicationReminders] = useState<MedicationReminder[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      // Replace with actual FastAPI backend call
      const mockAppointments: Appointment[] = [
        {
          id: 1,
          patient_name: "EYENGA BALA",
          doctor_name: "Dr. MBOUE",
          specialty: "Cardiologie",
          date: "2025-07-20",
          time: "10:00",
          status: "upcoming",
          location: "Clinique Centrale, Yaoundé",
        },
        {
          id: 2,
          patient_name: "EYENGA BALA",
          doctor_name: "Dr. NGONO",
          specialty: "Neurologie",
          date: "2025-07-25",
          time: "14:30",
          status: "upcoming",
          location: "Hôpital Général, Douala",
        },
        {
          id: 3,
          patient_name: "EYENGA BALA",
          doctor_name: "Dr. EKANE",
          specialty: "Endocrinologie",
          date: "2025-07-10",
          time: "09:00",
          status: "completed",
          location: "Clinique Centrale, Yaoundé",
        },
      ];

      const mockMedicationReminders: MedicationReminder[] = [
        {
          id: 1,
          medication_name: "Metformine",
          dosage: "500mg",
          frequency: "Deux fois par jour",
          time: "08:00, 20:00",
          start_date: "2025-07-01",
          end_date: "2025-12-31",
          status: "active",
        },
        {
          id: 2,
          medication_name: "Amlodipine",
          dosage: "10mg",
          frequency: "Une fois par jour",
          time: "07:00",
          start_date: "2025-07-01",
          end_date: "2025-09-30",
          status: "active",
        },
      ];

      setAppointments(mockAppointments);
      setMedicationReminders(mockMedicationReminders);
      setLoading(false);
    } catch (error) {
      console.error('Error loading data:', error);
      setError(t('common.error_loading'));
      setLoading(false);
    }
  };

  const filteredAppointments = appointments.filter(
    (appt) =>
      appt.doctor_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      appt.specialty.toLowerCase().includes(searchTerm.toLowerCase()) ||
      appt.location.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredMedications = medicationReminders.filter(
    (med) =>
      med.medication_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      med.dosage.toLowerCase().includes(searchTerm.toLowerCase()) ||
      med.frequency.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleCancelAppointment = async (id: number) => {
    try {
      // Replace with actual FastAPI backend call to cancel appointment
      setAppointments((prev) =>
        prev.map((appt) =>
          appt.id === id ? { ...appt, status: 'cancelled' } : appt
        )
      );
    } catch (error) {
      console.error('Error cancelling appointment:', error);
      setError(t('common.error_action'));
    }
  };

  const handleCompleteMedication = async (id: number) => {
    try {
      // Replace with actual FastAPI backend call to mark medication as completed
      setMedicationReminders((prev) =>
        prev.map((med) =>
          med.id === id ? { ...med, status: 'completed' } : med
        )
      );
    } catch (error) {
      console.error('Error completing medication:', error);
      setError(t('common.error_action'));
    }
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <NetworkStatus />
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <User className="h-8 w-8 text-blue-600" />
              <h1 className="text-4xl font-bold text-gray-900">
                {t('patient_portal.title')}
              </h1>
            </div>
            <p className="text-gray-600 text-lg">
              {t('patient_portal.subtitle')}
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

        {/* Search Bar */}
        <Card className="mb-8 bg-white shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="h-5 w-5" />
              {t('filter.search')}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <Input
                placeholder={t('patient_portal.search_placeholder')}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </CardContent>
        </Card>

        {/* Appointments Section */}
        <Card className="mb-8 bg-white shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5 text-blue-600" />
              {t('patient_portal.appointments')}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {error && (
              <div className="flex items-center gap-2 p-3 bg-red-50 rounded-lg mb-4">
                <AlertCircle className="h-5 w-5 text-red-600" />
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}
            {filteredAppointments.length === 0 ? (
              <p className="text-gray-600">{t('patient_portal.no_appointments')}</p>
            ) : (
              <div className="grid gap-4">
                {filteredAppointments.map((appt) => (
                  <Card key={appt.id} className="bg-gray-50 shadow-sm hover:shadow-md transition-shadow">
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <div>
                          <CardTitle className="text-lg">{appt.doctor_name}</CardTitle>
                          <CardDescription className="flex flex-wrap items-center gap-4 mt-1">
                            <span>
                              {new Date(appt.date).toLocaleDateString()} • {appt.time}
                            </span>
                            <Badge variant="secondary">{appt.specialty}</Badge>
                            <Badge
                              variant={
                                appt.status === 'upcoming'
                                  ? 'default'
                                  : appt.status === 'completed'
                                  ? 'secondary'
                                  : 'destructive'
                              }
                            >
                              {t(`patient_portal.status.${appt.status}`)}
                            </Badge>
                            <span className="flex items-center gap-1">
                              <Calendar className="h-3 w-3" />
                              {appt.location}
                            </span>
                          </CardDescription>
                        </div>
                        {appt.status === 'upcoming' && (
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={() => handleCancelAppointment(appt.id)}
                          >
                            {t('patient_portal.cancel')}
                          </Button>
                        )}
                      </div>
                    </CardHeader>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Medication Reminders Section */}
        <Card className="bg-white shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Pill className="h-5 w-5 text-purple-600" />
              {t('patient_portal.medication_reminders')}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {filteredMedications.length === 0 ? (
              <p className="text-gray-600">{t('patient_portal.no_medications')}</p>
            ) : (
              <div className="grid gap-4">
                {filteredMedications.map((med) => (
                  <Card key={med.id} className="bg-gray-50 shadow-sm hover:shadow-md transition-shadow">
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <div>
                          <CardTitle className="text-lg">{med.medication_name}</CardTitle>
                          <CardDescription className="flex flex-wrap items-center gap-4 mt-1">
                            <span>{t('patient_portal.dosage')}: {med.dosage}</span>
                            <span>{t('patient_portal.frequency')}: {med.frequency}</span>
                            <span>{t('patient_portal.time')}: {med.time}</span>
                            <Badge
                              variant={med.status === 'active' ? 'default' : 'secondary'}
                            >
                              {t(`patient_portal.status.${med.status}`)}
                            </Badge>
                            <span>
                              {t('patient_portal.duration')}: {new Date(med.start_date).toLocaleDateString()} -{' '}
                              {new Date(med.end_date).toLocaleDateString()}
                            </span>
                          </CardDescription>
                        </div>
                        {med.status === 'active' && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleCompleteMedication(med.id)}
                            className="flex items-center gap-2"
                          >
                            <CheckCircle2 className="h-4 w-4" />
                            {t('patient_portal.mark_completed')}
                          </Button>
                        )}
                      </div>
                    </CardHeader>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}