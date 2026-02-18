"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { apiBaseUrl } from "@/lib/auth";

type AuthResponse = {
  user: {
    email: string;
  };
};

export function UserHeader() {
  const [email, setEmail] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    async function loadUser() {
      try {
        const response = await fetch(`${apiBaseUrl()}/v1/auth/me`, {
          credentials: "include"
        });

        if (!response.ok) {
          if (mounted) {
            setEmail(null);
          }
          return;
        }

        const body = (await response.json()) as AuthResponse;
        if (mounted) {
          setEmail(body.user.email);
        }
      } catch {
        if (mounted) {
          setEmail(null);
        }
      }
    }

    loadUser();

    return () => {
      mounted = false;
    };
  }, []);

  if (!email) {
    return (
      <Link href="/login" className="text-sm text-slate-600 underline dark:text-slate-300">
        Login
      </Link>
    );
  }

  return <p className="text-sm text-slate-600 dark:text-slate-300">Signed in as {email}</p>;
}
