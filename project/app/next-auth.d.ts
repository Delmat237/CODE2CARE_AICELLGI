// next-auth.d.ts (à créer à la racine de votre projet)
import NextAuth from "next-auth";

declare module "next-auth" {
  interface User {
    id: string;
    name?: string | null;
    email?: string | null;
    image?: string | null;
    external_id?: string; // Added for credentials provider
    accessToken?: string; // Added for JWT token from FastAPI
  }

  interface Session {
    user: User;
    accessToken?: string; // Added for JWT token in session
  }
}