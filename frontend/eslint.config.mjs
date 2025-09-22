import { FlatCompat } from '@eslint/eslintrc';
import { dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({ baseDirectory: __dirname });

const eslintConfig = [
  ...compat.extends(
    'next/core-web-vitals',
    'next/typescript',
    'prettier',
    'plugin:import/recommended',
  ),
  {
    rules: {
      'no-restricted-imports': [
        'error',
        {
          paths: [
            {
              name: '@mui/material',
              message: 'Import from specific path, e.g., @mui/material/Button',
            },
            {
              name: '@mui/icons-material',
              message:
                'Import icons individually, e.g., @mui/icons-material/Add',
            },
          ],
          patterns: [
            // Blocks relative imports that go up beyond the current folder
            '../**',
          ],
        },
      ],
    },
  },
  { ignores: ['next-env.d.ts'] },
];

export default eslintConfig;
