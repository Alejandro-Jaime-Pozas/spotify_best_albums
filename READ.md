last run:

- searched the google json api | programmable search engine. looks like this is to create a google search box within your website, doesn't look like this helps in retrieving the actual contents of google search results, will have to use scraper?
- started getting acquainted with chatgpt-generated code in script.py. also with the requests package from python.

Edge cases:

	Page bottom cut off: need to click button to get more results (text)

	Multiple pages with results: need to either click button or change url param
        FIXES
        - insert '/page=num', '/num', '/p=num' or something like that in url IF results do not match the title ie '50 best albums'
        - if pages = 5 total, then inputting 6 will return 404, or redirect to other url to quit loop
        - limit this style to 5 pages only (to prevent when there's 50+ pages)

	Slideshow style: each slideshow has different content (how to change?)


Website Issues:

    - some sites 'albumoftheyear' dont have weighted ranking...only 'top' reviews
    - some sites have no number of albums that are top for year (this makes harder to know if and how many pages to search) 
    - many sites use multiple pages to list all albums