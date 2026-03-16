export const prerender = true;

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

	const press = [
		{
			title: 'Fed on Reams of Cell Data, AI Maps New Neighborhoods in the Brain',
			publication: 'Quanta Magazine',
			date: '2026-02-09',
			url: 'https://www.quantamagazine.org/fed-on-reams-of-cell-data-ai-maps-new-neighborhoods-in-the-brain-20260209/',
			image: '/press/quanta-brain-cartography.webp'
		},
		{
			title: 'How neuroscientists are using AI',
			publication: 'The Transmitter',
			date: '2025-11-04',
			url: 'https://www.thetransmitter.org/neuroscientists-using-ai/how-neuroscientists-are-using-ai/',
			image: '/press/transmitter-ai-neuroscience.png'
		},
		{
			title: 'The Dayhoff Atlas: scaling sequence diversity improves protein design',
			publication: 'Microsoft Research',
			date: '2025-07-25',
			url: 'https://www.microsoft.com/en-us/research/articles/the-dayhoff-atlas/',
			image: '/press/microsoft-dayhoff-atlas.png'
		}
	];

	return {
		papers,
		preprints,
		conferences,
		press,
		//json: json,
		//json: pageData,
		//list: (await listData.json()).slice(0, 10),
	};
	// } catch (err) {
	// 	console.error('error fetching blog post at [slug].svelte: ' + slug, res, err);
	// 	throw error(500, 'error fetching blog post at [slug].svelte: ' + slug + ': ' + res);
	// }
}
