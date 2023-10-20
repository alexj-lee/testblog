<script>
	import { MY_TWITTER_HANDLE, SITE_URL } from '$lib/siteConfig';
	// import Comments from '../../components/Comments.svelte';

	import { page } from '$app/stores';
	import 'prism-themes/themes/prism-nord.min.css';
	// https://svelte-put.vnphanquang.com/docs/toc
	import { createTocStore } from '@svelte-put/toc';
	// table of contennts
	const tocStore = createTocStore();

	/** @type {import('./$types').PageData} */
	export let data;

	/** @type {import('$lib/types').ContentItem} */
	$: json = data.json; // warning: if you try to destructure content here, make sure to make it reactive, or your page content will not update when your user navigates
	//export let commentsEl;
	$: issueNumber = json?.ghMetadata?.issueUrl?.split('/')?.pop();

	$: canonical = json?.canonical ? json.canonical : SITE_URL + $page.url.pathname;

	// customize this with https://tailgraph.com/
	// discuss this decision at https://github.com/sw-yx/swyxkit/pull/161
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

	<link
		rel="stylesheet"
		href="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css"
		crossorigin="anonymous"
	/>
</svelte:head>

<article
	class="swyxcontent prose mx-auto mt-16 mb-32 
	w-full max-w-2xl items-start justify-center 
	dark:prose-invert "
>
	<h1
		class="mb-8 text-center text-3xl font-bold tracking-tight text-black dark:text-white sm:text-center md:text-5xl"
	>
		{json.title}
	</h1>

	<div class="flex items-center justify-center">
		<span> Written: {json.date} by {json.author}</span>
	</div>

	<div
		class="bg border-red mt-2 flex w-full justify-between sm:items-start md:flex-row md:items-center"
	>
		<!-- <p class="flex items-center text-sm text-gray-700 dark:text-gray-300">{json.author}</p> -->
		<p class="flex items-center text-sm text-gray-600 dark:text-gray-400">
			<!-- <span class="mr-4 font-mono text-xs text-gray-700 text-opacity-70 dark:text-gray-300"
					>{json.ghMetadata.reactions.total_count} reactions</span
				> -->
		</p>
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
	<!-- <div
		class="max-w-1/8 center -mx-3 
my-2 flex h-1 w-1 bg-gradient-to-r
from-artemesia via-sulphur to-cameopink sm:mx-0 sm:w-1/2"
	/> -->

	<br />
	<div class="not-prose h-full w-full max-w-none overflow-hidden">
		<iframe
			class="feature not-prose h-96 max-h-96 w-full max-w-none"
			frameborder="1px"
			scrolling="no"
			title="A survey of sequence models for proteins"
			src="https://alexj-lee.github.io/identifiability-vae-presentation/idvae#/title-slide"
		/>
	</div>

	<br />

	{@html json.content}
</article>
