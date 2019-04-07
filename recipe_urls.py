from bs4 import BeautifulSoup
import requests, csv, json, time

all_data = []

time.sleep(0.5)

with open("world_recipe_urls.csv") as csvfile:
    next(csvfile)
    readcsv = csv.reader(csvfile, delimiter = ',')
    for row in readcsv:
        url= row[0]

        for i in range(1,200):

            url_page = url + "?page=" + str(i)

            html = requests.get(url)

            if html.status_code != 200:
               continue

            print(url_page,"scrapping!")

            page_html = html.text
            soup = BeautifulSoup(page_html, "lxml")


            all_id = soup.find_all("ar-save-item")
            for id in all_id:
                cat = {}
                cat["recipe_id"] = id['data-id']

            all_favorites = soup.find_all("div", {"class" : "grid-card-image-container"})
            for favorite in all_favorites:
                all_tag = favorite.find_all('a')
                for a_tag in all_tag:
                    cat["recipe_urls"] = a_tag['href']

                all_data.append(cat)
json.dump(all_data,open("recipe_urls.json", "w"), indent = 2)
