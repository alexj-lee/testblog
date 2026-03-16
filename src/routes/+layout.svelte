<script>
	import { MY_TWITTER_HANDLE, SITE_URL, SITE_TITLE } from '$lib/siteConfig';
	import Nav from '../components/Nav.svelte';
	import '../tailwind.css';

	const jsonLd = {
		'@context': 'https://schema.org',
		'@graph': [
			{
				'@type': 'WebSite',
				name: SITE_TITLE,
				url: SITE_URL
			},
			{
				'@type': 'Person',
				name: 'Alex J. Lee',
				url: SITE_URL,
				sameAs: [
					'https://github.com/alexj-lee',
					'https://orcid.org/0000-0003-0001-2848',
					'https://scholar.google.com/citations?user=fMdvjhkAAAAJ'
				],
				jobTitle: 'PhD Student',
				affiliation: [
					{ '@type': 'Organization', name: 'UCSF' },
					{ '@type': 'Organization', name: 'Calico Life Sciences' }
				]
			}
		]
	};
</script>

<svelte:head>
	{@html '<script type="application/ld+json">' + JSON.stringify(jsonLd) + '</script>'}
	<!-- <link
		rel="alternate"
		type="application/rss+xml"
		title={'RSS Feed for ' + SITE_TITLE}
		href="/rss.xml"
	/> -->
</svelte:head>

<div class="flex flex-col justify-center bg-emerald-50 px-4 dark:bg-gray-900 sm:px-8">
	<Nav />
</div>

<main class="flex flex-col justify-center bg-emerald-50 px-4 dark:bg-gray-900 sm:px-8">
	<slot />
</main>

<footer class="mx-auto mb-8 flex w-full max-w-2xl flex-col items-start justify-center">
	<hr class="border-1 mb-8 w-full border-gray-200 dark:border-gray-800" />
	<div class="grid w-full max-w-2xl grid-cols-1 gap-4 px-4 pb-16 sm:grid-cols-2 sm:px-8">
		<div class="flex flex-col space-y-4">
			<a class="text-gray-500 transition hover:text-gray-300" href="/">Home</a>
			<a class="text-gray-500 transition hover:text-gray-300" href="/about">About</a>
			<!-- <a class="text-gray-500 transition hover:text-gray-300" href="/#newsletter">Newsletter</a> -->
			<!-- <a class="text-gray-500 transition hover:text-gray-300" href="/rss.xml" rel="external">
				RSS
			</a> -->
		</div>
		<div class="flex flex-col space-y-4">
			<a
				class="text-gray-500 transition hover:text-gray-300"
				target="_blank"
				rel="noopener noreferrer"
				href={'https://twitter.com/' + MY_TWITTER_HANDLE}
			>
				Twitter
			</a>
			<a
				class="text-gray-500 transition hover:text-gray-300"
				target="_blank"
				rel="noopener noreferrer"
				href="https://github.com/alexj-lee"
			>
				GitHub
			</a>
		</div>
	</div>
	<p class="prose px-4 dark:prose-invert sm:px-8">
		This blog is based on the
		<a href="https://swyxkit.netlify.app/">swyxkit</a>
		template.
	</p>
</footer>
