import NextAuth, { NextAuthOptions } from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import GitHubProvider from "next-auth/providers/github";
import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
      authorization: {
        params: {
          prompt: "select_account", // Force la sélection du compte
          scope: "openid email profile", // Demande explicitement l'image de profil
        },
      },
    }),
    GitHubProvider({
      clientId: process.env.GITHUB_CLIENT_ID || "",
      clientSecret: process.env.GITHUB_CLIENT_SECRET || "",
      profile(profile) {
        return {
          id: profile.id.toString(),
          name: profile.name || profile.login,
          email: profile.email,
          image: profile.avatar_url,
        };
      },
    }),
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        external_id: { label: "code de connexion", type: "text", placeholder: "Entrez votre code" },
        email: { label: "Email", type: "email", placeholder: "Entrez votre email" },
        password: { label: "Password", type: "password", placeholder: "Entrez votre mot de passe" },
      },
      async authorize(credentials: {
        external_id: any; exter?: string; email?: string; password?: string 
} | undefined) {
        if (!credentials) {
          return null;
        }
        console.log("voici mes credentials",credentials)
        // Send credentials to FastAPI backend
        const res = await fetch("http://192.168.1.167:8000/api/auth/patient", {
          method: "POST",
          body: JSON.stringify({
            external_id:"P000001",
            email: "azangueleonel9@gmail.com"
         
          }),
          headers: { "Content-Type": "application/json" },
        });
        

        const user = await res.json();

        // If authentication is successful, return user object
        if (res.ok && user) {
          return {
            id: user.id,
            matricule: user.matricule,
            email: user.email,
            accessToken: user.access_token, // Assuming FastAPI returns a JWT
          };
        }

        // Return null if authentication fails
        return null;
      },
    }),
  ],
  callbacks: {
    async session({ session, token }) {
      // Transfère toutes les infos utilisateur à la session
      if (session.user) {
        session.user.id = token.sub || "";
        session.user.image = token.picture || null;
        session.user.external_id = token.matricule as string | undefined;
        session.user.email = token.email || null;
        session.accessToken = token.accessToken as string | undefined;
      }
      return session;
    },
    async jwt({ token, user }) {
      // Stocke l'image de profil et credentials dans le token
      if (user) {
        token.picture = user.image;
        token.matricule = user.external_id;
        token.email = user.email;
        token.accessToken = user.accessToken;
      }
      return token;
    },
    async redirect({ url, baseUrl }) {
      return url.startsWith(baseUrl) ? url : baseUrl;
    },
  },
  pages: {
    signIn: "/auth/signin",
    error: "/auth/error",
  },
  session: {
    strategy: "jwt", // Utilise JWT pour une meilleure compatibilité
  },
  debug: process.env.NODE_ENV === "development",
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };