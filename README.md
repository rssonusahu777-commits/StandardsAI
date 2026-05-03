# 🚀 StandardsAI

**AI-Powered BIS Standards Discovery Engine**

StandardsAI is an intelligent web application that helps users quickly find relevant **Bureau of Indian Standards (BIS)** codes using AI. Instead of manually searching through documents, users can simply enter a product description and get accurate, categorized standards instantly.

---

## 🌐 Live Demo

* **Frontend (Netlify):**
  https://vermillion-froyo-5bf6f4.netlify.app

* **Backend API (Railway):**
  https://web-production-63119.up.railway.app

---

## 🧠 Problem

Finding BIS standards manually is:

* Time-consuming
* Requires domain expertise
* Inefficient for quick decisions

---

## 💡 Solution

StandardsAI solves this by:

1. Accepting a simple product description
2. Detecting the relevant category
3. Using AI (RAG) to retrieve matching standards
4. Displaying results instantly with scores

---

## ⚙️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* FastAPI
* FAISS (vector search)
* Sentence Transformers

### Deployment

* Netlify (Frontend hosting)
* Railway (Backend hosting)
* GitHub (Version control)

---

## 🔥 Features

* 🔍 Smart product-based search
* 🧠 Category-aware AI retrieval
* ⚡ Fast response time
* 📊 Relevance scoring
* 🎯 Simple and clean UI

---

## 🏗️ Architecture

```
User → Frontend (Netlify)
       ↓
    Backend API (Railway)
       ↓
   RAG Engine + FAISS
       ↓
   BIS Standards Database
```

---

## 📁 Project Structure

```
StandardsAI/
│
├── backend/            # FastAPI backend (Railway)
│
├── index.html          # UI
├── app.js              # Frontend logic
├── style.css           # Styling
│
└── README.md
```

---

## 🚀 Run Locally

### Backend

```bash
cd backend/src
uvicorn main:app --reload
```

Runs at:

```
http://127.0.0.1:8000
```

---

### Frontend

```bash
python -m http.server 5500
```

Open:

```
http://127.0.0.1:5500
```

---

## 🌍 Deployment

* **Frontend deployed on Netlify**
* **Backend deployed on Railway**

Make sure frontend API URL points to:

```
https://web-production-63119.up.railway.app
```

---

## 🏆 Use Cases

* Engineers & Builders
* Manufacturers
* Students
* Compliance teams

---

## 🔮 Future Improvements

* Larger BIS dataset integration
* Better ranking models
* Authentication system
* Mobile responsiveness
* Multi-language support

---

## 👨‍💻 Author

**Chandrakant Sahu**

---

## ⭐ Support

If you found this project useful, give it a ⭐ on GitHub!
