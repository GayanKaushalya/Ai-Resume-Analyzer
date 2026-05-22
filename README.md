# 🤖 AI Resume Analyzer & ATS Scoring Platform

# 🛠 Tech Stack

<p align="left">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>

<img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white"/>

<img src="https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white"/>

<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white"/>

<img src="https://img.shields.io/badge/Tesseract_OCR-4285F4?style=for-the-badge"/>

<img src="https://img.shields.io/badge/PyMuPDF-FF6F00?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>

<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white"/>

<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white"/>

<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>

</p>

---

An advanced AI-powered Resume Analyzer and ATS (Applicant Tracking System) Scoring Platform built using **FastAPI**, **Machine Learning**, **NLP**, and **OCR** technologies.

The system allows users to upload resumes, analyze skills, compare resumes with job descriptions, calculate ATS compatibility scores, and generate AI-powered recommendations.

---

# 🚀 Features

## 🔐 Authentication & Security

- JWT Authentication
- Secure Password Hashing
- Role-Based Access Control
- Protected API Routes

---

## 📄 Resume Processing

- Upload PDF, DOCX, and Image Resumes
- OCR-Based Text Extraction
- Resume Parsing
- Resume History Tracking

---

## 🧠 AI & NLP Features

- Skill Extraction
- ATS Score Calculation
- Job Description Matching
- Missing Skill Detection
- Resume Recommendations
- Semantic Similarity Analysis
- Resume Ranking System
- AI Resume Summary Generation

---

## 📊 Analytics

- Top Skills Dashboard
- Resume Analytics
- ATS Performance Metrics
- User Statistics

---

## ⚡ Backend Features

- RESTful API Architecture
- Async API Processing
- Background Task Queue
- Dockerized Setup
- PostgreSQL Integration
- Redis Caching

---

# 🏗 System Architecture

```text
User
   ↓
FastAPI Backend
   ↓
Authentication System
   ↓
Resume Upload Module
   ↓
OCR & Text Extraction
   ↓
NLP Processing Engine
   ↓
ATS Scoring Engine
   ↓
Machine Learning Analysis
   ↓
PostgreSQL Database
   ↓
Analytics Dashboard
```

---

# 📂 Project Structure

```text
ai-resume-analyzer/
│
├── app/
│   ├── api/
│   ├── auth/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── nlp/
│   ├── ml/
│   ├── ocr/
│   ├── utils/
│   └── main.py
│
├── tests/
├── docker/
├── uploads/
├── requirements.txt
├── docker-compose.yml
├── README.md
└── .env
```

---

# 📌 Core Modules

## 🔹 Authentication Module

- User Registration
- Login System
- JWT Token Generation
- Password Encryption

---

## 🔹 Resume Upload Module

- Upload Resume Files
- Validate File Types
- Secure File Storage

---

## 🔹 OCR Module

- Extract Text From Images
- Process Scanned Resumes
- OCR Optimization

---

## 🔹 NLP Engine

- Skill Extraction
- Keyword Analysis
- Experience Detection
- Education Parsing

---

## 🔹 ATS Scoring Engine

- Resume vs Job Description Matching
- ATS Compatibility Score
- Missing Skill Analysis
- Recommendation Generation

---

## 🔹 Machine Learning Module

- TF-IDF Similarity
- Resume Ranking
- Semantic Matching
- AI Insights

---

# 📡 API Endpoints

## 🔐 Authentication APIs

```http
POST /auth/register
POST /auth/login
```

---

## 📄 Resume APIs

```http
POST /resume/upload
GET /resume/{id}
DELETE /resume/{id}
```

---

## 🧠 Analysis APIs

```http
POST /resume/analyze
POST /resume/match-job
GET /resume/score/{id}
```

---

## 📊 Analytics APIs

```http
GET /analytics/dashboard
GET /analytics/top-skills
GET /analytics/stats
```

---

# 🧪 Future Improvements

- AI Chatbot Assistant
- Interview Question Generator
- Multi-Language Resume Analysis
- Cloud Storage Integration
- Frontend Dashboard
- Real-Time Notifications
- Resume Templates
- AI Career Recommendations

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ai-resume-analyzer.git
```

---

## 2️⃣ Navigate Into Project

```bash
cd ai-resume-analyzer
```

---

## 3️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 4️⃣ Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6️⃣ Run Server

```bash
uvicorn app.main:app --reload
```

---

# 🐳 Docker Setup

## Run Using Docker

```bash
docker-compose up --build
```

---

# 📈 Development Roadmap

## ✅ Phase 1

- Project Setup
- FastAPI Configuration
- Database Setup

## ✅ Phase 2

- Authentication System
- JWT Security

## ✅ Phase 3

- Resume Upload & Parsing

## ✅ Phase 4

- OCR Integration

## ✅ Phase 5

- NLP Processing

## ✅ Phase 6

- ATS Scoring Engine

## ✅ Phase 7

- Machine Learning Integration

## ✅ Phase 8

- Analytics Dashboard

## ✅ Phase 9

- Docker Deployment

---

# 🎯 Learning Outcomes

This project demonstrates knowledge of:

- Backend Development
- REST API Design
- AI Integration
- OCR Processing
- NLP Pipelines
- Machine Learning
- Database Design
- Authentication & Security
- Docker & Deployment
- Software Architecture

---

# 📸 Screenshots

> Add screenshots here after building the UI/dashboard.

---

# 🤝 Contributing

Contributions are welcome!

Fork the repository and submit a pull request.

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Gayan
