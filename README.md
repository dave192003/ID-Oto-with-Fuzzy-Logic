<img width="2170" height="404" alt="ID-Oto Banner with Bongbong Marcos" src="https://github.com/user-attachments/assets/443906cf-27b3-4977-9abb-f3a756c87e8b" />


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

<img width="2075" height="758" alt="Photo Sizes for ID Printing" src="https://github.com/user-attachments/assets/c4b4ef6e-c6f1-489a-abd2-23d307d47bd2" />

