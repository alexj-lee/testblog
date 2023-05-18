<script>
	// const item = fs.readFile('static/identifiability-vae-presentation/idvae.html', { encoding: 'utf-8' });
	// export let data;
	// $: items = data.items;
	import Reveal from 'reveal.js';
	import { onMount, tick } from 'svelte';

	let document = `
	<div class="reveal">
		<div class="slides">
			<section>
				<a href="https://revealjs.com">
					<img
						src="https://static.slid.es/reveal/logo-v1/reveal-white-text.svg"
						alt="reveal.js logo"
						style="height: 180px; margin: 0 auto 4rem auto; background: transparent;"
						class="demo-logo"
					/>
				</a>
				<h3>The HTML Presentation Framework</h3>
				<p>
					<small
						>Created by <a href="http://hakim.se">Hakim El Hattab</a> and
						<a href="https://github.com/hakimel/reveal.js/graphs/contributors">contributors</a
						></small
					>
				</p>
			</section>

			<section>
				<h2>Hello There</h2>
				<p>
					reveal.js enables you to create beautiful interactive slide decks using HTML. This
					presentation will show you examples of what it can do.
				</p>
			</section>
		</div>
		`;
	onMount(async () => {
		await tick();

		const deck = new Reveal();
		deck.initialize();
	});
</script>

something

<!-- <iframe src="/identifiability-vae-presentation/test.html">
</iframe>  -->

<!-- <iframe>
	</div> -->
<!-- <iframe srcdoc="{document}"></iframe> -->
<iframe
	class="h-96 max-h-96"
	src="https://alexj-lee.github.io/identifiability-vae-presentation/idvae#/title-slide"
/>
