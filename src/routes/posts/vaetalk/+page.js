import { REPO_URL } from '$lib/siteConfig';

// we choose NOT to prerender blog pages because it is easier to edit and see changes immediately
// instead we set cache control headers
// export const prerender = true


/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch, setHeaders }) {
	const slug = "vaetalk";
	let [pageData, listData] = await Promise.all([
		fetch(`/api/blog/${slug}.json`),
		//fetch(`/api/localPosts.json`)
	])

	let json = await pageData.json();
	//console.log(Object.keys(params));

	//Object.assign(json, { date: '1999-0901' });
	//console.log(Object.keys(json));
	//console.log(json.content.content);



	// if (pageData.status > 400) {
	// 	throw error(pageData.status, await pageData.text());
	// }
	// if (listData.status > 400) {
	// 	throw error(listData.status, await listData.text());
	// }

	// const reet = await pageData.json();
	// console.log(reet.content)
	console.log('im done bro')
	return {
		json: json,
		//json: pageData,
		//list: (await listData.json()).slice(0, 10),
		slug,
		REPO_URL
	};
	// } catch (err) {
	// 	console.error('error fetching blog post at [slug].svelte: ' + slug, res, err);
	// 	throw error(500, 'error fetching blog post at [slug].svelte: ' + slug + ': ' + res);
	// }
}
