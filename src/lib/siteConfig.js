export const SITE_URL = 'https://alexlee.netlify.app';
export const APPROVED_POSTERS_GH_USERNAME = ['alexj-lee'];
export const GH_USER_REPO = 'alexj-lee/website'; // used for pulling github issues and offering comments
export const SITE_TITLE = 'alexblog';
export const SITE_DESCRIPTION = "Alex J. Lee — deep learning for computational biology, spatial transcriptomics, and protein design";
export const DEFAULT_OG_IMAGE =
	'https://user-images.githubusercontent.com/69220428/239652125-ca8f5501-0364-4be7-bc25-9af9adcbc689.png';
export const MY_TWITTER_HANDLE = 'eel__xela';
export const MY_YOUTUBE = '';
export const POST_CATEGORIES = ['Paper', 'Software', 'Blog', "Presentation"]; // Other categories you can consider adding: Talks, Tutorials, Snippets, Podcasts, Notes...
export const GH_PUBLISHED_TAGS = ['Published'];
export const ORCID_ID = '0000-0003-0001-2848'
// auto generated variables
export const REPO_URL = 'https://github.com/' + GH_USER_REPO;
export const REPO_OWNER = GH_USER_REPO.split('/')[0];

// dont forget process.env.GH_TOKEN
// if supplied, raises rate limit from 60 to 5000
// https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting
