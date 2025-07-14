"use client";
import Link from "next/link";
import { useSession } from "next-auth/react";
import UserMenu from "./UserMenu";

export default function Header() {
  const { data: session } = useSession();

  return (
    <header className="bg-blue-600 text-white p-4">
      <nav className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-xl font-bold">
          Mon App
        </Link>
        <ul className="flex space-x-4">
          <li>
            <Link href="/">Accueil</Link>
          </li>
          {session && (
            <li>
              <Link href="/protected">Page Protégée</Link>
            </li>
          )}
        </ul>
        <UserMenu/>
      </nav>
    </header>
  );
}