import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import '../style/globals.css';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import { AppProps } from 'next/app';
import Layout from '@/components/layout';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'Denbot - Denver Robotics',
  description: 'Placeholder',
};

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Layout>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Component {...pageProps} />
      </body>
    </Layout>
  );
}
