<script>
	import {
		DEFAULT_OG_IMAGE,
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
	<!-- <link rel="alternate" type="application/rss+xml" href={SITE_URL + '/rss.xml'} /> -->
	<meta property="og:url" content={SITE_URL} />
	<meta property="og:type" content="article" />
	<meta property="og:title" content={SITE_TITLE} />
	<meta name="Description" content={SITE_DESCRIPTION} />
	<meta property="og:description" content={SITE_DESCRIPTION} />
	<meta property="og:image" content={DEFAULT_OG_IMAGE} />
	<meta name="twitter:card" content="summary" />
	<meta name="twitter:title" content={SITE_TITLE} />
	<meta name="twitter:description" content={SITE_DESCRIPTION} />
	<meta name="twitter:image" content={DEFAULT_OG_IMAGE} />
</svelte:head>

<div
	class="mx-auto flex max-w-2xl flex-col items-start
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
					And this is my personal blog. I recently graduated from my PhD in computational biology
					and deep learning in the Abbasi lab at UCSF and am working at Calico Life Sciences a machine
					learning research scientist. I previously worked in the Seeley lab (multimodal imaging
					studies of neurodegeneration) and at a startup called Nano Precision Medical (engineering
					titanium nanostructures for ultralong subcutaneous GLP-1RA delivery).
				</h2>

				<h2 in:fade={{ delay: 1400, duration: 2000 }} class="mb-4 text-gray-700 dark:text-gray-200">
					Please enjoy this image of a protein wiggling around, PDB ID
					<a href="https://www.rcsb.org/structure/1JRJ">1jrj</a>. I worked on this protein
					for a couple years at Nano doing biophysical characterization and working
					to keep it stable for months and months--a fun fact is that the tryptophan cage structure
					here is one of the smallest tertiary folds (α-helix, 3₁₀-helix, and polyproline 
					motif all in ~20 AA) we know of, making it an excellent candidate for biophysical
					studies. 
				</h2>

				<div>
					<img
						src="/1jrj-d80_minsize_1mb_backup.webp"
						alt="Animated visualization of a protein wiggling around, PDB ID 1jrj."
						width="380"
						height="586"
						class="protein-img protein-fade-in"
					/>
				</div>
			</div>

		</div>
	{/if}

	<!-- <Newsletter /> -->
</div>
