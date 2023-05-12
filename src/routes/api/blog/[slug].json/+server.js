import { getBlogpost, getPost } from '$lib/content';
import { error } from '@sveltejs/kit';
/**
 * @type {import('@sveltejs/kit').RequestHandler}
 */
export async function GET({ fetch, params }) {
	const { slug,
		title,
		author,
		description,
		date,
		youtube,
		link,
	} = params;
	//const { slug } = params;
	let data;

	try {
		//data = await getBlogpost(slug);
		data = await getPost(slug);

		//let res = (await fetch(`/api/localPosts.json`)).json();
		//console.log('res is');
		//console.log(Object.keys(res));
		//console.log(data.md.md);

		let content = { content: data };

		Object.assign(content, {
			title: 'titlalexe',
			author: author,
			date: date
		});

		//let content_json = JSON.stringify(content);
		let content_json = JSON.stringify(data);

		console.log(Object.keys(data));
		//let json_data = JSON.stringify(data);
		//json_data = { json: json_data };
		//json_data['title'] = title;
		return new Response(content_json, {
			headers: {
				'Cache-Control': '`public, max-age=3600`'
			}
		});

		return new Response(JSON.stringify(data), {
			headers: {
				'Cache-Control': `public, max-age=3600`, // 1 hour
			}
		});
	} catch (err) {
		console.log("didn't find ", slug)
		console.error(err);
		throw error(404, err.message);
	}
}
