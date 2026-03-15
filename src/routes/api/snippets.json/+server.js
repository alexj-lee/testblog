import { slugFromPath } from '$lib/content.js';
import { json } from '@sveltejs/kit';
import { render } from 'svelte/server';

export const prerender = true;

export async function GET({ url }) {
	const modules = import.meta.glob('/src/routes/content/snippets/*.{md,svx,svelte.md}');
	const iterablePostFiles = Object.entries(modules);

	const allPosts = await Promise.all(
		iterablePostFiles.map(async ([path, resolver]) => {
			const resolvedPost = await resolver();
			const rendered = render(resolvedPost.default);
			const slug = slugFromPath(path);

			return {
				slug: slug,
				...resolvedPost.metadata,
				md: { html: rendered.body },
			};
		})
	);

	const sortedPosts = allPosts
		.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
		.filter(item => item.published == true);

	return json(sortedPosts);
}
