import { error } from '@sveltejs/kit';

export async function load({ fetch }) {
	const res = await fetch(`/api/localPosts.json`);
	// alternate strategy https://www.davidwparker.com/posts/how-to-make-an-rss-feed-in-sveltekit
	// Object.entries(import.meta.glob('./*.md')).map(async ([path, page]) => {
	if (res.status > 400) {
		throw error(res.status, await res.text());
	}

	/** /** @type {import('$lib/types').ContentItem[]} */
	var items = await res.json();

	// items = items.filter(item => { return item.published == true });
	// items = items.sort((a, b) => { return parseInt(b.Slice(0, 4)) - parseInt(a.Slice(0, 4)) })

	// items.sort(function compare(a, b) {
	// 	var dateA = new Date(a.date);
	// 	var dateB = new Date(b.date);
	// 	return dateB - dateA;
	// })

	// items.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
	return { items };
}
