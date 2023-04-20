import { slugFromPath } from '$lib/localcontent';
import { json } from '@sveltejs/kit';

/** @type {import('@sveltejs/kit').RequestHandler} */
export async function GET({ url
}) {
	/** const modules = import.meta.glob('/content/*.{md,svx,svelte.md}'); */
	const modules = import.meta.glob('/src/routes/content/*.{md,svx,svelte.md}');

	const postPromises = [];

	const l = modules.length;

	var n = 0
	for (const path in modules) {
		n += 1;
	}

	for (let [path, resolver] of Object.entries(modules)) {
		const slug = slugFromPath(path);
		const promise = resolver().then((post) => ({
			slug,
			...post.metadata
		}));

		postPromises.push(promise);
	}

	const posts = await Promise.all(postPromises);
	const publishedPosts = posts.filter((post) => post.published)

	publishedPosts.sort((a, b) => (new Date(a.date) > new Date(b.date) ? -1 : 1));

	return json(posts);
}
