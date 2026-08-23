import axios from 'axios';
import API_BASE_URL from '../config';

const GENERATE_API = `${API_BASE_URL}/generate_recipe`;

// API client for generating recipes from uploaded images
export const generateRecipeAPI = {
  /**
   * Generate a recipe from uploaded images
   * 
   * @param {Array} images - Array of image objects with filename and imageData
   * @param {number} servings - Number of servings (default: 2)
   * @param {boolean} useLlama - Whether to use Llama instead of Gemini (default: false)
   * @param {boolean} skipSegmentation - Whether to skip segmentation and use whole image (default: false)
   * @returns {Promise<Object>} - Recipe data response
   */
  generateRecipe: async (images, servings = 2, useLlama = false, skipSegmentation = false) => {
    try {
      const response = await axios.post(
        `${GENERATE_API}?use_llama=${useLlama}&skip_segmentation=${skipSegmentation}`, 
        {
          images: images,
          servings: servings
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error generating recipe:', error);
      throw error;
    }
  }
};

export default generateRecipeAPI; 