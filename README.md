# 🛡️ Presidio PII Detector

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0096887logo-fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/docker-X230db7cd.svg?logo=docker&logoColor=white)
![Presidio](https://img.shields.io/badge/Microsoft-Presidio-blue)

**A complete solution for detecting and redacting Personally Identifiable Information (PII) from documents using Microsoft Presidio, FastAPI, and a modern web frontend.**

[🚀 Quick Start](#quick-start-docker) • [📖 Documentation](#table-of-contents) • [🔌 API Docs](#api-endpoints) • [🐳 Docker](#docker-deployment) • [☁️ Railway](#railway-deployment)

</div>

---

## 📋 Table of Contents

- [✨ Features](#features)
- [🏗️ System Architecture](#system-architecture)
- [🛠️ Tech Stack](#tech-stack)
- [🚀 Quick Start (Docker)](#quick-start-docker)
- [💻 Local Development Setup](#local-development-setup)
- [📚 API Documentation](#api-documentation)
- [🐳 Docker Deployment](#docker-deployment)
- [☁️ Railway Deployment](#railway-deployment)
- [📝 License](#license)
- [🤝 Contributing](#contributing)

---

## ✨ Features

- 🔍 **Advanced PII Detection** - Detects multiple PII types including emails, phone numbers, credit cards, name, bank account numbers, aadhar card number, pan card number, organization IDs
- 🎭 **Text Masking** - Redact sensitive information from text while maintaining context
- 📄 **PDF Support** - Extract and analyze text from PDF documents
- 🎨 **Web Interface** - Modern, intuitive UI for easy interaction
- 🔌 **RESTful API** - Comprehensive API endpoints for programmatic access
- 📦 **Containerized** - Docker support for easy deployment
- 🚀 **Cloud Ready** - Deployed on Railway cloud platform
- ⚡ **Fast & Scalable** - Built with FastAPI for high performance

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (React/HTML)                  │
│              https://presidio-pii-detector.up.railway.app │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/HTTPS
                     │
┌────────────────────▼────────────────────────────────────┐
│               FastAPI Backend (Python)                    │
│         https://presidio-pii-detector-production.up.railway.app   │
├─────────────────────────────────────────────────────────┤
│  • Microsoft Presidio Analyzer                          │
│  • Custom PII Recognizers (PAN, Aadhaar, VoterId, etc) │
│  • PDF Processing (pdfplumber)                          │
│  • spaCy NLP Models                                      │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript
- Responsive Design

**Backend:**
- Python 3.8+
- FastAPI - Modern web framework
- Microsoft Presidio - PII detection engine
- spaCy - NLP models
- pdfplumber - PDF processing
- Uvicorn - ASGI server

**Infrastructure:**
- Docker & Docker Compose
- Railway - Cloud deployment platform

---

## 🚀 Quick Start (Docker)

### Prerequisites
- Docker & Docker Compose installed
- Git

### Steps

1. **Clone the repository:**
```bash
git clone https://github.com/KRAZATEC/Presidio-PII-Detector.git
cd Presidio-PII-Detector
```

2. **Build and run with Docker Compose:**
```bash
docker-compose up -d
```

3. **Access the application:**
- Frontend: http://localhost:80
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

4. **Stop the services:**
```bash
docker-compose down
```

---

## 💻 Local Development Setup

### Backend Setup

1. **Create a virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

3. **Run the FastAPI server:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

Simply serve the frontend files (index.html, style.css, script.js) using any web server.

---

## 📚 API Documentation

### Base URL
- **Local:** `http://localhost:8000`
- **Production:** `https://presidio-pii-detector-production.up.railway.app`

### API Endpoints

#### 1. Analyze Text
**POST** `/analyze`

Detect PII entities in text.

**Request Body:**
```json
{
  "text": "My name is John Smith and my email is john@example.com",
  "threshold": 0.5
}
```

**Response:**
```json
{
  "entities": [
    {
      "entity": "PERSON",
      "start": 11,
      "end": 21,
      "confidence": 0.95,
      "value": "John Smith"
    },
    {
      "entity": "EMAIL_ADDRESS",
      "start": 40,
      "end": 62,
      "confidence": 0.99,
      "value": "john@example.com"
    }
  ]
}
```

#### 2. Mask Text
**POST** `/mask`

Redact PII entities from text.

**Request Body:**
```json
{
  "text": "My aadhar is 5647 3498 2848",
  "threshold": 0.5
}
```

**Response:**
```json
{
  "masked": "My aadhar is XXXX XXXX XXXX"
}
```

#### 3. Upload and Analyze PDF
**POST** `/upload-pdf`

Extract text from PDF and detect PII.

**Request:**
- Form data with file upload

**Response:**
```json
{
  "entities": [
    {
      "entity": "CREDIT_CARD",
      "confidence": 0.87,
      "value": "4532-XXXX-XXXX-XXXX"
    }
  ]
}
```

### Detected Entities

- PERSON
- EMAIL_ADDRESS
- PHONE_NUMBER (Mobile Number - India)
- CREDIT_CARD
- BANK_ACCOUNT
- LOCATION
- PAN (Permanent Account Number - India)
- AADHAAR (Aadhaar Number - India)
- VOTER_ID (Voter ID - India)
- ORG_ID (Organization ID - Custom)

---

## 🐳 Docker Deployment

### Single Service Deployment

**Backend:**
```bash
cd backend
docker build -t presidio-backend .
docker run -p 8000:8000 presidio-backend
```

**Frontend:**
```bash
cd frontend
docker build -t presidio-frontend .
docker run -p 80:80 presidio-frontend
```

### Using Docker Compose

```bash
docker-compose up -d
```

Services will be available at:
- Frontend: http://localhost:80
- Backend: http://localhost:8000

---

## ☁️ Railway Deployment

Deploy both frontend and backend services to Railway as separate services.

### Prerequisites
- Railway account (https://railway.com)
- GitHub repository connected to Railway

### Deployment Steps

#### 1. **Create Backend Service**

1. Go to Railway Dashboard
2. Click "+ New Project"
3. Select "GitHub Repo" and choose your Presidio-PII-Detector repository
4. Configure the service:
   - **Name:** Presidio-PII-Detector (or preferred name)
   - **Root Directory:** `/backend`
   - **Build Command:** (leave default)
   - **Start Command:** (leave default for Dockerfile)
   - **Port:** 8000

5. Railway will automatically:
   - Detect the Dockerfile
   - Build the Docker image
   - Deploy the service

6. **Generate Public Domain:**
   - Go to Networking tab
   - Click "Generate Domain"
   - Set Port to 8000
   - Copy the generated URL (e.g., `https://presidio-pii-detector-production.up.railway.app`)

#### 2. **Create Frontend Service**

1. In the same Railway project, click "+ Create"
2. Select "GitHub Repo" and select the same repository
3. Configure the service:
   - **Name:** Frontend (or preferred name)
   - **Root Directory:** `/frontend`
   - **Builder:** Dockerfile
   - **Dockerfile Path:** `/frontend/Dockerfile`
   - **Port:** 80

4. Railway will automatically build and deploy

5. **Generate Public Domain:**
   - Go to Networking tab
   - Click "Generate Domain"
   - Set Port to 80
   - Copy the generated URL (e.g., `https://presidio-pii-detector.up.railway.app`)

#### 3. **Update Frontend API Endpoint**

1. Open `frontend/script.js`
2. Update the API endpoint (line 3):
   ```javascript
   const API = "https://presidio-pii-detector-production.up.railway.app";
   ```
3. Commit and push:
   ```bash
   git add frontend/script.js
   git commit -m "Update backend URL for production"
   git push
   ```

4. Railway will automatically redeploy the frontend with the updated configuration

### Production URLs

After deployment, you'll have:

**Frontend:** https://presidio-pii-detector.up.railway.app/

**Backend API:** https://presidio-pii-detector-production.up.railway.app/

### Monitoring

On Railway dashboard, you can:
- View deployment logs
- Monitor CPU and memory usage
- Check build history
- Scale instances
- Set environment variables

### Database Persistence

Railway supports database services if needed in the future. You can add:
- PostgreSQL
- MySQL
- MongoDB

Connect them via environment variables in your Railway project.

---

🚀 Deploying to Other Platforms
-------------------------------
### Deploying to AWS (ECS Fargate Example)

1. **Build and push images**
   - Build images locally or in CI.
   - Push to Amazon ECR.

2. **Create ECS task definition**
   - Define containers for `backend` and `frontend` using your ECR images.
   - Set environment variables from AWS SSM Parameter Store or Secrets Manager.

3. **Create ECS service**
   - Use Fargate launch type.
   - Attach an Application Load Balancer.
   - Map HTTP/HTTPS listeners to the frontend container port.

4. **Configure networking and domain**
   - Use a public subnet and security group allowing HTTP/HTTPS.
   - Point your domain to the ALB via Route 53 (optional).

### Deploying to Azure Container Apps / Web App for Containers

1. **Push Docker images** to Azure Container Registry.
2. **Create a Web App for Containers** (or Container App) from the Azure Portal.
3. **Set image source** to your ACR images for backend and frontend.
4. **Configure environment variables** in the Azure Portal.
5. **Assign custom domain and TLS** if needed.

> Note: Exact steps will vary per provider, but the core requirement is the same: run the Docker images (or `docker-compose` equivalent), supply the required environment variables, and expose the frontend over HTTP/HTTPS.

---

### 🧨 Testing

A dedicated `TEST` folder has been added to the project containing sample test cases. This folder is used to validate the functionality and working of the website.

**To run tests:**

1. Navigate to the TEST folder
2. Review the sample test cases provided
3. Execute the test cases against the application to verify correct PII detection and redaction
4. Ensure all detections match expected outputs

**Test Coverage:**

- Sample documents with various PII types
- Edge cases and special formatting
- Different document formats
- Performance validation
---

🧩 Troubleshooting
------------------

If something is not working as expected, check the common issues below before opening an issue.

- **Frontend not loading / blank page**
  - Make sure Docker containers are running: `docker ps` (you should see both frontend and backend services).
  - Verify you are opening `http://localhost:80` in the browser when running via Docker Compose.

- **Backend API not reachable**
  - Open `http://localhost:8000/docs` to confirm the FastAPI server is up.
  - If it fails, check container logs: `docker-compose logs backend`.
  - Ensure no other service is already using port `8000`.

- **PII not being detected correctly**
  - Confirm the text is in English (multilingual detection is not yet supported).
  - For **Employee/Organization IDs**, only IDs starting with `ORG` (like `ORG12345`) are reliably detected right now.
  - For **Location**, only some common places are detected; many cities/localities are not yet recognized.

- **Docker build or start fails**
  - Run `docker-compose down --volumes --remove-orphans` and then `docker-compose up --build`.
  - Ensure Docker and Docker Compose are installed and updated to the latest stable versions.

- **PDF upload issues**
  - Verify the PDF is not password-protected or corrupted.
  - Check backend logs for PDF parsing errors (`pdfplumber` related messages).

If the problem persists, please [open an issue](https://github.com/KRAZATEC/Presidio-PII-Detector/issues) with logs, steps to reproduce, and sample input.

---

## 🚀 Future Upgrades

- **Multilinguality**: Support for detecting PII across multiple languages to make the tool accessible globally
- UI  Improvements: Enhanced dark mode, responsive design for mobile devices, improved user experience with better navigation and accessibility features
- **Expanded Location Detection**: Detection for all kinds of locations (cities, states, countries, full addresses, ZIP/postal codes, GPS coordinates, landmarks, facilities, and points of interest)
- **Custom Entity Rules**: UI and config support for user-defined regex rules, lookup-based entities, and context-aware custom PII types without code changes
- **Storage & Integrations**: Optional integration with object storage (S3, GCS), databases, and document sources like SharePoint, Google Drive, and S3 buckets
- Real-time detection dashboard
- API rate limiting and caching improvements

---

⚠️ What is Not Working
----------------------

Currently, there are no known critical issues. However, the following areas are known limitations and may need improvement:

- **Organization / Employee ID Detection**: Custom `ORG_ID` detection currently works reliably only when the ID starts with the prefix `ORG` (for example, `ORG12345`). IDs with other prefixes or formats are not consistently detected.
- **Location Coverage**: `LOCATION` entity detection is limited to certain common place names and patterns. Many cities, localities, and less common addresses are not yet recognized, especially outside the currently tuned regions.
- Some edge cases in PII pattern matching may not be caught.
- Performance optimization for very large documents.
- Support for specialized PII formats from different regions.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---
<div align="center">

### ⭐ Star this repo if you found it helpful! ⭐

---
## 📄 License

This project is licensed under the MIT License.  
You are free to use, modify, and distribute this software for personal or commercial purposes, as long as the original copyright
and license notice are included in all copies or substantial portions of the software.

---

**Made with ❤️**

[Report Bug](https://github.com/KRAZATEC/Presidio-PII-Detector/issues) • [Request Feature](https://github.com/KRAZATEC/Presidio-PII-Detector/issues) • [Discussions](https://github.com/KRAZATEC/Presidio-PII-Detector/discussions)

</div>

---

