############ KEEP GOOGLE SEARCH REQUESTS LIMIT TO 20 PER HOUR...

import requests
from bs4 import BeautifulSoup

def get_google_search_results_urls(query):
    search_url = f"https://www.google.com/search?q={query}"
    
    # Send an HTTP request to the Google search page
    response = requests.get(search_url)
    # print(response.content)
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    # print('='*300, soup)
    
    # Extract the URLs from the search results
    search_results = []
    for link in soup.find_all("a"): # finding all <a/> html elements in code
        href = link.get("href")
        if href.startswith("/url?q="):
            url = href[7:].split("&")[0]  # Extract the URL from the href attribute
            search_results.append(url)
    
    return search_results

def main():
    query = "best albums year 2016"
    search_results = get_google_search_results_urls(query)
    
    # Print the extracted URLs; search_results is a list
    for url in search_results:
        print(url)

if __name__ == "__main__":
    main()