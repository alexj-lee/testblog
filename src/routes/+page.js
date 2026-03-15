import { error } from '@sveltejs/kit';

export const prerender = true;

export async function load({ setHeaders, fetch }) {
	const res = await fetch(`/api/localPosts.json`);

	if (res.status > 400) {
		error(res.status, await res.text());
	}

	/** @type {import('$lib/types').ContentItem[]} */
	const items = await res.json();
	setHeaders({
		'cache-control': `public, max-age=3600`, // 1 hour
	});
	return { items: items.slice(0, 10) };
}
