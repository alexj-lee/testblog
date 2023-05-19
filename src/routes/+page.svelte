<script>
	import {
		DEFAULT_OG_IMAGE,
		MY_TWITTER_HANDLE,
		SITE_DESCRIPTION,
		SITE_TITLE,
		SITE_URL
	} from '$lib/siteConfig';
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';

	/** @type {import('./$types').PageData} */
	export let data;
	// technically this is a slighlty different type because doesnt have 'content' but we'll let it slide
	/** @type {import('$lib/types').ContentItem[]} */
	// $: items = data.items;

	let mounted = false;
	onMount(() => (mounted = true));
</script>

<svelte:head>
	<title>{SITE_TITLE}</title>
	<link rel="canonical" href={SITE_URL} />
	<link rel="alternate" type="application/rss+xml" href={SITE_URL + '/rss.xml'} />
	<meta property="og:url" content={SITE_URL} />
	<meta property="og:type" content="article" />
	<meta property="og:title" content={SITE_TITLE} />
	<meta name="Description" content={SITE_DESCRIPTION} />
	<meta property="og:description" content={SITE_DESCRIPTION} />
	<meta property="og:image" content={DEFAULT_OG_IMAGE} />
	<meta name="twitter:card" content="summary" />
	<meta name="twitter:creator" content={'@' + MY_TWITTER_HANDLE} />
	<meta name="twitter:title" content={SITE_TITLE} />
	<meta name="twitter:description" content={SITE_DESCRIPTION} />
	<meta name="twitter:image" content={DEFAULT_OG_IMAGE} />
</svelte:head>

<div
	class="whitespace-break-spaces mx-auto flex max-w-2xl flex-col items-start
	 justify-center border-gray-200 pb-16 dark:border-gray-700 sm:px-4"
>
	{#if mounted}
		<div class="flex flex-col-reverse items-start sm:flex-row">
			<div class="flex flex-col pr-8">
				<h1
					in:fade={{ delay: 600, duration: 2000 }}
					class="mb-3 text-3xl font-bold tracking-tight text-black dark:text-white md:text-5xl"
				>
					Hi, my name is
					<span
						class="relative ml-2 inline-block before:absolute before:-inset-1 before:block before:-skew-y-3 before:bg-artemesia"
					>
						<span class="relative skew-y-3 text-white">alex</span>
					</span>
					!
				</h1>
				<h2 in:fade={{ delay: 600, duration: 2000 }} class="mb-4 text-gray-700 dark:text-gray-200">
					And this is my personal blog. I'm currently a grad student in the Abbasi lab at UCSF, and
					previously worked in the Seeley lab and at a startup called Nano Precision Medical.

					<br /> <br /> Please enjoy this image of a protein wiggling around, PDB ID
					<a href="https://www.rcsb.org/structure/1JRJ">1jrj</a>.
				</h2>

				<div>
					<img
						in:fade={{ delay: 1200, duration: 2500 }}
						src="/1jrj-d80_minsize.webp"
						alt="A video of a protein wiggling around."
						class="block
						max-w-sm scale-100
						bg-transparent opacity-90 brightness-125 dark:bg-transparent
						dark:opacity-100
						dark:brightness-110
						"
					/>
				</div>
			</div>

			<!-- <div
				class="w-[80px] h-[80px] rounded-full sm:w-[176px] sm:h-[136px] relative mb-8 sm:mb-0 mr-auto bg-cyan-300 bg-opacity-25"
			/> -->
		</div>
	{/if}

	<!-- <section class="w-full mb-16">
		<h3 class="mb-6 text-2xl font-bold tracking-tight text-black dark:text-white md:text-4xl">
			Featured Posts
		</h3>
		<div class="flex flex-col gap-6 md:flex-row">
			<FeatureCard title="Welcome to swyxkit 2022!" href="/welcome" stringData="Jan 2022" />
			<FeatureCard
				title="Moving to a GitHub CMS"
				href="/moving-to-a-github-cms"
				stringData="Jan 2022"
			/>
			<FeatureCard title="HTML Ipsum demo" href="/moo" stringData="Jan 2022" />
		</div>
	</section>

	<LatestPosts {items} /> -->

	<!-- <Newsletter /> -->
</div>
