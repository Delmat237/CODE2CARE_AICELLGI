"use client";
import Link from "next/link";
import { useSession } from "next-auth/react";
import UserMenu from "./UserMenu";

export default function Header() {
  const { data: session } = useSession();
  const role = session?.user?.role as string;

  const navItems = [
    { name: "Accueil", href: "/" },
    { name: "Dashboard", href: "/dashboard", roles: ["admin", "medecin"] },
    { name: "Mes dossiers", href: "/patient", roles: ["patient"] },
    { name: "Gestion Médecins", href: "/admin/medecins", roles: ["admin"] },
    { name: "Gestion Patients", href: "/medecin/patients", roles: ["medecin"] },
  ];

  return (
    <header className="bg-blue-700 text-white shadow-md sticky top-0 z-50">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
        {/* Logo */}
        <Link href="/" className="text-2xl font-semibold tracking-wide hover:text-gray-200">
          🩺 FeedbackApp
        </Link>
        <Link href="/patient" className="text-xl font-semibold tracking-wide hover:text-gray-200">
          patient
        </Link>


        {/* Navigation */}
        <ul className="hidden md:flex space-x-6 text-sm font-medium">
          {navItems
            .filter((item) => !item.roles || item.roles.includes(role))
            .map((item) => (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className="hover:text-gray-300 transition-colors"
                >
                  {item.name}
                </Link>
              </li>
            ))}
        </ul>

        {/* Menu utilisateur */}
        <UserMenu />
      </nav>
    </header>
  );
}
