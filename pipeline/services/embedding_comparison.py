import numpy as np

from sentence_transformers import SentenceTransformer, util
import json
import heapq

recipe_data_path = "Recipes/recipes_raw_nosource_ar.json"

# input_ingredients = ["spaghetti", "chicken breast", "butter", "onion", "lettuce", "salt"]

class EmbeddingComparison:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        # Load recipe embeddings
        self.ingredient_embeddings = np.load("services/ingredients.npy", allow_pickle=True)
        with open(recipe_data_path, 'r') as file:
            self.recipe_data = json.load(file)
    def compare_query(self, query):
        # Convert query ingredients into embeddings
        query_embedding = np.array(self.model.encode(query))
        print(query)
        scores = []
        for i in self.ingredient_embeddings:
            # Generate similarity between recipe and input ingredients
            similarities = util.cos_sim(query_embedding.astype(float), i.astype(float))
            # Calculate score based on number of ingredient matches
            combined_score = 0
            for j in similarities:
                if max(j) > 0.5:
                    combined_score += 1
            scores.append((combined_score / len(query_embedding.astype(float))))

        # Sort recipes by score and choose best matches
        indexed_arr = list(enumerate(scores)) 
        sorted_indexed_arr = sorted(indexed_arr, key=lambda x: x[1], reverse=True)
        return self.get_recipes(sorted_indexed_arr[:1])

    def get_recipes(self, indicies):
        # Find JSON for matching recipes
        index = 0
        indicies = [i[0] for i in indicies]
        matching_recipes = []
        print(indicies)
        for i in self.recipe_data:
            if index in indicies:
                matched_recipe = self.recipe_data[i]
                ingredient_list = []
                for i in matched_recipe["ingredients"][:-1]:
                    ingredient_list.append(i.replace("ADVERTISEMENT", ""))
                matched_recipe["ingredients"] = ingredient_list
                matching_recipes.append(str(matched_recipe))
            index += 1
        return matching_recipes

