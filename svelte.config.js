import adapter from '@sveltejs/adapter-netlify';
import { mdsvex } from 'mdsvex';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import rehypeKatexSvelte from 'rehype-katex-svelte';
import rehypeSlug from 'rehype-slug';
import remarkAbbr from 'remark-abbr';
import remarkGithub from 'remark-github';
import remarkMath from 'remark-math';

// mdsvex config
const mdsvexConfig = {
	extensions: ['.svelte.md', '.md', '.svx'],
	layout: {
		_: new URL('./src/mdsvexlayout.svelte', import.meta.url).pathname,
		blog: new URL('./src/mdsvexlayout.svelte', import.meta.url).pathname
	},
	remarkPlugins: [
		[
			remarkGithub,
			{
				repository: 'https://github.com/mvasigh/sveltekit-mdsvex-blog.git'
			}
		],
		remarkAbbr,
		remarkMath
	],
	rehypePlugins: [
		rehypeSlug,
		[
			rehypeAutolinkHeadings,
			{
				behavior: 'prepend'
			}
		],
		rehypeKatexSvelte
	]
};

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: ['.svelte', '.html', '.svx', ...mdsvexConfig.extensions],
	preprocess: [mdsvex(mdsvexConfig), vitePreprocess()],

	kit: {
		adapter: adapter({
			edge: false
		}),
		prerender: {
			handleHttpError: 'warn'
		}
	}
};

export default config;
