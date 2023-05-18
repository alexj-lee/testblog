// import { promises as fs } from 'fs';
export const prerender = true;


/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch }) {
	// let [pageData, listData] = await Promise.all([
	// 	fetch(`/api/research.json`),
	// ])

	// const item = await fs.readFile('static/identifiability-vae-presentation/idvae.html', { encoding: 'utf-8' });
	// console.log(item);
	var items = await fetch(`/api/reveal.json`).then((res) => res.json());
	const entries = Object.values(items);
	console.log(items);
	console.log(typeof items)
	items = JSON.stringify(items);
	console.log(typeof items)
	
	return {
		items
		// item
		//json: json,
		//json: pageData,
		//list: (await listData.json()).slice(0, 10),
	};
	// } catch (err) {
	// 	console.error('error fetching blog post at [slug].svelte: ' + slug, res, err);
	// 	throw error(500, 'error fetching blog post at [slug].svelte: ' + slug + ': ' + res);
	// }
}
