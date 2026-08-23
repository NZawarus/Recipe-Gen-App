import React from 'react';
import './RecipeDisplay.css';

const RecipeDisplay = ({ recipe }) => {
  if (!recipe) {
    return null;
  }

  // The new API response format includes recipe and ingredients
  const recipeData = recipe.recipe;
  const ingredients = recipe.ingredients || [];
  
  // The recipe might be a JSON string or already parsed as an object
  let parsedRecipe;
  try {
    parsedRecipe = typeof recipeData === 'string' ? JSON.parse(recipeData) : recipeData;
  } catch (e) {
    console.error('Error parsing recipe:', e);
    // If we can't parse it, just display it as raw text
    return (
      <div className="recipe-display">
        <h2>Your Generated Recipe</h2>
        <div className="recipe-content">
          <pre>{recipeData}</pre>
        </div>
      </div>
    );
  }

  return (
    <div className="recipe-display">
      <h2>{parsedRecipe.title || 'Your Generated Recipe'}</h2>
      
      <div className="recipe-info">
        <p><strong>Servings:</strong> {parsedRecipe.servings}</p>
        <p><strong>Calories:</strong> {parsedRecipe.calories} per serving</p>
      </div>
      
      <div className="recipe-ingredients">
        <h3>Ingredients</h3>
        <ul>
          {parsedRecipe.recipe_ingredients && parsedRecipe.recipe_ingredients.map((item, index) => (
            <li key={index}>
              <span className="ingredient-name">{item.ingredient}</span>
              <span className="ingredient-quantity">{item.quantity}</span>
            </li>
          ))}
        </ul>
      </div>
      
      <div className="recipe-instructions">
        <h3>Instructions</h3>
        <ol>
          {parsedRecipe.instructions && parsedRecipe.instructions.map((step, index) => (
            <li key={index}>{step}</li>
          ))}
        </ol>
      </div>
      
      {ingredients.length > 0 && (
        <div className="detected-ingredients">
          <h3>Detected Ingredients</h3>
          <p>{ingredients.join(', ')}</p>
        </div>
      )}
      
      <div className="recipe-actions">
        <button className="save-button">Save Recipe</button>
        <button className="share-button secondary">Share</button>
      </div>
    </div>
  );
};

export default RecipeDisplay; 