<script>
	export let data;

	$: papers = data.papers;
	$: preprints = data.preprints;
	$: conferences = data.conferences;
</script>

<svelte:head>
	<title>papers</title>
	<meta name="description" content="Projects and papers I've worked on" />
</svelte:head>

<div
	class="mx-auto flex max-w-2xl flex-col items-start justify-center border-gray-200 px-4 pb-16 text-gray-900 dark:border-gray-700 dark:text-gray-400 sm:px-8"
>
	<span>
		<a
			class="mt-5 text-3xl text-gray-700 dark:text-gray-300 md:text-4xl"
			href="https://orcid.org/0000-0003-0001-2848"
		>
			<img
				class="mx- my-0 inline-block h-9 w-9 bg-transparent py-0"
				alt="ORCIDiD icon"
				src="ORCIDiD_iconvector.svg"
			/>
			<span class="align-middle">0000-0003-0001-2848</span>
		</a>
		<br /> <br />
	</span>

	<div class="">
		<h1
			class="relative mb-3 text-3xl font-bold tracking-tight text-black dark:text-white md:text-4xl"
		>
			Papers
			<span class="inline-block pt-2 text-sm" />
		</h1>
		<br />
	</div>

	<div class="border-l-4 dark:border-artemesia">
		<ol class="ml-6 list-decimal space-y-4 leading-relaxed">
			{#each papers as paper}
				<li>
					{@html paper.text} [<a href={paper.doi}>doi</a>,
					<a href="pdfs/{paper.doiSymbol}.pdf">pdf</a>]
				</li>
			{/each}
		</ol>
	</div>

	<div class="">
		<br />
		<h1
			class="relative mb-3 text-3xl font-bold tracking-tight text-black dark:text-white md:text-4xl"
		>
			Preprints
		</h1>
		<br />
	</div>

	<div class="border-l-4 dark:border-artemesia">
		<ol class="ml-6 list-decimal space-y-4 leading-relaxed">
			{#each preprints as item}
				<li>{@html item.text} [<a href={item.doi}>doi</a>]</li>
			{/each}
		</ol>
	</div>

	<div class="">
		<br />
		<h1
			class="relative mb-3 text-3xl font-bold tracking-tight text-black dark:text-white md:text-4xl"
		>
			Conference abstracts
		</h1>
		<br />
	</div>

	<div class="border-l-4 dark:border-artemesia">
		<ol class="ml-6 list-decimal space-y-4 leading-relaxed">
			{#each conferences as item}
				<li>{@html item.text} [<a href={item.doi}>doi</a>]</li>
			{/each}
		</ol>
	</div>
</div>
