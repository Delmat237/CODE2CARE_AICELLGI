// app/layout.tsx
import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { getServerSession } from 'next-auth/next';
import { authOptions } from './api/auth/[...nextauth]/route';
import { Providers } from './providers';
import AuthProvider from './AuthProvider';
import Header from '@/components/Header';


const inter = Inter({ subsets: ['latin'] });
export const dynamic = "force-dynamic";


export const metadata: Metadata = {
  title: 'DGH Patient Feedback System',
  description: "Système de gestion et d'analyse des feedbacks patients - Douala General Hospital",
  keywords: 'patient feedback, hospital, healthcare, Douala, Cameroon',
  authors: [{ name: 'DGH Development Team' }],
  viewport: 'width=device-width, initial-scale=1, maximum-scale=1',
  themeColor: '#2563eb',
  manifest: '/manifest.json',
};

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await getServerSession(authOptions);

  return (
    <html lang="fr">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="format-detection" content="telephone=no" />
      </head>
      <body className={`min-h-screen bg-gray-100 ${inter.className}`}>
        <Providers>
          <AuthProvider session={session}>
            <Header />
            {children}
          </AuthProvider>
        </Providers>
      </body>
    </html>
  );
}
