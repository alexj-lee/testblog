import grayMatter from 'gray-matter';
import { promises as fs } from 'fs';
import { basename, resolve } from 'path';

/**
 * @param {string | number} text
 * @returns {string}
 */
function slugify(text) {
	return text
		.toString()
		.normalize('NFKD')
		.toLowerCase()
		.trim()
		.replace(/\s+/g, '-')
		.replace(/[^\w-]+/g, '')
		.replace(/--+/g, '-')
		.replace(/(^-|-$)/g, '');
}

/**
 * @param {string} text
 * @returns {string}
 */
function readingTime(text) {
	let minutes = Math.ceil(text.trim().split(' ').length / 225);
	return minutes > 1 ? `${minutes} minutes` : `${minutes} minute`;
}

export const slugFromPath = (path) => path.match(/([\w-]+)\.(svelte\.md|md|svx)/i)?.[1] ?? null;

export async function getPost(slug) {
	const post = await import(`../routes/content/${slug}.md`);
	const { render } = await import('svelte/server');
	const content = render(post.default).body;
	const metadata = post.metadata;

	return {
		content,
		...metadata
	};
}

export async function listBlogposts() {
	let content = [];
	for await (const _path of getFiles('content')) {
		const src = await fs.readFile(_path, 'utf8');
		const data = grayMatter(src);
		content.push({
			content: data.content,
			data: data.data,
			slug: data.data.slug ?? basename(_path, '.md')
		});
	}
	return content;
}

async function* getFiles(dir) {
	const dirents = await fs.readdir(dir, { withFileTypes: true });
	for (const dirent of dirents) {
		const res = resolve(dir, dirent.name);
		if (dirent.isDirectory()) {
			yield* getFiles(res);
		} else {
			yield res;
		}
	}
}
