
import uFuzzy from '@leeoniya/ufuzzy';

// https://github.com/leeoniya/uFuzzy#options
const u = new uFuzzy({ intraMode: 1 });

// debounce async function returning a promise
// https://dev.to/gabe_ragland/debouncing-with-async-await-in-js-26ci
function debounce(func, wait) {
  let timeout;
  return (...args) => {
    const context = this;
    return new Promise((resolve, reject) => {
      const later = () => {
        timeout = null;
        resolve(func.apply(context, args));
      };
      const callNow = !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) resolve(func.apply(context, args));
    });
  };
};



/**
 * @param {import('$lib/types').ContentItem[]} items
 * @param {string[]} selectedCategories
 * @param {string} search
 * @return {Object[]}
 */
function _fuzzySearch(items, selectedCategories, search) {
  // console.log('---start---')
  // console.log('items', items);
  // console.log('categories', selectedCategories);
  // console.log('search', search);

  const filteredItems = items.filter((item) => {
    if (selectedCategories?.length < 1) return true
    return selectedCategories
      .map((element) => {
        return element.toLowerCase();
      })
      .includes(item.category.toLowerCase());
  })
  if (search) {
    const haystack = filteredItems.map((v) =>
      [
        v.title,
        // v.subtitle,
        v.md.html,
        v.description,
        v.tags.map((tag) => 'hashtag-' + tag), // add #tag so as to enable tag search

      ].join(' ')
    );
    // console.log('haystack', haystack);
    // console.log('---end---')

    const idxs = u.filter(haystack, search);
    const info = u.info(idxs, haystack, search);
    const order = u.sort(info, haystack, search);
    //const mark = (part, matched) => matched ? '<b style="color:#f5f5b8">' + part + '</b>' : part;
    const mark = (part, matched) => matched ? '<b>' + part + '</b>' : part;

    const list = order.map(i => {
      const x = filteredItems[info.idx[order[i]]]
      let filtered_item = haystack[info.idx[order[i]]];
      const hl = uFuzzy.highlight(
        haystack[info.idx[order[i]]]
          .replaceAll("<", " ")
          .replaceAll("/>", " ")
          .replaceAll(">", " "),
        // sanitize html as we dont actually want to render it
        info.ranges[order[i]],
        mark
      )
        // highlight whats left
        .slice(Math.max(info.ranges[order[i]][0] - 200, 0), Math.min(info.ranges[order[i]][1] + 200, haystack[info.idx[order[i]]].length))
        // slice clean words
        .split(' ').slice(1, -1).join(' ')

      console.log('hl', hl, 'next', haystack[info.idx[order[i]]])
      //const x_filt = x.replaceAll("<", " ").replaceAll("/>", " ").replaceAll("<", " ").replaceAll(">", " ")
      return { ...x, highlightedResults: hl }
    })
    return list
  } else {
    // console.log('filtereditems', filteredItems);
    return filteredItems
  }
}

export function fuzzySearch(items, selectedCategories, search) {
  return debounce(_fuzzySearch, 100)(items, selectedCategories, search)
}