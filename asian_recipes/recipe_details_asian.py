from bs4 import BeautifulSoup
import requests, json, time, re

all_data = []

with open ('recipe_urls_asian.json') as recipe_urls:
    loadData = json.load(recipe_urls)

try:
    for all in loadData:
        url = all['recipe_urls']

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

        review = soup.find('span', {'class': 'review-count'})

        if review is None:
            continue
        else:
            review_number = review.text.strip('reviews').strip()

            review_star = soup.find('div', {'class': 'rating-stars'})
            review_score = review_star['data-ratingstars']

        data['review_count'] = review_number
        data['review_score'] = review_score

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
    try:

        for all in loadData:
            url = all['recipe_urls']

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

            rating = soup.find('span', {'class': 'review-star-text'}).text.strip()

            if rating is None:
                continue
                
            else:
                review_score = re.findall('(\d+(?:\.\d+)?)',rating)
                review_count = soup.find('span', {'class': 'ratings-count'}).text.strip('Ratings').strip()

                data['review_count'] = review_count
                data['review_score'] = review_score


            data['ingredients'] = []

            all_ingredients = soup.find_all('li', {'class': 'ingredients-item'})
            for ingredients in all_ingredients:
                ingredient_id = ingredients['data-id']

                detail = {}
                detail['ing_id'] = ingredient_id

                ing_names = ingredients.find_all("span", {"class" : "ingredients-item-name"})

                for ing_text in ing_names:
                    ingredient_item = ing_text.text.strip()
                    ingredient_count = len(all_ingredients)

                    detail['ing_name'] = ingredient_item
                    data['ing_count'] = ingredient_count

                    data['ingredients'].append(detail)

            all_data.append(data)
    except:
        raise ValueError(url, "error")

finally:
    json.dump(all_data,open('recipe_details_asian.json', 'w'), indent = 2)
    