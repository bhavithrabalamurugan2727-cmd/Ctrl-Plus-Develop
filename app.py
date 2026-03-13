import streamlit as st
import time
import random
import re

# Set up the page configuration
st.set_page_config(
    page_title="ShieldAI - Phishing Detector",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .report-card {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        color: white;
    }
    .safe {
        background-color: #2e7d32;
    }
    .warning {
        background-color: #edad0e;
        
    }
    .danger {
        background-color: #c62828;
    }
</style>
""", unsafe_allow_html=True)


def analyze_text(text):
    """Mock AI analysis for text messages"""
    time.sleep(1.5) # Simulate processing time
    text_lower = text.lower()
    
    suspicious_keywords = {
        "urgent": 30, "account": 20, "suspend": 30, "locked": 30, 
        "click": 25, "password": 40, "verify": 25, "win": 30, 
        "prize": 30, "lottery": 40, "bank": 20, "otp": 50, 
        "login": 25, "security": 20, "update": 15, "fraud": 30
    }
    score = 0
    
    for word, points in suspicious_keywords.items():
        if word in text_lower:
            score += points
            
    score = min(100, score)
            
    if score >= 55:
        return "danger", "High Risk: This message contains multiple triggers commonly associated with phishing or scam attempts. Do not reply or click any links.", score
    elif score >= 20:
        return "warning", "Moderate Risk: This message seems suspicious. Please verify the sender before taking any action.", score
    else:
        return "safe", "Safe: No obvious signs of phishing detected. Still, always remain cautious.", score


def analyze_link(url):
    """Mock AI analysis for URLs"""
    time.sleep(1.2)
    score = 0
    url_lower = url.lower()
    
    # Simple heuristics
    if "http://" in url_lower:
        score += 30 # Unsecure
    if len(url) > 60:
        score += 20 # Suspiciously long
    if re.search(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', url):
        score += 50 # Contains IP address instead of domain
    if "-" in url.split("/")[-1] and len(url.split("/")[-1]) > 15:
        score += 20 # Long dash separated paths
    if any(kw in url_lower for kw in ['login', 'verify', 'secure', 'update']):
        score += 20
    if url_lower.count('.') > 3:
        score += 25
        
    score = min(100, score)
        
    if score >= 50:
        return "danger", "High Risk: This URL has characteristics of a malicious or deceptive website. Do not visit.", score
    elif score >= 20:
        return "warning", "Moderate Risk: The URL looks slightly suspicious (e.g., unsecure connection or unusual structure).", score
    else:
        return "safe", "Safe: The URL appears legitimate and secure.", score


def analyze_call(transcript):
    """Mock AI analysis for voice call transcripts"""
    time.sleep(2)
    transcript_lower = transcript.lower()
    
    coercive_phrases = {
        "police": 40, "arrest": 40, "fine": 30, "gift card": 50,
        "social security": 40, "cancel": 20, "immediately": 20,
        "irs": 40, "warrant": 40, "compromised": 30, "transfer": 20
    }
    score = 0
    
    for phrase, points in coercive_phrases.items():
        if phrase in transcript_lower:
            score += points
            
    score = min(100, score)
            
    if score >= 50:
        return "danger", "High Risk: The caller is using high-pressure tactics or requesting sensitive information typical of vishing (voice phishing) scams. Hang up immediately.", score
    elif score >= 20:
        return "warning", "Moderate Risk: The conversation contains unusual requests. Verify the caller's identity through official channels.", score
    else:
        return "safe", "Safe: The call transcript does not indicate immediate malicious intent.", score


def main():
    st.title("🛡️ ShieldAI")
    st.subheader("AI-Powered Protection Against Phishing, Smishing & Vishing")
    
    st.markdown("Welcome to the ShieldAI sandbox. Select an option below to test suspicious messages, links, or call transcripts.")
    
    tab1, tab2, tab3 = st.tabs(["💬 Text Message", "🔗 Link/URL", "📞 Voice Call"])
    
    # --- TEXT MESSAGE TAB ---
    with tab1:
        st.write("### Verify SMS, WhatsApp, or Email Text")
        user_text = st.text_area("Paste the suspicious message here:", placeholder="Dear customer, your bank account is locked. Click here to verify...", height=150)
        
        if st.button("Scan Text", key="btn_text"):
            if user_text.strip():
                with st.spinner("AI is analyzing the message for manipulation and urgency cues..."):
                    status, message, score = analyze_text(user_text)
                    
                st.markdown(f"""
                <div class="report-card {status}">
                    <h3>Report</h3>
                    <p><strong>Status:</strong> {status.upper()}</p>
                    <p><strong>Threat Score:</strong> {score}%</p>
                    <p><strong>Analysis:</strong> {message}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Please enter some text to analyze.")

    # --- LINK TAB ---
    with tab2:
        st.write("### Verify Suspicious Links")
        user_link = st.text_input("Paste the URL here:", placeholder="http://secure-login.bank-update.com/verify")
        
        if st.button("Scan Link", key="btn_link"):
            if user_link.strip():
                with st.spinner("AI is analyzing the URL structure and searching threat databases..."):
                    status, message, score = analyze_link(user_link)
                    
                st.markdown(f"""
                <div class="report-card {status}">
                    <h3>Report</h3>
                    <p><strong>Status:</strong> {status.upper()}</p>
                    <p><strong>Threat Score:</strong> {score}%</p>
                    <p><strong>Analysis:</strong> {message}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Please enter a URL to analyze.")

    # --- VOICE CALL TAB ---
    with tab3:
        st.write("### Verify Phone Calls")
        st.info("For this sandbox, you can paste the text transcript of a suspicious call. In production, this would accept an audio file upload (.mp3, .wav) and use AI Speech-to-Text.")
        call_transcript = st.text_area("Enter the call transcript:", placeholder="Hello, this is the police department. There is a warrant for your arrest regarding social security fraud. You must pay a fine in gift cards immediately...", height=150)
        
        if st.button("Analyze Call Transcript", key="btn_call"):
            if call_transcript.strip():
                with st.spinner("AI is analyzing the conversational intent and pressure tactics..."):
                    status, message, score = analyze_call(call_transcript)
                    
                st.markdown(f"""
                <div class="report-card {status}">
                    <h3>Report</h3>
                    <p><strong>Status:</strong> {status.upper()}</p>
                    <p><strong>Threat Score:</strong> {score}%</p>
                    <p><strong>Analysis:</strong> {message}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Please enter a transcript to analyze.")

if __name__ == "__main__":
    main()
