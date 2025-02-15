import requests
from bs4 import BeautifulSoup
import sys

def scrape_main_wiki_page(show_name):
    """
    Given a show name (e.g., "Sailor Moon"), this function constructs a URL
    like "https://en.wikipedia.org/wiki/Sailor_Moon_(TV_series)", fetches it,
    and prints the first paragraph from the page (if found).
    """
    # 1. Prepare the show name for the URL
    #    Replace spaces with underscores and add "_(TV_series)" at the end.
    formatted_name = show_name.replace(" ", "_")    
    url = f"https://en.wikipedia.org/wiki/{formatted_name}"
    
    print(f"Scraping URL: {url}")
    
    # 2. Send a GET request to the Wikipedia page
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return
    
    # 3. Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    formatted_anchor_title = "List of " + show_name + " episodes"   
    
    
     
    # 4. Find the first paragraph on the page
    episode_list_link = None
    anchor = soup.find("a", title=lambda x: x and x.startswith("List of") and x.endswith("episodes"))    
    if anchor and 'title' in anchor.attrs:
        if show_name in anchor['title']:
            if anchor:
                episode_list_link = anchor['href']
            else:                    
                print(f"Error: Could not find an anchor with title '{formatted_anchor_title}'")

        if len(episode_list_link) > 0:
            episode_list_link = f"https://en.wikipedia.org{episode_list_link}"
    else:
        episode_list_link = url
        
            
    return episode_list_link

def scrape_episode_page(episode_list_link, season_number):
    """
    Given a link to the episode list page, this function fetches the page and
    prints the first paragraph from the page (if found).
    """    
    # 1. Send a GET request to the episode list page
    response = requests.get(episode_list_link)
    
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return
    
    # 2. Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Save the HTML content to a file on the desktop   
    
    
    # Check if the season number is less than 10 and contains a leading zero
    searchable_value = ""
    if season_number.isnumeric():
        if int(season_number) < 10 and str(season_number).startswith('0'):
            season_number = int(str(season_number).lstrip('0'))    
            searchable_value = f"Season {season_number}"
    else:
        searchable_value = f"{season_number}"
        searchable_value = searchable_value.replace(" ", "_")

    season_header = None
    if "List_of_" in episode_list_link:    
        # Find the first instance of a table with the class 'wikiepisodetable' after the position of the substring "Season " + str(season_number)
        season_header = soup.find("h3", id=lambda x: x and f"{searchable_value}" in x)    
    
    if season_header:
        table = season_header.find_next(lambda tag: tag.name == "table" and ("wikiepisodetable" in tag.get("class", []) or "wikitable" in tag.get("class", [])))
            
        if table:
            print("Found the episode table for season", searchable_value)
            return table
        else:
            print(f"Error: Could not find a table with class 'wikiepisodetable' after '{searchable_value}'")
    else:
        print(f"Searching same page for table with class 'wikiepisodetable'")
        same_page_episode_table = soup.find("table", class_="wikiepisodetable")              
        return same_page_episode_table
    return None   

def scrape_table_for_row_data(scraped_table_data,episode_number):
    if scraped_table_data is None:
        print("Error: scraped_table_data is None")
        return None

    soup = BeautifulSoup(scraped_table_data, 'html.parser')      
    
    # Find the row corresponding to the episode number
    episode_rows = soup.find_all('tr')
    
    
    for episode_row in episode_rows:    
        th_count = len(episode_row.find_all('th'))    
        if th_count == 1: 
            
            th = episode_row.find('th')
            if th and th.get_text().strip() == str(episode_number):
                row_data = episode_row                
                        
            episodes_data = episode_row.find_all('td')        
            
            for episode_data in episodes_data:                        
                cleaned_episode_data = BeautifulSoup(str(episode_data), "html.parser").get_text()                        
                if cleaned_episode_data == str(episode_number):                                
                    row_data = episode_row
                    break
                                        
    return row_data
    
def scrape_single_row_for_data(scraped_table_data):
    if scraped_table_data is None:
        print("Error: scraped_table_data is None")
        return None    
    
    soup = BeautifulSoup(scraped_table_data, 'html.parser')      
    # Get the number of 'td' instances in soup
    # td_count = len(soup.find_all('td'))
        
    # Find the 'td' with the class 'summary'
    episode_name = soup.find('td', class_='summary')
        
    # print(test)
    # sys.exit()
    # # Find the row corresponding to the episode number
    # print(f"Found {td_count} 'td' instances in scraped_table_data")
    # if td_count == 0:
    #     print("Error: No 'td' instances found in scraped_table_data")
    # elif td_count > 1:
    #     episode_name = soup.find_all('td')[1]    
    # elif td_count == 1:
    #     episode_name = soup.find_all('td')[0]        

    return episode_name
    
    
        
