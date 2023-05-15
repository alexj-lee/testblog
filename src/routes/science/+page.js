async function loadSorted(filterKey, values) {
	const filtered = values.filter((item) => item.type == filterKey);
	const sorted = filtered.sort((a, b) => new Date(b.year) - new Date(a.year));
	return sorted
};

/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch, setHeaders }) {
	// let [pageData, listData] = await Promise.all([
	// 	fetch(`/api/research.json`),
	// ])

	const items = await fetch(`/api/research.json`).then((res) => res.json());
	const entries = Object.values(items);

	//console.log(Object.entries(items));
	// console.log(typeof items);
	// console.log(entries)

	// const preprints = entries.filter((item) => item.type == 'preprint');
	// const papers = entries.filter((item) => item.type == 'paper');
	// const conferences = entries.filter((item) => item.type == 'conference');

	const preprints = await loadSorted('preprint', entries);
	const papers = await loadSorted('paper', entries);
	const conferences = await loadSorted('conference', entries);


	//const sortedPreprints = papers.sort((a, b) => { return new Date(b.year) > new Date(a.year) });
	// const sortedPreprints = papers.sort((a, b) => { return new Date(b.year) - new Date(a.year) })
	// const dates = entries.map((item) => new Date(item.year));
	// dates.sort((a, b) => { return b - a })
	// console.log(dates);
	// console.log(sortedPreprints);
	// console.log('aaa')
	// const x = await loadSorted('paper', entries);
	// console.log(x);

	return {
		json: {
			papers,
			preprints,
			conferences,
		}
		//json: json,
		//json: pageData,
		//list: (await listData.json()).slice(0, 10),
	};
	// } catch (err) {
	// 	console.error('error fetching blog post at [slug].svelte: ' + slug, res, err);
	// 	throw error(500, 'error fetching blog post at [slug].svelte: ' + slug + ': ' + res);
	// }
}
