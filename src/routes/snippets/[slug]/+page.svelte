<script>
	import { page } from '$app/stores';
	import { MY_TWITTER_HANDLE, SITE_URL } from '$lib/siteConfig';

	export let data;
	$: json = data.json;
	$: canonical = json?.canonical ? json.canonical : SITE_URL + $page.url.pathname;
	$: image =
		json?.image ||
		`https://og.tailgraph.com/og
															?fontFamily=Roboto
															&title=${encodeURIComponent(json?.title)}
															&titleTailwind=font-bold%20bg-transparent%20text-7xl
															&titleFontFamily=Poppins
															${json?.subtitle ? '&text=' + encodeURIComponent(json?.subtitle) : ''}
															&textTailwind=text-2xl%20mt-4
															&logoTailwind=h-8
															&bgUrl=https%3A%2F%2Fwallpaper.dog%2Flarge%2F20455104.jpg
															&footer=${encodeURIComponent(SITE_URL)}
															&footerTailwind=text-teal-900
															&containerTailwind=border-2%20border-orange-200%20bg-transparent%20p-4
															`.replace(/\s/g, ''); // remove whitespace
</script>

<svelte:head>
	<title>{json.title}</title>
	<!-- reference: https://gist.github.com/whitingx/3840905 -->

	<link rel="canonical" href={canonical} />
	<meta property="og:url" content={canonical} />
	<meta property="og:type" content="article" />
	<meta property="og:title" content={json.title} />
	{#if json.subtitle}
		<meta property="subtitle" content={json.subtitle} />
	{/if}
	<meta name="Description" content={json.description || 'swyxkit blog'} />
	<meta property="og:description" content={json.description || 'swyxkit blog'} />
	<meta name="twitter:card" content={json.image ? 'summary_large_image' : 'summary'} />
	<meta name="twitter:creator" content={'@' + MY_TWITTER_HANDLE} />
	<meta name="twitter:title" content={json.title} />
	<meta name="twitter:description" content={json.description} />
	<meta property="og:image" content={image} />
	<meta name="twitter:image" content={image} />
</svelte:head>

<article
	class="swyxcontent prose mx-auto mt-16 mb-32 w-full max-w-2xl items-start justify-center dark:prose-invert"
>
	<h1
		class="mb-8 text-center text-3xl font-bold tracking-tight text-black dark:text-white sm:text-center md:text-5xl"
	>
		{json.title}
	</h1>

	<div class="flex items-center justify-center">
		<span> Written: {json.date}</span>
	</div>

	<div
		class="bg border-red mt-2 flex w-full justify-between sm:items-start md:flex-row md:items-center"
	>
		<!-- <p class="flex items-center text-sm text-gray-700 dark:text-gray-300">{json.author}</p> -->
	</div>

	<div class="mx-auto max-w-2xl">
		{#if json?.tags?.length}
			<p class="mb-4 flex-auto italic !text-slate-400">
				Tagged in:
				{#each json.tags as tag}
					<span class="px-1">
						<a href={`/snippets?filter=hashtag-${tag}`}>#{tag}</a>
					</span>
				{/each}
			</p>
		{/if}
		<!-- <div class="prose mb-12 max-w-full border-t border-b border-blue-800 p-4 dark:prose-invert" /> -->

		<!-- <LatestPosts items={data.list} /> -->
	</div>

	<div class="max-w-1/2 grid justify-items-center">
		<div
			class=" 
			h-1
			w-full max-w-2xl items-center bg-gradient-to-r
			from-artemesia via-sulphur
			to-cameopink object-none object-center "
		/>
	</div>

	<br />

	{@html json.md.html}
</article>

<style>
	/* https://ryanmulligan.dev/blog/layout-breakouts/ */
	.swyxcontent {
		--gap: clamp(1rem, 6vw, 3rem);
		--full: minmax(var(--gap), 1fr);
		/* --content: min(65ch, 100% - var(--gap) * 2); */
		--content: 130ch;
		--popout: minmax(0, 2rem);
		--feature: minmax(0, 5rem);

		display: grid;
		grid-template-columns:
			[full-start] var(--full)
			[feature-start] 0rem
			[popout-start] 0rem
			[content-start] var(--content) [content-end]
			[popout-end] 0rem
			[feature-end] 0rem
			var(--full) [full-end];
	}

	@media (min-width: 768px) {
		.swyxcontent {
			grid-template-columns:
				[full-start] var(--full)
				[feature-start] var(--feature)
				[popout-start] var(--popout)
				[content-start] var(--content) [content-end]
				var(--popout) [popout-end]
				var(--feature) [feature-end]
				var(--full) [full-end];
		}
	}

	:global(.swyxcontent > *) {
		grid-column: content;
	}

	article :global(pre) {
		grid-column: feature;
		margin-left: -1rem;
		margin-right: -1rem;
	}

	/* hacky thing because otherwise the summary>pre causes overflow */
	article :global(summary > pre) {
		max-width: 90vw;
	}

	article :global(.popout) {
		grid-column: popout;
	}
	article :global(.feature) {
		grid-column: feature;
	}
	article :global(.full) {
		grid-column: full;
		width: 100%;
	}

	article :global(.admonition) {
		@apply border-4 border-red-500 p-8;
	}

	/* fix github codefence diff styling from our chosen prismjs theme */
	article :global(.token.inserted) {
		background: #00ff0044;
	}

	article :global(.token.deleted) {
		background: #ff000d44;
	}
</style>
