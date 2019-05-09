from bs4 import BeautifulSoup
import requests, json, time


try:
    all_data = []
    url = "https://www.allrecipes.com/recipes/228/world-cuisine/australian-and-new-zealander/"

    for i in range(1,29):

        url_page = url + "?page=" + str(i)

        time.sleep(1)
        html = requests.get(url_page)

        print("page",str(i),"scrapping!")

        page_html = html.text
        soup = BeautifulSoup(page_html, "lxml")

        all_recipe = soup.find_all("article", {"class": "fixed-recipe-card"})

        for a_recipe in all_recipe:
            id_tag = a_recipe.find_all("ar-save-item")
            for a_id in id_tag:
                recipe_id = a_id["data-id"]

                data = {}
                data["recipe_id"] = recipe_id

                all_favorites = a_recipe.find_all("div", {"class" : "grid-card-image-container"})
                for favorite in all_favorites:
                    a_tag = favorite.find('a')
                    data["recipe_urls"] = a_tag['href']

                all_data.append(data)

except:
    raise ValueError("error")

finally:
	json.dump(unique_list,open("recipe_urls_australian_clean.json", "w"), indent = 2)
