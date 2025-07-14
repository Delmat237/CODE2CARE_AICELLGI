'use client';
import { signIn } from "next-auth/react";
import Head from "next/head";
import { FaGoogle, FaGithub } from "react-icons/fa";

export default function SignIn() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Head>
        <title>Connexion - Application Next.js</title>
        <meta name="description" content="Page de connexion sécurisée" />
      </Head>
      
      <div className="bg-white p-8 rounded-xl shadow-sm w-full max-w-md border border-gray-200">
        <h1 className="text-2xl font-bold mb-8 text-center text-gray-800">Connectez-vous à votre compte</h1>
        
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
        
        <div className="mt-6 pt-6 border-t border-gray-200 text-center">
          <p className="text-sm text-gray-500">
            En continuant, vous acceptez nos conditions d'utilisation
          </p>
        </div>
      </div>
    </div>
  );
}