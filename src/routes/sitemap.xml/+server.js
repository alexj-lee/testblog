import { SITE_URL } from '$lib/siteConfig';

export const prerender = true;

export async function GET() {
	const modules = import.meta.glob('/src/routes/content/*.{md,svx,svelte.md}');
	const posts = await Promise.all(
		Object.entries(modules).map(async ([path, resolver]) => {
			const post = await resolver();
			const meta = post.metadata ?? {};
			const slug = path.split('/').pop().replace(/\.(md|svx|svelte\.md)$/, '');
			return {
				slug,
				date: meta.date,
				published: meta.published
			};
		})
	);

	const publishedPosts = posts
		.filter((p) => p.published !== false)
		.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

	const staticPages = ['', '/science', '/blog', '/snippets', '/about'];

	const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${staticPages
	.map(
		(page) => `  <url>
    <loc>${SITE_URL}${page}</loc>
  </url>`
	)
	.join('\n')}
${publishedPosts
	.map(
		(post) => `  <url>
    <loc>${SITE_URL}/posts/${post.slug}</loc>
    ${post.date ? `<lastmod>${new Date(post.date).toISOString().slice(0, 10)}</lastmod>` : ''}
  </url>`
	)
	.join('\n')}
</urlset>`;

	return new Response(sitemap.trim(), {
		headers: {
			'Content-Type': 'application/xml'
		}
	});
}
