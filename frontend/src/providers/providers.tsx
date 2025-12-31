"use client";

import { QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { getQueryClient } from "./get-query-client";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { AntdRegistry } from "@ant-design/nextjs-registry";

import { useAuth } from "@clerk/nextjs";
import { setTokenGetter } from "@/apis/api";
import { useEffect } from "react";

interface ProvidersProps {
  children: React.ReactNode;
}

export function AuthInitializer({ children }: { children: React.ReactNode }) {
  const { getToken } = useAuth();

  useEffect(() => {
    setTokenGetter(async () => {
      return await getToken();
    });
  }, [getToken]);

  return <>{children}</>;
}

export function Providers({ children }: ProvidersProps) {
  const queryClient = getQueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      <NextThemesProvider
        attribute="class"
        defaultTheme="light"
        enableSystem
        disableTransitionOnChange
      >
        <AntdRegistry>
          <AuthInitializer>{children}</AuthInitializer>
        </AntdRegistry>
      </NextThemesProvider>
      {process.env.NODE_ENV === "development" && (
        <ReactQueryDevtools initialIsOpen={false} />
      )}
    </QueryClientProvider>
  );
}
