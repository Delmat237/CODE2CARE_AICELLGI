// components/UserMenu.tsx
'use client'

import { signOut } from "next-auth/react";
import { useSession } from "next-auth/react";
import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import { FiUser, FiLogOut, FiSettings } from "react-icons/fi";

export default function UserMenu() {
  const { data: session } = useSession();
  const [isOpen, setIsOpen] = useState(false);

  if (!session?.user) return null;

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2"
        aria-label="Menu utilisateur"
      >
        <div className="relative h-8 w-8 rounded-full overflow-hidden">
          <Image
            src={session.user.image || '/default-avatar.png'}
            alt="Photo de profil"
            fill
            className="object-cover"
            sizes="32px"
          />
        </div>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50 border border-gray-100">
          <div className="px-4 py-2 text-sm text-gray-700">
            <p className="font-medium">{session.user.name || session.user.email}</p>
          </div>
          <Link
            href="/profile"
            className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
            onClick={() => setIsOpen(false)}
          >
            <div className="flex items-center">
              <FiUser className="mr-2" />
              Profil
            </div>
          </Link>
          <button
            onClick={() => signOut({ callbackUrl: '/' })}
            className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
          >
            <div className="flex items-center">
              <FiLogOut className="mr-2" />
              Déconnexion
            </div>
          </button>
        </div>
      )}
    </div>
  );
}