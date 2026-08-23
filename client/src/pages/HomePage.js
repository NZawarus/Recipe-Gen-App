import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>Transform Your Ingredients into Delicious Recipes</h1>
        <p>
          Upload a photo of your fridge or pantry, and let our AI identify your ingredients
          and generate personalized recipes.
        </p>
        <Link to="/upload" className="get-started-button">
          Get Started
        </Link>
      </div>

      <div className="features-section">
        <h2>How RecipeIQ Works</h2>
        
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">📷</div>
            <h3>Upload Your Photos</h3>
            <p>Take a picture of your ingredients or your entire fridge.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>AI-Powered Ingredient Detection</h3>
            <p>Our advanced AI identifies all the ingredients in your photo.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">📝</div>
            <h3>Custom Recipe Generation</h3>
            <p>Get personalized recipes based on what you already have.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 