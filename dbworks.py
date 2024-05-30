from datetime import datetime
import general as general

class DBWorks:

    def __init__(self):
        pass
    
    # Function to insert events into database
    def insert_events(self, conn, cur, events):
        try:
            rows_inserted = 0
            event_query = """
                INSERT INTO "EVN"."EVENT_MASTER"("EventName", "EventDateTime", "EventLocation", "EventArtists", "EventImageURL")
                VALUES (%s, %s, %s, %s, %s)
                """

            for event in events:
                date_time = datetime.strptime(event['date'], '%a %d.%m.%Y %H.%M')  # Adjust the format as needed
                artists = ""
                for artist in event['artists']:
                    if event['title'] != artist:
                        if len(artist) > 1:
                            artists = (artists + ',' + artist)
                        else:
                            artists = artist

                cur.execute(event_query, (event['title'], date_time, event['location'], artists.lstrip(','), event['image_link']))
                rows_inserted += 1

            
            conn.commit()
            cur.close()
            conn.close()

            print(f"{rows_inserted} events inserted successfully.")
        except Exception as e:
            print(f"DB Insert Error Found: {e}")