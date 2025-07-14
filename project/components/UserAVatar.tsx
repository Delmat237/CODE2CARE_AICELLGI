// components/UserAvatar.tsx
'use client'

import { useSession } from "next-auth/react";

export default function UserAvatar() {
  const { data: session } = useSession();
  
  if (!session?.user) return null;

  console.log(session.user.id); // ✔ TypeScript ne montrera plus d'erreur
  // ...
}