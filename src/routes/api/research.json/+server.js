import { json } from '@sveltejs/kit';
import { promises as fs } from 'fs';
export const prerender = true;

async function readPaperFile(fileName, postPromises, typeOfItem) {
	const papers = fs.readFile(fileName, { encoding: 'utf-8' });
	const papersArray = (await papers).split("\n");

	for (let [index, item] of Object.entries(papersArray)) {
		if (!item) {
			continue
		};

		//const regex = /(?:(Alex Jihun Lee|Lee, Alex J.|Alex Lee|Alex J Lee|Alex J. Lee)?).*\({0,1}(20\d{2})\){0,1}.*(https.*\d)>{0,1}$/gm
		//const regex = /.*?(?:(Alex Lee|Alex Jihun Lee|Alex J Lee|Alex J\. Lee|Lee, Alex J\.))?.*\({0,1}(20\d{2})\){0,1}.*(https.*\d)>{0,1}$/gm
		//const regex = /.*?(?:(Alex Lee|Alex Jihun Lee|Alex J Lee|Lee, A\.|Lee, A\. J\.|Alex J\. Lee|Alex J\. Lee|Lee, Alex J\.).*)?\({0,1}(20\d{2})\){0,1}.*https:\/\/doi.org\/(.*\d)>{0,1}$/gm
		//cconst regex = /.*?(?:(Alex Lee|Alex Jihun Lee|Alex J Lee|Lee, A\.|Lee, A\. J\.|Alex J\. Lee|Alex J\. Lee|Lee, Alex J\.|Alex J\. Lee).*)?\({0,1}.*(20\d{2})\).*https:\/\/doi.org\/(.*\d)>.*$/gm
		const regex = /(?:.*(Alex Lee|Lee, Alex J\.|Alex Jihun Lee|Alex J\. Lee))?.*(20\d{2})\)(?:.+(https:.*[^>]\d))?/gm
		const regex_search = regex.exec(item);
		//(Alex Lee|Alex J Lee|Alex J. Lee).*\({0,1}(20\d{2})\){0,1},.*(https:.*)>
		if (regex_search == null) {
			console.log('nomatch', item)
			postPromises.push({
				text: item,
				myName: null,
				type: typeOfItem,
				year: null,
				doi: null,
				doiSymbol: null
			})
		} else {
			//my_name = regex_search[1];
			let [match, myName, year, doi] = regex_search

			let entry;
			if (myName == null) {
				entry = item.replace('and others', 'and others <span class="font-bold dark:text-white"> (and me!) </span>')

			}
			else {
				entry = item.replace(myName, '<span class="font-bold dark:text-white">' + myName + '</span>')
			}

			entry = entry.replace(year, '<i>' + year + '</i>');

			let doiSymbol;

			// TDDO: check if v2, v3 exist etc.
			if (match.includes('bioRxiv')) {
				doiSymbol = 'https://www.biorxiv.org/content/' + doi + 'v1.full.pdf+html'
				//https://www.biorxiv.org/content/10.1101/2023.03.10.531984v1.full.pdf+html
			}			// 10.48550arXiv.2303.16725
			else if (doi != undefined) {
				console.log('issue', doi)

				doiSymbol = doi.replace('/', '');
				doiSymbol = doiSymbol.replace('https://doi.org', '')
			}

			postPromises.push({
				text: entry,
				type: typeOfItem,
				myName: myName,
				year: year,
				doi: doi,
				doiSymbol: doiSymbol,
			})
		}
	}
}

export async function GET({ url }) {

	// const paper_modules = await import(`/src/routes/research/papers.md`);
	// const content = paper_modules.default;
	// const metadata = paper_modules.metadata;

	// const papers = [];

	// //console.log(paper_modules.default.render())

	const papers = await fs.readFile(`src/routes/research/papers.md`, { encoding: 'utf-8' });
	const papers_array = papers.split(/\r?\n|\r|\n/g);
	const paperPromises = [];

	await readPaperFile("./src/routes/research/papers.md", paperPromises, "paper")
	await readPaperFile("./src/routes/research/preprints.md", paperPromises, "preprint")
	await readPaperFile("./src/routes/research/conference.md", paperPromises, "conference")

	// for (let [index, item] of Object.entries(papers_array)) {
	// 	if (!item) {
	// 		continue
	// 	}

	// 	const regex = /(Alex Lee|Alex J Lee|Alex J. Lee).*\({0,1}(20\d{2})\){0,1}.*(https.*\d)>{0,1}$/gm
	// 	const regex_search = regex.exec(item);
	// 	//(Alex Lee|Alex J Lee|Alex J. Lee).*\({0,1}(20\d{2})\){0,1},.*(https:.*)>
	// 	if (regex_search == null) {
	// 		paperPromises.push({
	// 			text: item,
	// 			type: 'paper',
	// 			year: null,
	// 			doi: null
	// 		})
	// 	} else {
	// 		//my_name = regex_search[1];
	// 		let [, myName, year, doi] = regex_search
	// 		const entry = item.replace(myName, '<b>' + myName + '</b>')

	// 		paperPromises.push({
	// 			text: entry,
	// 			type: 'paper',
	// 			year: year,
	// 			doi: doi

	// 		})
	// 	};



	// 		myname = regex_search[1];
	// 		year = regex_search[2];
	// 		doi = regex_search[3];
	// 		entry = item.replace(myname, '<b>' + myname + '</b>')

	// 		// paperPromises.push({
	// 		// 	type: 'paper',
	// 		// 	text: entry,
	// 		// 	year: year,
	// 		// 	doi: doi
	// 		// })
	// 	}

	//paperPromises.push(item);
	//}

	return json({ ...paperPromises })
	//return json({ 'abcdf': 'abcdef', 'p': paperPromises, 'd': existsSync("./src/routes/research/papers.md") });

	// 	const regex = /(.*)(Alex Lee|Alex J Lee|Alex J. Lee)(.*)(https:.*)./
	// 	const regex_search = regex.exec(item);

	// 	if (regex_search == null) {
	// 		paperPromises.push({ item: item, details: {}, year: year })

	// 	} else {
	// 		const url = regex_search[4]
	// 		const after_name = regex_search[3]
	// 		const name = regex_search[2]
	// 		const before_name = regex_search[1]

	// 		paperPromises.push({
	// 			type: 'paper',
	// 			item: item,
	// 			year: year,
	// 			details: { before_name: before_name, name: name, after_name: after_name, url: url }
	// 		})
	// 	}
	// };


	// return { paperPromises };
	// const modules = import.meta.glob('/src/routes/research/*.{md,svx,svelte.md}');
	// const iterablePostFiles = Object.entries(modules);

	// const allPosts = await Promise.all(
	// 	iterablePostFiles.map(async ([path, resolver]) => {
	// 		const resolvedPost = await resolver();
	// 		const body = resolvedPost.default.render(); // this is the compiled HTML
	// 		const slug = slugFromPath(path);
	// 		// const md = await compile(body.html, { remarkPlugins, rehypePlugins });
	// 		//console.log(md);
	// 		const metadata = resolvedPost.metadata;
	// 		//console.log(metadata.category);

	// 		return {
	// 			// meta: resolvedPost.metadata,
	// 			slug: slug,
	// 			...resolvedPost.metadata,
	// 			//extra: md,
	// 			//...metadata,
	// 			// body: body,
	// 			md: body,
	// 		};
	// 	})
	// );
	// //console.log(allPosts);

	// const sortedPosts = allPosts.sort((a, b) => {
	// 	return new Date(b.date) > new Date(a.date);
	// })

	//return json(sortedPosts);

};

