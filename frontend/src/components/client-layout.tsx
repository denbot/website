'use client';

import { createTheme, CssBaseline, ThemeProvider } from '@mui/material';
import { Toaster } from 'react-hot-toast';

const theme = createTheme({
  colorSchemes: {
    dark: true,
  },
});

export default function ClientLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline /> {children}
      <Toaster position="top-right" />
    </ThemeProvider>
  );
}
