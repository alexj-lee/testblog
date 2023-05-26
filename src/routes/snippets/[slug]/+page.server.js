
/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch, setHeaders }) {
	const slug = params.slug;
	console.log('slug', slug);
	let [pageData, listData] = await Promise.all([
		fetch(`/api/snippets.json`),
		//fetch(`/api/localPosts.json`)
	])

	let json = await pageData.json();
	json = json.filter(item => item.slug === slug);
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

	return {
		json: json[0],
		//json: pageData,
		//list: (await listData.json()).slice(0, 10),
		slug,
	};
	// } catch (err) {
	// 	console.error('error fetching blog post at [slug].svelte: ' + slug, res, err);
	// 	throw error(500, 'error fetching blog post at [slug].svelte: ' + slug + ': ' + res);
	// }
}
