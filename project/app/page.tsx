import { redirect } from 'next/navigation';
import { getServerSession } from 'next-auth/next';
import { authOptions } from './api/auth/[...nextauth]/route';
import Link from 'next/link';

export default async function Home() {
  const session = await getServerSession(authOptions);

  if (session) {
    redirect('/dashboard');
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4 text-center">Bienvenue dans l'application Next.js</h1>
      <p className="text-center mb-6">
        Veuillez vous connecter pour accéder aux fonctionnalités protégées.
      </p>
      <div className="text-center">
        <Link href="/auth/signin">
          <button className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700">
            Se connecter
          </button>
        </Link>
      </div>
    </main>
  );
}
