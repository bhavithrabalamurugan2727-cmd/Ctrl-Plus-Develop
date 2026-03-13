# Product Requirements Document (PRD)
## Project Name: AI Generated Phishing Detection

### 1. Introduction & Objective
**Problem:** With the rise of AI, malicious actors are generating highly convincing phishing links, spam messages, and fraudulent calls (vishing) at an unprecedented scale. 
**Solution:** Build a reliable, real-time platform that leverages Artificial Intelligence to verify and check suspicious links, text messages, and voice calls submitted by users, protecting them from fraud.

### 2. Target Audience
*   **Everyday Internet Users:** Individuals who receive suspicious SMS messages, WhatsApp texts, or emails and want a quick verification.
*   **Vulnerable Populations:** Elderly users or those less tech-savvy who are frequent targets of call scams.
*   **Businesses (Future phase):** Companies wanting an API integration to automatically scan employee communications.

### 3. Core Features (Scope of Work)

#### 3.1. Link & URL Verification
*   **Feature:** Users can paste a suspicious link into the platform.
*   **Mechanisms:**
    *   **Threat Database Lookup:** Check URLs against known phishing databases (e.g., Google Safe Browsing, PhishTank).
    *   **Lexical Analysis:** Use ML to analyze the structural anomalies of the URL (e.g., homograph attacks, excessive subdomains).
    *   **Content Scanning (Optional/Background):** Scrape the target HTML quietly to detect fake login portals (e.g., looking like a bank login).
*   **Output:** A "Safe" or "Malicious" rating with a confidence percentage.

#### 3.2. Text Message & Email Verification
*   **Feature:** Users can copy-paste text from a message or email.
*   **Mechanisms:**
    *   **NLP Text Classification:** Use Natural Language Processing (NLP) models (e.g., BERT, RoBERTa, or LLM-based prompting) to detect urgency cues, requests for personal information, and common scam templates.
*   **Output:** Spam probability score with highlights of suspicious sentences.

#### 3.3. Voice Call Verification (Vishing)
*   **Feature:** Users can upload an audio recording of a suspicious call.
*   **Mechanisms:**
    *   **Speech-to-Text (STT):** Transcribe the audio file using AI (e.g., OpenAI Whisper).
    *   **Conversational NLP:** Analyze the transcript for coercive language, IRS/Tech Support scam scripts, and AI-generated voice patterns.
*   **Output:** Call transcript + Scam probability score.

#### 3.4. User Dashboard
*   **Feature:** A simple interface to input data.
*   **Mechanisms:** Clean, modern web UI with distinct tabs for "Link", "Text", and "Audio".

### 4. Non-Functional Requirements
*   **Performance:** URL and Text checks should return results in under 2 seconds. Audio processing should return in under 15 seconds.
*   **Privacy & Data Security:** User-submitted data (especially texts and audio) must not be tied to their personal identities. Data should be anonymized or deleted after processing unless explicitly opted-in for AI training.
*   **Scalability:** The backend must handle concurrent requests efficiently, as ML inference can be resource-heavy.

### 5. Technology Stack Setup
*   **Frontend (User Interface):** React.js or Next.js, styled with Tailwind CSS for a modern, responsive feel.
*   **Backend (API & Logic):** Python with FastAPI (chosen for its high performance and native compatibility with AI libraries).
*   **Database:** PostgreSQL (for storing scan history, feedback, and threat patterns).
*   **AI/ML Layer:**
    *   *Audio:* OpenAI Whisper API or Google Cloud STT.
    *   *Text:* Hugging Face Transformers, OpenAI API, or custom-trained Scikit-Learn models.
    *   *URLs:* Custom feature extraction using Python, combined with external API integrations.

### 6. Implementation Milestones

*   **Phase 1: Minimum Viable Product (MVP)**
    *   Set up basic FastAPI server & React frontend.
    *   Implement Text Message Verification using a pre-trained NLP model.
*   **Phase 2: Link Analysis Integration**
    *   Add URL parsing.
    *   Integrate third-party threat intelligence APIs.
    *   Train/deploy the URL lexical analysis model.
*   **Phase 3: Voice Verification**
    *   Implement file upload handling on the frontend.
    *   Integrate Speech-to-Text inference pipeline.
*   **Phase 4: Polish & Deploy**
    *   Add user feedback mechanism (e.g., "Was this helpful?").
    *   Deploy frontend to Vercel/Netlify and Backend to Render/AWS.
