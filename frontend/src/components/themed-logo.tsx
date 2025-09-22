'use client';

import { useColorScheme } from '@mui/material/styles';
import Image from 'next/image';

export default function ThemedLogo() {
  const { mode, systemMode } = useColorScheme();

  const light = (): boolean =>
    (mode == 'system' ? systemMode : mode) == 'light';

  return (
    <Image
      src={
        light() ?
          '/images/denbot-logo-light.svg'
        : '/images/denbot-logo-dark.svg'
      }
      alt="Logo"
      width={10}
      height={10}
      sizes="100vw"
      style={{ width: '80%', height: 'auto', paddingLeft: '10%' }}
      loading="eager"
    />
  );
}
