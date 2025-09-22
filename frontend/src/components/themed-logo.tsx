'use client';

import { useTheme } from '@mui/material';
import Image from 'next/image';

export default function ThemedLogo() {
  const theme = useTheme();

  return (
    <Image
      src={
        theme.palette.mode == 'light' ?
          '/images/denbot-logo-light.svg'
        : '/images/denbot-logo-dark.svg'
      }
      alt="Logo"
      width={0}
      height={0}
      sizes="100vw"
      style={{ width: '80%', height: 'auto', paddingLeft: '10%' }}
    />
  );
}
