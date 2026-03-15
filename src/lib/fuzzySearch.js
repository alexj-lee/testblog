import uFuzzy from '@leeoniya/ufuzzy';

const u = new uFuzzy({ intraMode: 1 });

const STRIP_HTML = /<[^>]*>/g;

/**
 * @param {import('$lib/types').ContentItem[]} items
 * @param {string[]} selectedCategories
 * @param {string} search
 * @return {Object[]}
 */
export function fuzzySearch(items, selectedCategories, search) {
	const filteredItems = items.filter((item) => {
		if (!selectedCategories?.length) return true;
		return selectedCategories
			.map((c) => c.toLowerCase())
			.includes(item.category.toLowerCase());
	});

	if (!search) return filteredItems;

	const haystack = filteredItems.map((v) =>
		[
			v.title,
			v.md?.html?.replace(STRIP_HTML, ' ') ?? '',
			v.description,
			v.tags?.map((tag) => 'hashtag-' + tag).join(' ') ?? ''
		].join(' ')
	);

	const idxs = u.filter(haystack, search);
	if (!idxs?.length) return [];

	const info = u.info(idxs, haystack, search);
	const order = u.sort(info, haystack, search);
	const mark = (part, matched) => (matched ? '<b>' + part + '</b>' : part);

	return order.map((i) => {
		const idx = info.idx[order[i]];
		const item = filteredItems[idx];
		const range = info.ranges[order[i]];
		const text = haystack[idx].replace(STRIP_HTML, ' ');

		const hl = uFuzzy
			.highlight(text, range, mark)
			.slice(Math.max(range[0] - 200, 0), Math.min(range[1] + 200, text.length))
			.split(' ')
			.slice(1, -1)
			.join(' ');

		return { ...item, highlightedResults: hl };
	});
}
