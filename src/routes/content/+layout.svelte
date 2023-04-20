<!-- <script context="module"> 
<script context="module">
	import { REPO_URL, SITE_TITLE } from '$lib/siteConfig';
	import Nav from '../../components/Nav.svelte';
	import '../../tailwind.css'; -->
<!-- <script>
	import Toc from '../../components/Toc.svelte';
</script> -->

<script>

</script>

<svelte:head>
		<link
		rel="stylesheet"
		href="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css"
		crossorigin="anonymous"
	/>
</svelte:head>


<main class="">
	<!-- <Toc /> -->

	<slot />
</main>
