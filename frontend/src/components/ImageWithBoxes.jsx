import React, { useRef, useEffect, useState, useCallback } from 'react';

export default function ImageWithBoxes({ imageFile, extractedData }) {
  const canvasRef = useRef(null);
  const [imageUrl, setImageUrl] = useState(null);

  // Generate color based on confidence score (0-1)
  const getConfidenceColor = (confidence) => {
    // Convert confidence to a color from red (low) to green (high)
    const red = Math.round(255 * (1 - confidence));
    const green = Math.round(255 * confidence);
    return `rgb(${red}, ${green}, 0)`;
  };

  // Get confidence level text
  const getConfidenceLevel = (confidence) => {
    if (confidence >= 0.9) return 'Very High';
    if (confidence >= 0.8) return 'High';
    if (confidence >= 0.7) return 'Medium';
    if (confidence >= 0.6) return 'Low';
    return 'Very Low';
  };

  const drawBoundingBoxes = useCallback(() => {
    if (!imageUrl || !extractedData) return;
    
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Create a new image element
    const img = new Image();
    img.onload = () => {
      // Set canvas dimensions to match image
      canvas.width = img.width;
      canvas.height = img.height;
      
      // Draw the image
      ctx.drawImage(img, 0, 0);
      
      // Draw bounding boxes for each field
      Object.entries(extractedData).forEach(([fieldName, fieldData]) => {
        if (fieldData.bbox && fieldData.confidence !== undefined) {
          const bbox = fieldData.bbox;
          const confidence = fieldData.confidence;
          const color = getConfidenceColor(confidence);
          
          // Set line style
          ctx.strokeStyle = color;
          ctx.lineWidth = 3;
          ctx.fillStyle = color;
          
          // Draw the bounding box
          ctx.beginPath();
          ctx.moveTo(parseInt(bbox[0][0]), parseInt(bbox[0][1]));
          
          for (let i = 1; i < bbox.length; i++) {
            ctx.lineTo(parseInt(bbox[i][0]), parseInt(bbox[i][1]));
          }
          
          ctx.closePath();
          ctx.stroke();
          
          // Draw semi-transparent fill
          ctx.globalAlpha = 0.1;
          ctx.fill();
          ctx.globalAlpha = 1;
          
          // Draw field label with confidence
          const labelX = parseInt(bbox[0][0]);
          const labelY = parseInt(bbox[0][1]) - 5;
          
          ctx.fillStyle = color;
          ctx.font = '14px Arial';
          ctx.fontWeight = 'bold';
          
          const label = `${fieldName.replace(/_/g, ' ')} (${(confidence * 100).toFixed(1)}%)`;
          
          // Draw background for text
          const textMetrics = ctx.measureText(label);
          ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
          ctx.fillRect(labelX - 2, labelY - 16, textMetrics.width + 4, 18);
          
          // Draw text
          ctx.fillStyle = color;
          ctx.fillText(label, labelX, labelY);
        }
      });
    };
    
    img.src = imageUrl;
  }, [imageUrl, extractedData, getConfidenceColor]);

  useEffect(() => {
    if (imageFile) {
      const url = URL.createObjectURL(imageFile);
      setImageUrl(url);
      
      return () => {
        URL.revokeObjectURL(url);
      };
    }
  }, [imageFile]);

  useEffect(() => {
    drawBoundingBoxes();
  }, [drawBoundingBoxes]);

  // Generate legend data
  const legendData = [
    { level: 'Very High', range: '90-100%', color: getConfidenceColor(0.95) },
    { level: 'High', range: '80-89%', color: getConfidenceColor(0.85) },
    { level: 'Medium', range: '70-79%', color: getConfidenceColor(0.75) },
    { level: 'Low', range: '60-69%', color: getConfidenceColor(0.65) },
    { level: 'Very Low', range: '0-59%', color: getConfidenceColor(0.3) },
  ];

  if (!imageFile || !extractedData) {
    return null;
  }

  return (
    <div className="image-with-boxes">
      <div className="results-header">
        <h3>Annotated Image</h3>
        <p>Bounding boxes show detected fields with confidence-based colors</p>
      </div>
      
      <div className="image-analysis-container">
        <div className="image-container">
          <canvas
            ref={canvasRef}
            className="annotated-image"
            style={{ maxWidth: '100%', height: 'auto' }}
          />
        </div>
        
        <div className="confidence-legend">
          <h4>Confidence Legend</h4>
          <div className="legend-items">
            {legendData.map((item, index) => (
              <div key={index} className="legend-item">
                <div 
                  className="color-indicator"
                  style={{ backgroundColor: item.color }}
                ></div>
                <span className="confidence-level">{item.level}</span>
                <span className="confidence-range">({item.range})</span>
              </div>
            ))}
          </div>
          
          <div className="legend-stats">
            <h5>Field Statistics</h5>
            {Object.entries(extractedData).map(([fieldName, fieldData]) => (
              <div key={fieldName} className="field-stat">
                <span className="field-name">{fieldName.replace(/_/g, ' ')}</span>
                <span 
                  className="field-confidence"
                  style={{ color: getConfidenceColor(fieldData.confidence) }}
                >
                  {(fieldData.confidence * 100).toFixed(1)}% - {getConfidenceLevel(fieldData.confidence)}
                </span>
              </div>
            ))}
          </div>
        </div>
        <div className="image-file-warning">
            <b>*Note:</b> Undetected fields may be calculated using heuristics, hence the bounding boxes are drawn based ONLY on the detected fields. Ensure the image is clear to detect all fields.
        </div>
      </div>
    </div>
  );
}