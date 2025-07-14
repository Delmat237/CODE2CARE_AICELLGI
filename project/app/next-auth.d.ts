// next-auth.d.ts (à créer à la racine de votre projet)
import NextAuth from "next-auth";

declare module "next-auth" {
  interface User {
    id: string;
    name?: string | null;
    email?: string | null;
    image?: string | null;
  }
  
  interface Session {
    user: User;
  }
}