fully working, may need to clean up searches that dont match, or leave as is and clean up manually in spotify while storing the albums that dont match from code.

TODO
        - for main code:
                - only add matching albums on spotify, if not found don't add (but store in text file missing album)
                - ideally, only add original songs from albums, no deluxe/ultimate/bonus/live tracks
                        - maybe to avoid deluxe albums, return 2-3 album results, and grab best matching album
        - create code to always get a new token once the old token expires
        - fix timeout error occurring related to requests package not communicating w/spotify api correctly resuling in timeout error
        - create a word/excel file or csv to store all artists and album and year info

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