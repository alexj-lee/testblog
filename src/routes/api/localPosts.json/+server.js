import { slugFromPath } from '$lib/content.js';
import { json } from '@sveltejs/kit';
// /** @type {import('@sveltejs/kit').RequestHandler} */
// export async function GET({ url }) {
// 	/** const modules = import.meta.glob('/content/*.{md,svx,svelte.md}'); */
// 	const modules = import.meta.glob('/src/routes/content/*.{md,svx,svelte.md}', { eager: true });

// 	const postPromises = [];

// 	for (let [path, resolver] of Object.entries(modules)) {
// 		const slug = slugFromPath(path);
// 		const promise = resolver().then((post) => ({
// 			slug,
// 			...post.metadata
// 		}));

// 		postPromises.push(promise);
// 	}

// 	const posts = await Promise.all(postPromises);
// 	// const publishedPosts = posts.filter((post) => post.published)

// 	// publishedPosts.sort((a, b) => (new Date(a.date) > new Date(b.date) ? -1 : 1));

// 	return json(posts);
// }



import rehypeKatex from 'rehype-katex';
import rehypeSlug from 'rehype-slug';
import remarkAbbr from 'remark-abbr';
import rehypeAutoLink from 'remark-autolink-headings';
import remarkMath from 'remark-math';

const remarkPlugins = [
	remarkAbbr,
	remarkMath,
];
const rehypePlugins = [
	//rehypeStringify,
	rehypeSlug,
	[
		rehypeAutoLink,
		{
			behavior: 'wrap',
			properties: { class: 'hover:text-yellow-100 no-underline' }
		}
	],
	rehypeKatex
];

export const prerender = true;

export async function GET({ url }) {
	const modules = import.meta.glob('/src/routes/content/*.{md,svx,svelte.md}');
	const iterablePostFiles = Object.entries(modules);

	const allPosts = await Promise.all(
		iterablePostFiles.map(async ([path, resolver]) => {
			const resolvedPost = await resolver();
			const body = resolvedPost.default.render(); // this is the compiled HTML
			const slug = slugFromPath(path);
			//const md2 = await compile(body.html, { remarkPlugins, rehypePlugins });
			// const md = await compile(body.html, { remarkPlugins, rehypePlugins });
			//console.log(md);
			//md2.html = md2.code;
			const metadata = resolvedPost.metadata;
			//console.log(metadata.category);

			return {
				// meta: resolvedPost.metadata,
				slug: slug,
				...resolvedPost.metadata,
				//extra: md,
				//...metadata,
				// body: body,
				md: body,
				//md2: md2,
			};
		})
	);
	//console.log(allPosts);

	// const sortedPosts = allPosts.filter(item => item.published == true).sort((a, b) => {
	// 	return new Date(b.date).getTime() - new Date(a.date).getTime();
	// })
	const sortedPosts = allPosts.sort((a, b) => {
		return new Date(b.date).getTime() - new Date(a.date).getTime();
	})


	return json(sortedPosts);

};

