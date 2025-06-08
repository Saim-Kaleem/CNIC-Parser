import { useState } from 'react';
import UploadForm from './components/UploadForm';
import ExtractedInfo from './components/ExtractedInfo';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [imageURL, setImageURL] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleResult = (data) => {
    setResult(data);
    setLoading(false);
  };

  const handleImage = (url) => {
    setImageURL(url);
    setLoading(true);
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <header className="app-header">
          <h1 className="app-title">CNIC Parser</h1>
          <p className="app-subtitle">
            Extract information from Pakistani CNIC cards using advanced OCR technology
          </p>
        </header>

        <section className="upload-section">
          <UploadForm onResult={handleResult} onImage={handleImage} />
        </section>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <span>Processing your CNIC image...</span>
          </div>
        )}

        {imageURL && !loading && (
          <section className="image-preview">
            <img src={imageURL} alt="CNIC Preview" className="preview-image" />
          </section>
        )}

        {result && !loading && (
          <section className="results-section">
            <ExtractedInfo data={result} />
          </section>
        )}
      </div>
    </div>
  );
}

export default App;