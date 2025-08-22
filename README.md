#  HR Agent System
An intelligent HR assistant that **automates resume screening and interview scheduling** using AI-powered agents.

##  Features
- 📄 **Job Description Embedding** — HR enters a job description that is converted into vector embeddings.
- 📑 **Resume Screening** — Upload multiple resumes (PDFs); the system finds **best-fit candidates**.
- 📊 **Performance Scoring** — Each candidate gets a matching score against the job description.
- 📅 **Interview Scheduling** — After HR selects candidates, interviews are booked via **Google Calendar API**.

##  Agents & Tools
A modular **multi-agent** setup with dedicated tools:
-  **LOADPDFTOSTORE** — Load and store resumes for processing.  
-  **INFOANDSUMMARY** — Extract key details and summarize each resume.  
-  **PERFORMANCESCORE** — Compute similarity/match score vs job description.  
-  **SCHEDULECALENDER** — Create interview events in Google Calendar.

##  Tech Stack
- **Backend:** Flask  
- **AI Framework:** LangChain  
- **Vector Store:** FAISS / ChromaDB (choose one)  
- **Embeddings:** `BAAI/bge-small-en` via HuggingFace  
- **LLM Runtime:** Groq API (`langchain_groq`)  
- **Scheduler:** Google Calendar API  
- **Utilities:** `pdfplumber`, `pydantic`, `langchain_huggingface`

##  Requirements
langchain  
flask  
pydantic  
pdfplumber  
langchain_groq  
langchain_huggingface  
google-api-python-client  
google-auth-oauthlib  
  

*(If you use FAISS or ChromaDB, add their packages as needed — e.g., `faiss-cpu` or `chromadb`.)*
    

# Install dependencies  
pip install -r requirements.txt  

## ⚙️ Configuration
1) **Google Calendar API**  
- Open Google Cloud Console → Enable Calendar API.  
- Create OAuth 2.0 Client ID credentials.  
- Download `credentials.json` and place it in the project root.  

2) **Environment Variables**  
Create a `.env` file in the project root:  
GROQ_API_KEY=your_groq_api_key  
HUGGINGFACEHUB_API_TOKEN=your_hf_api_key  

## ▶️ Usage
# Run the Flask app  
python app.py  

Open in your browser:  
http://127.0.0.1:5000/  

### Workflow
- Enter job description   
- Upload resumes 
- Review ranked candidates   
- Schedule interviews 

## Workflow
![Demo](https://github.com/fadhilHussain11/HireHR/blob/main/uploads/worflow.jpg)

##  Embeddings Example
from langchain_community.embeddings import HuggingFaceEmbeddings  
embeddings = HuggingFaceEmbeddings(  
    model_name="BAAI/bge-small-en",  
    show_progress=True  
)  

##  How It Works (High Level)
- **Embed Job Description** → Convert job description into vectors.  
- **Process Resumes** → Extract text from PDFs, embed, and store.  
- **Match & Rank** → Compare resumes with job description, generate performance scores.  
- **HR Selection** → HR picks the best candidate.  
- **Schedule Interview** → Event booked using Google Calendar API.  

##  Notes
- Keep `credentials.json` and `.env` out of version control (add to `.gitignore`).  
- Use valid date-time formats when creating events (e.g., ISO/RFC3339 strings).  

##  Future Improvements
- Add chat-based HR assistant for live Q&A.  
- Support multi-round interview workflows.  
- Integrate with Slack/Email notifications.  

## output calender schedule
![schedule](https://github.com/fadhilHussain11/HireHR/blob/main/uploads/calender_schedule.png)