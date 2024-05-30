import connection
from dbworks import DBWorks
from webscrape import WebScrape

# Establish database connection
conn, cur = connection.get_connection()

# Create an instance of DBWorks
db_worker = DBWorks()

# Create an instance of WebScrape
wb = WebScrape()

if __name__ == '__main__':
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    baseurl = "https://www.lucernefestival.ch"
    url = "https://www.lucernefestival.ch/en/program/summer-festival-24"
    events = wb.scrape_events(useragent=useragent,baseurl=baseurl,url=url)
    db_worker.insert_events(conn=conn, cur=cur, events=events)