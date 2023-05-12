/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		'./src/**/*.svelte',
		// may also want to include HTML files
		'./src/**/*.html'
	],
	darkMode: 'class',
	theme: {
		extend: {
			colors: {
				'tahiti': '#32b978',
				'cameopink': '#EFBBCC',
				'cerblue': '#29bdad',
				'greenblue': '#2dbc94',
				'pistachio': '#56aa69',
				'chromium': '#66ab56',
				'artemesia': '#65a98f',
				'sulphur': '#f5f5b8',
				'vblue': '#021126',
			},

			typography: (theme) => ({
				DEFAULT: {
					css: {
						'--tw-prose-bullets': theme('colors.black'),
						// these customizations are explained here https://youtu.be/-FzemNMcOGs
						blockquote: {
							borderLeft: '3px solid red',
							fontSize: 'inherit',
							fontStyle: 'inherit',
							fontWeight: 'medium'
						},
						'blockquote p:first-of-type::before': {
							content: ''
						},
						'blockquote p:last-of-type::after': {
							content: ''
						},

						'code::before': false,
						'code::after': false,
						code: {
							'border-radius': '0.25rem',
							padding: '0.15rem 0.3rem',
							borderWidth: '2px',
							borderColor: 'rgba(0,0,0,0.1)'
						},
						pre: {
							'border-radius': '0rem',
						},
						'a:hover': {
							color: '#31cdce !important',
							textDecoration: 'underline !important'
						},
						a: {
							color: '#2071ad',
							textDecoration: 'none'
						},
						'a code': {
							color: 'unset'
						},
						table: {
							overflow: 'hidden'
						},
						'li, ul, ol': {
							margin: 0
						},
						'li > img': {
							margin: 0,
							display: 'inline'
						},
						'ol > li::marker': {
							color: 'var(--tw-prose-body)'
						},
						'ul > li::marker': {
							color: 'var(--tw-prose-body)'
						},
						'ul > li > p': {
							marginTop: 0,
							marginBottom: 0,
						},
					}
				}
			})
		}
	},
	variants: {},
	plugins: [
		require('@tailwindcss/typography')
	]
};
