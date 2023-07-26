import requests
from bs4 import BeautifulSoup

# Step 1: Perform Google search and extract relevant URLs
def google_search(query):
    # Your code here to perform the Google search and extract relevant URLs
    search_results = []  # List of relevant URLs from the search results
    return search_results

# Step 2-5: Web scraping and storing the data
def scrape_album_data(url):
    # Your code here to send HTTP request, parse HTML, and extract album data
    album_data = {
        'year': 2016,  # Extract the year from the webpage or set it to 2016
        'rank': 1,     # Extract the rank from the webpage or set it based on the order of search results
        'artist': 'Artist Name',  # Extract the artist name from the webpage
        'album': 'Album Name'     # Extract the album name from the webpage
    }
    return album_data

def main():
    query = 'best albums year 2016'
    search_results = google_search(query)
    scraped_albums = []

    for url in search_results:
        album_data = scrape_album_data(url)
        if album_data:
            scraped_albums.append(album_data)

    # Step 6: Append all albums into an ordered list in ascending order by the album rank
    sorted_albums = sorted(scraped_albums, key=lambda x: x['rank'])

    # Print the sorted list of albums
    for album in sorted_albums:
        print(f"Rank: {album['rank']}, Artist: {album['artist']}, Album: {album['album']}")

if __name__ == '__main__':
    main()
