import requests
from bs4 import BeautifulSoup
import general as general

class WebScrape:

    def __init__(self):
        pass
    
    # Function to Scrape Events from the URL
    def scrape_events(self,useragent, baseurl , url):
        try:
            # User Agent Assignment
            headers = {'User-Agent' : useragent}

            # Request the webpage content
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            event_list = soup.find_all('p', class_='event-title h3')

            event_links = [] # For fetching all the individual Websites from the event masterpage
            events = [] # For Storing all the individual event details for adding into DB

            for event in event_list:
                for link in event.find_all('a', href = True):
                    event_links.append(baseurl + link['href'])

            print(len(event_links))

            for link in event_links:
                print(link)
                event_link = link

                response = requests.get(event_link, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')

                event_name_raw = soup.find('h1').text.strip()
                event_name = event_name_raw.split('|')[0].strip()
                event_details = soup.find('div', class_='cell large-6 subtitle').text.strip()
                text_content = event_details.strip()
                details = text_content.split('|')
                # Get the last three elements: date, time, and venue
                date, time, venue = details[-3], details[-2], details[-1]
                event_date = ((date.strip()).replace("Date and Venue","").replace("\n", "").replace("\t", "") + "2024")
                event_time = time.strip()
                event_venue = venue.strip()
                event_date_time_raw = (event_date + " " + event_time)
                event_date_time = event_date_time_raw.split('/')[0].strip()
                performers_raw = [performer.get_text(strip=True) for performer in soup.find_all('li', class_='cell medium-6 p')]
                subtitles = [subtitle.get_text(strip=True) for subtitle in soup.find_all('span', class_='body-small')]
                performers = general.GeneralFunctions.remove_words_from_list(performers_raw, subtitles)
                image_tag = (soup.find("img"))
                image_url = (baseurl + image_tag["src"])

                events.append({
                            'date': event_date_time,
                            'location': event_venue,
                            'title': event_name,
                            'artists': performers,
                            'image_link': image_url
                        })
                
            return events
            
        except Exception as e:
            print(f"WebScraping Error Found: {e}")