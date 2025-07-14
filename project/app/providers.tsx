"use client";

import { LanguageProvider } from '@/lib/language-context';
import { SessionProvider } from 'next-auth/react'


export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <LanguageProvider>
      {children}
    </LanguageProvider>
  );
}


export default function AuthProvider({
  children,
  session
}: {
  children: React.ReactNode
  session: any
}) {
  return <SessionProvider session={session}>{children}</SessionProvider>
}