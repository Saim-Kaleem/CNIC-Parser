import { useState } from 'react';
import { uploadImage } from '../api';

export default function UploadForm({ onResult, onImage }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a file first");
      return;
    }

    setError(null);
    onImage(URL.createObjectURL(file)); // Show preview
    
    try {
      const data = await uploadImage(file);
      onResult(data);
    } catch (err) {
      setError(`Upload failed: ${err.message}`);
      onResult(null);
    }
  };

  return (
    <form onSubmit={handleUpload} className="upload-form">
      <div className="file-input-wrapper">
        <label htmlFor="file-input" className="file-input-label">
          <div className="upload-icon">📄</div>
          <div className="upload-text">
            {file ? file.name : "Choose CNIC image to upload"}
          </div>
          <div className="upload-subtext">
            Supports PNG, JPG, JPEG formats
          </div>
          <input
            id="file-input"
            type="file"
            className="file-input"
            accept="image/*"
            onChange={handleFileChange}
          />
        </label>
      </div>
      
      {error && (
        <div className="error">
          {error}
        </div>
      )}
      
      <button type="submit" className="upload-button" disabled={!file}>
        {file ? "Extract Information" : "Select File First"}
      </button>
    </form>
  );
}