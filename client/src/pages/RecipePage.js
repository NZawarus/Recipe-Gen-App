import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './RecipePage.css';

// This is a placeholder component for the future functionality
// to view individual saved recipes
const RecipePage = () => {
  const { id } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // In a real implementation, we would fetch the recipe by ID
    // For now, just simulate a loading state and then success
    const timer = setTimeout(() => {
      setRecipe({
        id,
        name: 'Placeholder Recipe',
        content: 'This is a placeholder for recipe content that would be loaded from the backend API.'
      });
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, [id]);

  if (loading) {
    return (
      <div className="recipe-page loading">
        <div className="loading-spinner"></div>
        <p>Loading recipe...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="recipe-page error">
        <h2>Error</h2>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="recipe-page">
      <h1>{recipe.name}</h1>
      <div className="recipe-content">
        <p>{recipe.content}</p>
      </div>
    </div>
  );
};

export default RecipePage; 