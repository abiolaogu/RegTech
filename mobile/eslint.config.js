// eslint.config.js (flat config with Babel parser)
import js from '@eslint/js';
import reactPlugin from 'eslint-plugin-react';
import babelParser from '@babel/eslint-parser';

export default [
    js.configs.recommended,
    {
        files: ['**/*.js', '**/*.jsx'],
        languageOptions: {
            parser: babelParser,
            parserOptions: {
                requireConfigFile: false,
                babelOptions: {
                    presets: ['@babel/preset-react'],
                },
                ecmaVersion: 2021,
                sourceType: 'module',
                ecmaFeatures: { jsx: true },
            },
            globals: {
                browser: true,
                node: true,
                describe: 'readonly',
                it: 'readonly',
                expect: 'readonly',
                test: 'readonly',
                jest: 'readonly'
            },
        },
        plugins: { react: reactPlugin },
        rules: {
            ...reactPlugin.configs.recommended.rules,
            'react/prop-types': 'off',
            'no-unused-vars': 'warn',
        },
        settings: { react: { version: 'detect' } },
    },
];
