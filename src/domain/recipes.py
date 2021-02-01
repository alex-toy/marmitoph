import pandas as pd
from marmiton import Marmiton, RecipeNotFound


def get_recipes(ingredients_to_include = [], ingredients_to_exclude = []):
    """Function extracting recipes from Marmiton website based on ingredients list.
    
    Parameters
        ----------
        ingredients_to_include : list of strings
            Ingredients to include to recipe (in French)
        ingredients_to_exclude : list of strings
            Ingredients to exclude from recipe (in French)


        Returns
        -------
        DataFrame
            DataFrame containing all matching recipes with recipe name as index 
            and with recipe infos as columns :
            - ingredients: string list of the recipe ingredients (including quantities)
            - steps: string list of each step of the recipe
            - image: if exists, image of the recipe (url).
            - cook_time: string, cooking time of the recipe
            - prep_time: string, estimated preparation time of the recipe
            - total_time: string, estimated total time of the recipe (cooking + preparation time)
            - author: string, name of the author of the recipe
            - nb_comments: string, number of comments/rates left by users
            - people_quantity: string, number of people the recipie is made for
            - budget: string, indicate the category of budget according to the website
            - difficulty: string, indicate the category of difficulty according to the website
            - rate, string: rate of the recipe out of 5
            - author_tip: string, note or tip left by the author
            - tags: string list, tags of the recipe
        """

    # Creation of query keywords based on ingredients
    query_keywords = " ".join(ingredients_to_include)
    if len(ingredients_to_exclude) > 0:
        query_keywords += " sans "
        query_keywords += " ".join(ingredients_to_exclude)


    # Search :
    query_options = {"aqt": query_keywords, "st": 1}
    query_result = Marmiton.search(query_options)

    # Recap on recipes and urls
    url_list = [recipe['url'] for recipe in query_result]
    recipes_list = [recipe['name'] for recipe in query_result]

    # Creation of tab with recipes infos
    recipes_keys = list(Marmiton.get(url_list[0]).keys())
    recipes_keys.remove('name')
    recipes_tab = pd.DataFrame(index = recipes_list, 
                                columns = ['url'] + recipes_keys)

    for url in url_list:
        recipe = Marmiton.get(url)
        recipes_tab.loc[recipe['name'], 'url'] = url
        for key in recipes_keys:
            recipes_tab.loc[recipe['name'], key] = recipe[key]
        
    return recipes_tab
