// vite.config.js
import { sveltekit } from '@sveltejs/kit/vite';
import { mdsvex } from 'mdsvex';
import { ssp } from "sveltekit-search-params/plugin";


/** @type {import('vite').UserConfig} */
const config = {
	plugins: [ssp(), sveltekit(), mdsvex()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	},
	server: {
		fs: {
			// https://vitejs.dev/config/server-options.html#server-fs-allow
			// allows importing readme for About page
			allow: ['..']
		}
	}
};

export default config;
