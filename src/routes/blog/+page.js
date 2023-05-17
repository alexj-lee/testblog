import { error } from '@sveltejs/kit';

export async function load({ setHeaders, fetch }) {
	const res = await fetch(`/api/localPosts.json`);
	// alternate strategy https://www.davidwparker.com/posts/how-to-make-an-rss-feed-in-sveltekit
	// Object.entries(import.meta.glob('./*.md')).map(async ([path, page]) => {
	if (res.status > 400) {
		throw error(res.status, await res.text());
	}

	/** /** @type {import('$lib/types').ContentItem[]} */
	var items = await res.json();
	// console.log('im here alex');
	// console.log(typeof items);
	// console.log(items[0])


	items = items.filter(item => { return item.published == true });

	return { items };
}
