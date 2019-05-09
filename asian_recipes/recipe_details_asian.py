from bs4 import BeautifulSoup
import requests, json, time, re

all_data = []

with open ('recipe_urls_asian.json') as recipe_urls:
    loadData = json.load(recipe_urls)


    for all in loadData:
        url = all['recipe_urls']

        try:
            time.sleep(1)

            html = requests.get(url)
            page_html = html.text
            soup = BeautifulSoup(page_html, 'lxml')
            print(url,"scrapping!")

            recipe_title = soup.find('h1')
            recipe_title = recipe_title.text

            data = {}
            data['recipe_id'] = all['recipe_id']
            data['title'] = recipe_title
            data['ingredients'] = []

            all_ingredients = soup.find_all('span', {'class': 'recipe-ingred_txt added'})
            for ingredient_list in all_ingredients:

                ingredient_id = ingredient_list['data-id']
                ingredient_item = ingredient_list.text
                ingredient_count = len(all_ingredients)

                detail = {}
                detail['ing_id'] = ingredient_id
                detail['ing_name'] = ingredient_item
                data['ing_count'] = ingredient_count

                data['ingredients'].append(detail)

            all_data.append(data)
        except:
            raise ValueError(url, "error")

        finally:
            json.dump(all_data,open('recipe_details_asian.json', 'w'), indent = 2)
