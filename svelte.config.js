import adapter from '@sveltejs/adapter-vercel';
import { mdsvex } from 'mdsvex';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import rehypeKatexSvelte from "rehype-katex-svelte";
import rehypeSlug from 'rehype-slug';
import remarkAbbr from 'remark-abbr';
import remarkGithub from 'remark-github';
import remarkMath from 'remark-math';
import preprocess from 'svelte-preprocess';

// mdsvex config
const mdsvexConfig = {
	extensions: ['.svelte.md', '.md', '.svx'],
	layout: {
		_: './src/mdsvexlayout.svelte', // default mdsvex layout
		blog: './src/mdsvexlayout.svelte'
	},
	remarkPlugins: [
		[
			remarkGithub,
			{
				// Use your own repository
				repository: 'https://github.com/mvasigh/sveltekit-mdsvex-blog.git'
			}
		],
		remarkAbbr,
		remarkMath,
	],
	rehypePlugins: [
		rehypeSlug,
		[
			rehypeAutolinkHeadings,
			{
				behavior: 'wrap'
			}
		],
		rehypeKatexSvelte,
	]
};

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: ['.svelte', '.html', '.svx', ...mdsvexConfig.extensions],
	preprocess: [
		mdsvex(mdsvexConfig),
		preprocess({
			postcss: true
		})
	],

	// Docs: https://github.com/sveltejs/kit/blob/master/packages/adapter-netlify/README.md
	kit: {
		adapter: adapter({
			split: true,
			//edge: false,

			// pages: 'build',
			// assets: 'build',
			// fallback: null,
			// precompress: false,
			// strict: true,

			// nov 2022
			// if true, will create a Netlify Edge Function rather
			// than using standard Node-based functions. however, also uses esbuild, which as of nov 2022 has a bug on netlify
			// https://github.com/sveltejs/kit/issues/7839#issuecomment-1328605300

			// dec 2022 - moved back to true since we're using esbuild again

		}),

		// https://kit.svelte.dev/docs/configuration#csp
		// csp: {
		// 	directives: {
		// 		'script-src': ['self']
		// 	},
		// 	reportOnly: {
		// 		'script-src': ['self']
		// 	}
		// }
	}
};

export default config;
