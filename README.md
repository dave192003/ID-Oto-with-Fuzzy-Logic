# ID_Oto
<img width="1900" height="358" alt="image" src="https://github.com/user-attachments/assets/3c6b9d0d-365c-4a8a-81ac-9591f7b5a83e" />

## Overview

**ID-Oto** is a **standalone full-stack web application** that automates the processing of ID photos, reducing manual editing time and the preparation of print-ready ID pictures.

## Architecture

```
Frontend (HTML + CSS + JavaScript)
        ↓
Flask REST API (http://localhost:8000/api)
        ↓
Python Image Processing Services
        ↓
Processed Image
        ↓
Frontend
```

No n8n dependency. The Flask backend handles the complete image processing pipeline.

## Automation Process

**Step-by-step workflow:**

1. **Upload Image/Photo**
   * User uploads the raw image or photo on website and chooses the size of an id.

2. **Background Removal**
   * The system automatically removes the background from the uploaded photo.

3. **Photo Enhancement**
   * The image quality is enhanced for better clarity, lighting, and overall appearance using a **Mamdani Fuzzy Inference System**.

4. **Crop to Designated Size**
   * The photo is automatically cropped according to the required ID dimensions.

5. **Layout for Printing**
   * Multiple copies of the processed ID photo are arranged into a printable sheet layout.

6. **Print Ready Output**
   * Final output is generated and prepared for printing.

## Project Structure

```
ID-Oto/
│
├── frontend/
│   ├── landing-page.html      # Main ID photo processor page
│   ├── fuzzy-analysis.html    # Fuzzy logic analysis visualization page
│   ├── script.js              # Main page logic
│   ├── fuzzy-analysis.js      # Fuzzy analysis page logic
│   ├── style.css              # Main styles
│   ├── fuzzy-analysis.css     # Fuzzy analysis page styles
│   ├── js/
│   │   └── api.js             # API service layer (Flask backend)
│   ├── Dockerfile             # Nginx container for frontend
│   └── resources/
│       └── images/            # Static images
│
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── routes/
│   │   ├── image_routes.py    # Image processing API routes
│   │   └── analysis_routes.py # Fuzzy analysis API routes
│   ├── services/
│   │   ├── background_removal.py  # Background removal service
│   │   ├── image_analysis.py      # Image feature extraction
│   │   ├── fuzzy_enhancement.py   # Fuzzy logic enhancement
│   │   ├── cropping.py            # ID photo cropping service
│   │   └── print_layout.py        # Print layout generation
│   ├── fuzzy_logic/
│   │   ├── __init__.py
│   │   ├── membership.py          # Triangular membership functions
│   │   ├── memberships.py         # Input membership definitions
│   │   ├── output_membership.py   # Output membership definitions
│   │   ├── rules.py               # Fuzzy rule base and evaluation
│   │   ├── inference.py           # Mamdani inference pipeline
│   │   └── defuzzification.py     # Centroid defuzzification
│   ├── utils/
│   │   ├── __init__.py
│   │   └── image_utils.py         # Image utility functions
│   ├── Dockerfile
│   └── requirements.txt
│
└── docker-compose.yml
```

## Fuzzy Logic Pipeline

The image enhancement uses a complete **Mamdani Fuzzy Inference System**:

```
Image
  ↓
Feature Extraction (Brightness, Contrast, Sharpness, Noise)
  ↓
Fuzzification (Triangular membership functions)
  ↓
Rule Evaluation (15 fuzzy rules)
  ↓
Aggregation (Max aggregation)
  ↓
Defuzzification (Centroid method)
  ↓
Enhancement Parameters (Alpha, Beta, Sharpen, Denoise)
  ↓
Image Enhancement
  ↓
Processed Image
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/health` | GET | JSON health status |
| `/api/process` | POST | Complete ID photo pipeline (background removal, enhancement, cropping) |
| `/api/analyze` | POST | Full fuzzy logic analysis (features, parameters, rules) |
| `/api/remove-bg` | POST | Remove image background |
| `/api/id-crop` | POST | Crop to ID photo size |

### POST /api/process

Accepts `multipart/form-data`:

| Field | Type | Description |
|-------|------|-------------|
| `image` | file | The uploaded image (JPG, PNG, JPEG) |
| `type` | string | ID photo size: `1x1`, `1.5x1.5`, `2x2`, `passport` |

Returns the processed image as `image/png`.

## Fuzzy Logic Analysis Page

The `fuzzy-analysis.html` page provides a complete visualization of the fuzzy inference pipeline:

- **Image Comparison** - Original vs Processed side-by-side
- **Image Statistics** - Brightness, Contrast, Sharpness, Noise for both images
- **Enhancement Parameters** - Alpha, Beta, Sharpen, Denoise with descriptions
- **Applied Fuzzy Rules** - Fired rules with activation strengths and visual bars
- **Before vs After Comparison** - Table with changes and percentage changes

## Prerequisite

Before running the project, install the following:

- Docker Desktop: https://www.docker.com/products/docker-desktop/

## Running with Docker

```bash
docker compose up --build
```

This will start:
- **Backend** (Flask API) on port `8000`
- **Frontend** (Nginx) on port `8080`

Open http://localhost:8080 in your browser.

## Running Locally (Development)

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The backend will run on http://localhost:8000.

### Frontend

Serve the `frontend/` directory with any static file server:

```bash
cd frontend
python -m http.server 5173
```

Or use VS Code Live Server. The frontend will be available at http://localhost:5173.

## Photo Sizes

| Size | Dimensions (300 DPI) |
|------|---------------------|
| 1x1 | 300 x 300 px |
| 1.5x1.5 | 450 x 450 px |
| 2x2 | 600 x 600 px |
| Passport | 413 x 531 px |