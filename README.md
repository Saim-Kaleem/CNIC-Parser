# CNIC Parser

<div align="center">

<img src="./frontend/src/assets/5265347.png" alt="CNIC Parser Logo" width="200" height="200" />

**Advanced OCR-powered Pakistani CNIC Information Extraction System**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000.svg)](https://flask.palletsprojects.com)

[Demo](#demo) • [Features](#features) • [Installation](#installation) • [Usage](#usage) • [API](#api)

</div>

---

## Introduction

CNIC Parser is a web application that uses advanced Optical Character Recognition (OCR) technology to automatically extract and digitize information from Pakistani Computerized National Identity Cards (CNIC). The system provides highly accurate text extraction with confidence scoring and visual bounding box annotations.

## Motivation

Manual data entry from identity documents is time-consuming, error-prone and inefficient. This project aims to:

- **Automate** the extraction of personal information from CNIC cards
- **Reduce** human error in data transcription
- **Accelerate** document processing workflows
- **Provide** confidence metrics for extracted data reliability
- **Visualize** extraction accuracy through interactive bounding boxes

## Features

### 🔍 **Advanced OCR Processing**
- High-accuracy text extraction using state-of-the-art OCR models
- Support for various image formats (PNG, JPG, JPEG)
- Robust preprocessing for optimal recognition

### 📊 **Confidence Scoring**
- Real-time confidence metrics for each extracted field
- Color-coded visualization (Green: High confidence, Red: Low confidence)

### 🎨 **Interactive Visualization**
- Dynamic bounding box overlay on original images
- Confidence-based color mapping
- Comprehensive legend and field statistics

### 🚀 **Modern Web Interface**
- Responsive, minimalist design
- Drag-and-drop file upload
- Real-time processing feedback
- Mobile-friendly interface

### 🔒 **Secure Processing**
- Temporary file handling with automatic cleanup
- No permanent storage of sensitive documents
- CORS-enabled for secure cross-origin requests

## Tech Stack

### **Backend**
- **Python 3.9+** - Core processing engine
- **Flask** - Lightweight web framework
- **OpenCV** - Image preprocessing
- **EasyOCR** - Text extraction engine
- **NumPy** - Numerical computations

### **Frontend**
- **React 18** - Modern UI framework
- **Vite** - Fast build tool and dev server
- **CSS3** - Custom styling with CSS variables
- **HTML5 Canvas** - Dynamic bounding box rendering

### **Development Tools**
- **ESLint** - Code quality assurance
- **Git** - Version control
- **npm/pip** - Package management

## Visuals

### Dashboard Overview and Upload Interface
![Dashboard Screenshot](./docs/dashboard.PNG)
*Clean, intuitive interface for CNIC upload, validation and processing*

### Extraction Results
![Extraction Results](./docs/extraction_results.PNG)
*Detailed information extraction with confidence metrics*

### Annotated Image Analysis
![Annotated Image](./docs/annotated_image.PNG)
*Interactive bounding boxes with confidence-based color coding statistics legend*


## Getting Started

### Prerequisites

- **Python 3.9+** installed on your system
- **Node.js 16+** and **npm** for frontend development
- **Git** for version control

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/cnic-parser.git
   cd cnic-parser
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. **Start the Backend Server**
   ```bash
   cd backend
   python app.py
   ```
   The Flask server will start on `http://localhost:5000`

2. **Start the Frontend Development Server**
   ```bash
   cd frontend
   npm run dev
   ```
   The React app will be available at `http://localhost:5173`

3. **Access the Application**
   Open your browser and navigate to `http://localhost:5173`

## Usage

1. **Upload CNIC Image**
   - Click on the upload area or drag and drop your CNIC image
   - Supported formats: PNG, JPG, JPEG

2. **Processing**
   - The system automatically processes the uploaded image

3. **View Results**
   - Extracted information appears in a clean, organized format
   - Confidence scores indicate extraction reliability

4. **Analyze Accuracy**
   - Interactive annotated image shows bounding boxes
   - Color-coded confidence visualization
   - Detailed field statistics

## API Reference

### Upload Endpoint

```http
POST /parse
```

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with `image` field containing the CNIC file

**Response:**
```json
{
  "name": {
    "value": "John Doe",
    "bbox": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
    "confidence": 0.95
  },
  "cnic_number": {
    "value": "12345-6789012-3",
    "bbox": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
    "confidence": 0.92
  }
  // ... other fields
}
```

## Project Structure

```
cnic-parser/
├── backend/
│   ├── app.py              # Flask application
│   ├── ocr_utils.py        # OCR processing utilities
│   ├── requirements.txt    # Python dependencies
│   └── uploads/           # Temporary file storage
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── assets/        # Static assets
│   │   └── api.js         # API communication
│   ├── public/            # Public assets
│   └── package.json       # Node.js dependencies
└── docs/
    └── images/            # Documentation images
```


## Acknowledgments

- OCR technology providers for accurate text recognition
- React and Flask communities for excellent documentation
- Pakistani government for CNIC format standardization

## Support

If you encounter any issues or have questions:

- **Create an Issue** on GitHub
- **Email:** saim.kaleem.a@gmail.com

---

<div align="center">

**Made with ❤️ for automating document processing**

⭐ **Star this repo if you found it helpful!** ⭐

</div>