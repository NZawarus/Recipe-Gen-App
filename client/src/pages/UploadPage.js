import React, { useState } from 'react';
import './UploadPage.css';
import ImageUploader from '../components/ImageUploader';
import RecipeDisplay from '../components/RecipeDisplay';
import { generateRecipeAPI } from '../api/routers/generate';

const UploadPage = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [generatedRecipe, setGeneratedRecipe] = useState(null);
  const [servings, setServings] = useState(2);
  const [useLlama, setUseLlama] = useState(false);
  const [skipSegmentation, setSkipSegmentation] = useState(false);

  const handleImageUpload = async ({ images }) => {
    if (!images || images.length === 0) {
      setError('Please select at least one image to upload');
      return;
    }
    
    setLoading(true);
    setError('');
    setGeneratedRecipe(null);
    
    try {
      const response = await generateRecipeAPI.generateRecipe(
        images,
        servings,
        useLlama,
        skipSegmentation
      );
      setGeneratedRecipe(response);
    } catch (err) {
      console.error('Recipe generation error:', err);
      
      // Display a more specific error message if available
      if (err.response && err.response.data && err.response.data.detail) {
        setError(`Error: ${err.response.data.detail}`);
      } else {
        setError('Failed to generate recipe. Please try again with different images.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-header">
        <h1>Generate Recipe from Your Ingredients</h1>
        <p>Upload photos of your ingredients and let our AI create a custom recipe for you.</p>
        <p className="upload-subtitle">You can upload multiple images for better ingredient detection</p>
      </div>

      <div className="recipe-options">
        <div className="option-group">
          <label htmlFor="servings">Number of Servings:</label>
          <input 
            type="number" 
            id="servings" 
            min="1" 
            max="12" 
            value={servings} 
            onChange={(e) => setServings(parseInt(e.target.value, 10))}
          />
        </div>
        
        <div className="option-group">
          <label htmlFor="model-select">Recipe Model:</label>
          <div className="model-toggle">
            <button 
              className={`model-button ${!useLlama ? 'active' : ''}`} 
              onClick={() => setUseLlama(false)}
            >
              Gemini
            </button>
            <button 
              className={`model-button ${useLlama ? 'active' : ''}`} 
              onClick={() => setUseLlama(true)}
            >
              Llama
            </button>
          </div>
        </div>
        
        <div className="option-group">
          <label htmlFor="segmentation">Segmentation:</label>
          <div className="model-toggle">
            <button 
              className={`model-button ${!skipSegmentation ? 'active' : ''}`} 
              onClick={() => setSkipSegmentation(false)}
            >
              Enabled
            </button>
            <button 
              className={`model-button ${skipSegmentation ? 'active' : ''}`} 
              onClick={() => setSkipSegmentation(true)}
            >
              Disabled
            </button>
          </div>
        </div>
      </div>

      <ImageUploader onImageUpload={handleImageUpload} />

      {loading && (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>
            Analyzing your ingredients 
            {!skipSegmentation && " with segmentation"} 
            and generating a recipe using {useLlama ? 'Llama' : 'Gemini'}...
          </p>
        </div>
      )}

      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button 
            className="retry-button" 
            onClick={() => setError('')}
          >
            Try Again
          </button>
        </div>
      )}

      {generatedRecipe && (
        <>
          <div className="model-info">
            Recipe generated using: <span className="model-name">{generatedRecipe.generator_used || (useLlama ? 'Llama' : 'Gemini')}</span>
            {generatedRecipe.segmentation_used !== undefined && (
              <span className="segmentation-info">
                {' '} with segmentation {generatedRecipe.segmentation_used ? 'enabled' : 'disabled'}
              </span>
            )}
          </div>
          <RecipeDisplay recipe={generatedRecipe} />
        </>
      )}
    </div>
  );
};

export default UploadPage; 