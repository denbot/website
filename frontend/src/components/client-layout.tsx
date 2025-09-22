'use client';

import { Toaster } from 'react-hot-toast';

export default function ClientLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <Toaster position="top-right" />
      {children}
    </>
  );
}
