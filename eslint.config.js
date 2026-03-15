import js from '@eslint/js';
import svelte from 'eslint-plugin-svelte';
import prettier from 'eslint-config-prettier';
import globals from 'globals';

export default [
	js.configs.recommended,
	...svelte.configs['flat/recommended'],
	prettier,
	...svelte.configs['flat/prettier'],
	{
		languageOptions: {
			globals: {
				...globals.browser,
				...globals.node
			}
		},
		rules: {
			'no-unused-expressions': 'warn',
			'no-constant-binary-expression': 'warn',
			'no-sequences': 'warn',
			'no-unused-vars': 'warn',
			'svelte/no-at-html-tags': 'warn',
			'svelte/require-each-key': 'warn',
			'svelte/no-navigation-without-resolve': 'warn'
		}
	},
	{
		ignores: ['build/', '.svelte-kit/', 'node_modules/', '.netlify/']
	}
];
