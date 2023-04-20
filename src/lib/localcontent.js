import { promises as fs } from 'fs';
import grayMatter from 'gray-matter';
import { basename, resolve } from 'path';

export const slugFromPath = (path) => path.match(/([\w-]+)\.(svelte\.md|md|svx)/i)?.[1] ?? null;

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
