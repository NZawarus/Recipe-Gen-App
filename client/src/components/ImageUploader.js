import React, { useState } from 'react';
import './ImageUploader.css';

const ImageUploader = ({ onImageUpload }) => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [previewUrls, setPreviewUrls] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    handleFiles(files);
  };

  const handleFiles = (files) => {
    if (!files.length) return;

    // Check if files are images
    const validFiles = [];
    const validPreviews = [];
    
    files.forEach(file => {
      if (!file.type.startsWith('image/')) {
        setErrorMessage('Please select only image files (JPEG, PNG, etc.)');
        return;
      }
      
      validFiles.push(file);
      
      // Create preview for this file
      const reader = new FileReader();
      reader.onload = () => {
        validPreviews.push({
          file: file,
          preview: reader.result
        });
        
        // Update state if all previews are generated
        if (validPreviews.length === validFiles.length) {
          setSelectedFiles(prevFiles => [...prevFiles, ...validFiles]);
          setPreviewUrls(prevUrls => [...prevUrls, ...validPreviews]);
          setErrorMessage(''); // Clear any error
        }
      };
      reader.readAsDataURL(file);
    });
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);
    
    if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
      handleFiles(Array.from(event.dataTransfer.files));
    }
  };

  const removeFile = (index) => {
    setSelectedFiles(files => files.filter((_, i) => i !== index));
    setPreviewUrls(urls => urls.filter((_, i) => i !== index));
  };

  const handleUpload = () => {
    if (!selectedFiles.length) {
      setErrorMessage('Please select at least one image to upload');
      return;
    }

    // Prepare images data
    const processFiles = selectedFiles.map((file, index) => {
      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = () => {
          // Extract base64 data
          const base64Data = reader.result.split(',')[1];
          resolve({
            filename: file.name,
            image_data: base64Data
          });
        };
        reader.readAsDataURL(file);
      });
    });

    // Process all files and then upload
    Promise.all(processFiles)
      .then(images => {
        onImageUpload({ images });
      });
  };

  return (
    <div className="image-uploader">
      <div 
        className={`upload-area ${isDragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input 
          type="file" 
          id="file-input" 
          accept="image/*" 
          onChange={handleFileChange}
          className="file-input"
          multiple
        />
        
        {previewUrls.length > 0 ? (
          <div className="preview-container">
            {previewUrls.map((item, index) => (
              <div key={index} className="image-preview-item">
                <img src={item.preview} alt={`Preview ${index}`} className="image-preview" />
                <button 
                  className="remove-image-btn" 
                  onClick={() => removeFile(index)}
                  title="Remove image"
                >
                  ×
                </button>
              </div>
            ))}
            <label htmlFor="file-input" className="add-more-images">
              + Add More
            </label>
          </div>
        ) : (
          <div className="upload-prompt">
            <i className="upload-icon">📷</i>
            <p>Drag & drop images here or click to browse</p>
            <p className="upload-subtitle">You can select multiple images</p>
            <label htmlFor="file-input" className="browse-button">Browse Files</label>
          </div>
        )}
      </div>

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      <div className="actions">
        {selectedFiles.length > 0 && (
          <>
            <p className="selected-count">{selectedFiles.length} image{selectedFiles.length !== 1 ? 's' : ''} selected</p>
            <button onClick={handleUpload} className="upload-button">
              Upload & Generate Recipe
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default ImageUploader; 