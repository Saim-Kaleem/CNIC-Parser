# 🚀 Deployment Guide

## Vercel Deployment (Backend)

### Prerequisites
- Vercel account
- Vercel CLI installed: `npm install -g vercel`

### Backend Deployment Steps

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Deploy to Vercel**
   ```bash
   vercel --prod
   ```

3. **Set Environment Variables (if needed)**
   ```bash
   vercel env add PYTHONPATH
   # Enter: /var/task
   ```

### Frontend Deployment (Vercel/Netlify)

1. **Build the frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Vercel**
   ```bash
   vercel --prod
   ```

3. **Update API endpoint**
   - Update `src/api.js` to use your deployed backend URL
   ```javascript
   const API_BASE_URL = 'https://your-backend.vercel.app';
   ```

### Environment Configuration

The app is configured to:
- Use temporary directory for file uploads (Vercel compatible)
- Handle CORS for cross-origin requests
- Clean up uploaded files automatically
- Use OpenCV headless for serverless environments

### Troubleshooting

**Common Issues:**

1. **Timeout errors**: OCR processing can take time. The function timeout is set to 30s.
2. **Memory issues**: Large images may cause memory problems. Consider image compression.
3. **Cold starts**: First request might be slower due to model loading.

**Solutions:**
- Use `opencv-python-headless` instead of `opencv-python`
- Optimize image size before processing
- Consider using edge functions for better performance

### Local Development

1. **Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Production Considerations

- **Security**: Implement rate limiting and file validation
- **Performance**: Add caching for repeated requests
- **Monitoring**: Set up error tracking and logging
- **Scaling**: Consider using dedicated OCR services for high volume
