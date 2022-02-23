# Downloads source pages from spotifycharts

from datetime import datetime, timedelta
from time import sleep

from bushbaby import BushBaby

end_date = datetime(day=11, month=2,
                    year=2022)  # must set this to the latest date which is always one day ahead of what is
# represented on the site
date_pairs = []
for x in range(0, 52):
    week_start = end_date - timedelta(days=7)
    weekend = end_date.strftime("%Y-%m-%d")
    week_start = week_start.strftime("%Y-%m-%d")
    date_string = f"{week_start}--{weekend}"
    date_pairs.append(date_string)
    end_date = end_date - timedelta(days=7)


url = "https://spotifycharts.com/regional/za/weekly/"
#scraper

for d in date_pairs:
    scrape_url = f"{url}{d}"
    print (scrape_url)
    target = BushBaby(scrape_url)
    target.go_hunt_bushbaby()
    target.save_page_source(d)
    sleep(10)

# Install chromedriver
