export default function ExtractedInfo({ data }) {
  if (!data || Object.keys(data).length === 0) {
    return (
      <div className="error">
        No information could be extracted from the image. Please try with a clearer CNIC image.
      </div>
    );
  }

  return (
    <div>
      <div className="results-header">
        <h3>Extracted Information</h3>
      </div>
      
      <div className="info-grid">
        {Object.entries(data).map(([key, obj]) => (
          <div key={key} className="info-item">
            <span className="info-label">{key.replace(/_/g, ' ')}</span>
            <span className="info-value">{obj.value || 'Not detected'}</span>
          </div>
        ))}
      </div>
    </div>
  );
}