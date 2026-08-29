import type { Metadata } from 'next';
import './globals.css';

const siteOrigin = process.env.VERCEL_PROJECT_PRODUCTION_URL
  ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`
  : 'http://localhost:3000';

export const metadata: Metadata = {
  metadataBase: new URL(siteOrigin),
  title: 'TraceFlow AI — Evidence to verified passport',
  description: 'A structured, evidence-backed product record for compliance workflows and Digital Product Passports.',
  openGraph: {
    title: 'TraceFlow AI',
    description: 'From product evidence to verified passport.',
    images: [{ url: '/og.png', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'TraceFlow AI',
    description: 'From product evidence to verified passport.',
    images: ['/og.png'],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
