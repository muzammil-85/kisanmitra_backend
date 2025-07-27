# 🌾 KisanMitra Backend

KisanMitra is a backend service built using Django and Firebase to support Indian farmers with tools for crop market price tracking, community discussions, and agri-scheme applications. This backend integrates with Firestore and Google Cloud Storage, and is ready for deployment on Google Cloud Run.

---

## 🔧 Tech Stack

- **Backend**: Django, Django REST Framework  
- **Database**: Google Firestore (Firebase)  
- **Storage**: Google Cloud Storage  
- **AI Integration**: Gemini (Google Generative AI)  
- **Deployment**: Google Cloud Run  
- **Authentication**: Firebase Service Account  

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/kisanmitra_backend.git
cd kisanmitra_backend
```

### 2. Create a Virtual Environment & Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY=your-secret-key
FIREBASE_PROJECT_ID=your-firebase-project-id
GOOGLE_APPLICATION_CREDENTIALS=/app/firebase-key.json
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
```

Also, place your Firebase service account key file and name it:

```
firebase-key.json
```

---

### 4. Run Migrations & Start Development Server

```bash
python manage.py migrate
python manage.py runserver
```