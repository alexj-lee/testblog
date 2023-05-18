# alexblog

Based on a lightly opinionated starter for [SvelteKit](https://kit.svelte.dev/) blogs:

## TODO:
- 2023-05-15: 
  - [ x ] change ToC to be the old one
  - change coloring on bottom nav bar links (non-mobile) to be gray
  - allow CSS for blogs to have first introduction have # 
  - allow PDF viewer and PDF download for science page
  - allow low motion mode
  - [ x ] remove About from bottom nav bar
  - sanitize HTML from search bar and allow more granular search

## For svelte rendering:
- I think I can just use something like: https://github.com/huijing/slides and just use this strategy: https://svelte.dev/repl/32f4d35f41eb4914aa3be5e4a0eacbfa?version=3.59.1

I think what I need to do here is create a separate api to load the reveal files and then access that from the load() function in page.js

Or maybe something like: https://stackoverflow.com/questions/56354228/how-can-i-encapsulate-svelte-app-within-iframe-of-svelte-app