'use client';
import { signIn } from "next-auth/react";
import Head from "next/head";
import { FaGoogle, FaGithub } from "react-icons/fa";
import { useState } from "react";

export default function SignIn() {
  const [matricule, setMatricule] = useState("");
  const [email, setEmail] = useState("");

  const handleCredentialsSignIn = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await signIn("credentials", {
      matricule,
      email,
      callbackUrl: "/"
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Head>
        <title>Connexion - Application Next.js</title>
        <meta name="description" content="Page de connexion sécurisée" />
      </Head>
      
      <div className="bg-white p-8 rounded-xl shadow-sm w-full max-w-md border border-gray-200">
        <h1 className="text-2xl font-bold mb-8 text-center text-gray-800">Connectez-vous à votre compte</h1>
        
        <div className="space-y-6">
          {/* Matricule and Email Form */}
          <form onSubmit={handleCredentialsSignIn} className="space-y-4">
            <div>
              <label htmlFor="matricule" className="block text-sm font-medium text-gray-700 mb-1">
                Matricule
              </label>
              <input
                id="matricule"
                type="text"
                value={matricule}
                onChange={(e) => setMatricule(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Entrez votre matricule"
                required
              />
            </div>
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Adresse Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Entrez votre email"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
            >
              <span className="font-medium">Connexion avec matricule</span>
            </button>
          </form>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-gray-500">Ou continuer avec</span>
            </div>
          </div>

          {/* Social Login Buttons */}
          <div className="space-y-4">
            <button
              onClick={() => signIn("google", { callbackUrl: "/" })}
              className="w-full flex items-center justify-center gap-3 bg-white text-gray-700 py-3 px-4 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors shadow-sm"
            >
              <FaGoogle className="text-red-500 text-xl" />
              <span className="font-medium">Continuer avec Google</span>
            </button>
            
            <button
              onClick={() => signIn("github", { callbackUrl: "/" })}
              className="w-full flex items-center justify-center gap-3 bg-gray-800 text-white py-3 px-4 rounded-lg hover:bg-gray-900 transition-colors shadow-sm"
            >
              <FaGithub className="text-xl" />
              <span className="font-medium">Continuer avec GitHub</span>
            </button>
          </div>
        </div>
        
        <div className="mt-6 pt-6 border-t border-gray-200 text-center">
          <p className="text-sm text-gray-500">
            En continuant, vous acceptez nos conditions d'utilisation
          </p>
        </div>
      </div>
    </div>
  );
}