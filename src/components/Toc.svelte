<script lang="ts">
	// copied from https://github.com/janosh/svelte-toc
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { blur } from 'svelte/transition';

	export let headingSelector = `main :where(h1, h2, h3, h4):not(.toc-exclude)`;
	export let getHeadingTitles = (node: HTMLHeadingElement): string => node.innerText;
	export let getHeadingIds = (node: HTMLHeadingElement): string => node.id;
	export let getHeadingLevels = (node: HTMLHeadingElement): number => Number(node.nodeName[1]); // get the number from H1, H2, ...
	export let activeHeading: HTMLHeadingElement | null = null;
	export let open = true;
	export let title = `On this page`;
	export let openButtonLabel = `Open table of contents`;
	export let breakpoint = 1000;
	export let flashClickedHeadingsFor = true;
	export let keepActiveTocItemInView = false;
	export let activeTopOffset = 400;

	let windowWidth: number;
	let windowHeight: number;
	let headings: HTMLHeadingElement[] = [];
	let aside: HTMLElement;
	$: levels = headings.map(getHeadingLevels);
	$: minLevel = Math.min(...levels);

	function goTop(e) {
		window.scrollTo({ top: 0, behavior: `smooth` });
	}

	function close(event: MouseEvent) {
		if (!aside.contains(event.target as Node)) open = false;
	}

	// (re-)query headings on mount and on route changes
	function requery_headings() {
		if (typeof document === `undefined`) return; // for SSR safety
		headings = [...document.querySelectorAll(headingSelector)] as HTMLHeadingElement[];
		setActiveHeading();
	}

	page.subscribe(requery_headings);
	onMount(requery_headings);

	function setActiveHeading() {
		let idx = headings.length;
		while (idx--) {
			const { top } = headings[idx].getBoundingClientRect();

			// loop through headings from last to first until we find one that the viewport already
			// scrolled past. if none is found, set make first heading active
			if (top < activeTopOffset || idx === 0) {
				activeHeading = headings[idx];
				if (keepActiveTocItemInView) {
					// get the currently active ToC list item
					const activeTocLi = document.querySelector(`aside.toc > nav > ul > li.active`);
					activeTocLi?.scrollIntoView({ block: `nearest` });
				}
				return;
			}
		}
	}

	const clickHandler = (node: HTMLHeadingElement) => () => {
		open = false;
		// Chrome doesn't (yet?) support multiple simultaneous smooth scrolls (https://stackoverflow.com/q/49318497)
		// with node.scrollIntoView(). Use window.scrollTo() instead.
		const scrollMargin = Number(getComputedStyle(node).scrollMarginTop.replace(`px`, ``));
		window.scrollTo({ top: node.offsetTop - scrollMargin, behavior: `smooth` });

		const id = getHeadingIds && getHeadingIds(node);
		if (id) history.replaceState({}, ``, `#${id}`);

		if (flashClickedHeadingsFor) {
			node.classList.add(`toc-clicked`);
			setTimeout(() => node.classList.remove(`toc-clicked`), flashClickedHeadingsFor);
		}
	};

	const getPrefix = (node: HTMLHeadingElement) => {
		if (node.tagName == 'H1') {
			return '';
		} else if (node.tagName == 'H2') {
			return '─';
		} else {
			const increments = Number(node.tagName.slice(1, 2));
			return '\u00A0'.repeat(increments * 1.5) + '└' + '─'.repeat(increments - 2);
			// return '└─';
		}
	};
</script>

<svelte:window
	bind:innerWidth={windowWidth}
	bind:innerHeight={windowHeight}
	on:scroll={setActiveHeading}
	on:click={close}
/>

<aside class="toc fixed left-4 top-72 max-w-[20em] rounded-xl" bind:this={aside}>
	<div class="invisible flex flex-col text-gray-900 dark:text-gray-100 md:visible">
		{#if true}
			<div class="flex pl-5">
				<span> Contents: <br /> <br /> </span>
			</div>
			<nav transition:blur|local>
				<ul class="inline-block flex-col space-y-0">
					{#each headings as heading, idx}
						<li
							class="ml-1 mb-1 inline-block pl-1 pb-1"
							tabindex={idx + 1}
							class:active={activeHeading === heading}
							on:click={clickHandler(heading)}
						>
							<slot name="tocItem" {heading} {idx}>
								{getPrefix(heading)}
								{getHeadingTitles(heading)}
							</slot>
						</li>
						<!-- <div>
							<br />
						</div> -->
					{/each}
				</ul>
				<div class="flex items-center justify-center">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-7 w-7"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						on:click={goTop}
					>
						<path strokeLinecap="round" strokeLinejoin="round" d="M5 15l7-7 7 7" />
					</svg>
				</div>
			</nav>
		{/if}
	</div>
</aside>

<style>
	:where(aside.toc > div > nav > ul > li.active) {
		font-weight: normal;
		text-shadow: 0.15px 0.15px;
		border-left: 2px solid #65a98f;
		border-bottom: 3px solid #65a98f;
	}
</style>
