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
        "prize": 40, "lottery": 50, "bank": 20, "otp": 50, 
        "login": 25, "security": 20, "update": 15, "fraud": 30,
        "free": 30, "instant": 30, "cash": 30, "money": 30,
        "guaranteed": 30, "claim": 30, "reward": 30, "bonus": 30,
        "gift": 20, "winner": 40, "selected": 20, "offer": 20, 
        "limited": 20, "act now": 30, "crypto": 20, "bitcoin": 20, 
        "profit": 30, "get": 15, "transfer": 20, "package": 20, 
        "delivery": 20, "pay": 20
    }
    score = 0
    
    for word, points in suspicious_keywords.items():
        if word in text_lower:
            score += points
            
    # Check for digit sequences indicating large money/amounts like 5000
    if re.search(r'\$?[0-9]{3,}', text_lower) and not re.search(r'(otp|code|pin|verification)[\s:]*[0-9]{4,6}', text_lower):
        score += 25
            
    # Logic: Detect standard OTP/Verification messages and whitelist them
    is_otp_message = False
    otp_patterns = [
        r'[0-9]{4,8}\s+(is|for).*?(otp|code|verification|pin)',
        r'(otp|code|pin|verification).*?[0-9]{4,8}',
        r'[0-9]{4,8}.*?(otp|code|pin|verification)',
        r'do not share this (otp|code|pin)'
    ]
    
    if any(re.search(pattern, text_lower) for pattern in otp_patterns):
        is_otp_message = True
        
    # Standard OTPs often contain words like 'otp', 'verify', 'security' which we penalize. 
    # If it strictly follows the structure of a system OTP message without other phishing hooks (like links), reduce score.
    if is_otp_message and "http" not in text_lower and ".com" not in text_lower:
        score -= 75
            
    score = max(0, min(100, score))
            
    if score >= 55:
        return "danger", "High Risk: This message contains multiple triggers commonly associated with phishing or scam attempts. Do not reply or click any links.", score
    elif score >= 20:
        return "warning", "Moderate Risk: This message seems suspicious. Please verify the sender before taking any action.", score
    else:
        return "safe", "Safe: No obvious signs of phishing detected. Still, always remain cautious.", score


class LinkSandbox:
    """Simulates an isolated environment for link detonation in a sandbox."""
    def __init__(self):
        # Improved patterns to prevent false positives like matching "chatgpt.com" to "t.co"
        self.malicious_patterns = [r"bit\.ly", r"//t\.co/", r"tinyurl\.com", r"redirect", r"\.exe$", r"\.zip$", r"ow\.ly", r"is\.gd"]
        self.high_risk_keywords = [
            'login', 'verify', 'secure', 'update', 'account', 'banking',
            'confirm', 'free', 'gift', 'support', 'service', 'validation',
            'auth', 'billing', 'invoice', 'helpdesk', 'recovery', 'wallet',
            'paypal', 'amazon', 'apple', 'microsoft', 'google', 'netflix',
            'post', 'dhl', 'fedex', 'ups', 'track', 'parcel'
        ]
        self.safe_domains = [
            'youtube.com', 'google.com', 'chatgpt.com', 'github.com',
            'linkedin.com', 'twitter.com', 'x.com', 'facebook.com',
            'instagram.com', 'apple.com', 'microsoft.com', 'amazon.com',
            'wikipedia.org'
        ]

    def detonate(self, url):
        """Simulates following redirects and checking page behavior in isolation."""
        analysis_steps = [
            "Initializing secure sandbox container...",
            "Resolving DNS and checking SSL certificates...",
            "Tracing redirects and expanding shorteners...",
            "Analyzing target DOM for hidden scripts...",
            "Checking signatures against threat databases..."
        ]
        
        score = 0
        findings = []
        url_lower = url.lower()
        
        import urllib.parse
        parsed_url = urllib.parse.urlparse(url_lower)
        domain = parsed_url.netloc

        # Simple heuristics
        if "http://" in url_lower:
            score += 30
            findings.append("Unsecured HTTP connection.")
            
        if len(url) > 75:  # Many valid URLs are over 60 (like chatgpt)
            score += 20
            findings.append("Suspiciously long URL length.")
            
        if re.search(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', domain):
            score += 40
            findings.append("Contains raw IP address instead of domain.")
            
        path_end = parsed_url.path.split("/")[-1]
        is_uuid = re.match(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', path_end)
        
        if "-" in path_end and len(path_end) > 15 and not is_uuid:
            score += 20
            findings.append("Long dash separated paths (possible obfuscation).")

        # Logic: Check for URL shorteners
        if any(re.search(p, url_lower) for p in self.malicious_patterns):
            score += 30
            findings.append("URL Shortener/Obfuscation detected.")

        # Logic: Check for phishing keywords in URL
        keyword_count = sum(1 for kw in self.high_risk_keywords if kw in url_lower)
        if keyword_count > 0:
            score += (keyword_count * 15)
            findings.append(f"Found {keyword_count} phishing-related keywords.")

        if domain.count('.') > 3:
            score += 25
            findings.append("Excessive subdomains (score +25).")

        # Logic: Check for homoglyphs or misleading domains (e.g., paypa1, g00gle)
        if domain and re.search(r'[0-9]', domain):
            score += 15
            findings.append("Suspected homoglyph or misleading digit in domain.")

        # Logic: Check for suspicious TLDs
        cheap_tlds = ['.xyz', '.top', '.pw', '.cc', '.club', '.online', '.site', '.click', '.link', '.vip']
        if any(domain.endswith(tld) for tld in cheap_tlds):
            score += 35
            findings.append("Suspicious Top-Level Domain (TLD).")

        # Logic: Deduct points for known safe domains
        if any(domain == safe or domain.endswith('.' + safe) for safe in self.safe_domains):
            score -= 60
            findings.append(f"Verified known safe domain: {domain}.")

        score = max(0, min(100, score))
        
        if score >= 50:
            status = "danger"
            message = "High Risk: Sandbox detonation reveals malicious behavior or deceptive properties. Do not visit!"
        elif score >= 20:
            status = "warning"
            message = "Moderate Risk: The sandbox detected slightly suspicious characteristics (e.g., unsecure connection)."
        else:
            status = "safe"
            message = "Safe: The URL successfully passed all sandbox detonation checks and appears legitimate."
            
        return status, message, score, findings, analysis_steps


def analyze_call(transcript):
    """Mock AI analysis for voice call transcripts"""
    time.sleep(2)
    transcript_lower = transcript.lower()
    
    coercive_phrases = {
        "police": 40, "arrest": 40, "fine": 30, "gift card": 50,
        "social security": 40, "cancel": 20, "immediately": 30,
        "irs": 40, "warrant": 40, "compromised": 30, "transfer": 20,
        "tax": 30, "lawsuit": 40, "fbi": 40, "courthouse": 30,
        "magistrate": 30, "suspended": 30, "deportation": 40,
        "customs": 30, "border protection": 30, "illegal package": 40,
        "money laundering": 40, "drug": 30, "cartel": 40,
        "bank account": 20, "routing number": 40, "wire": 30,
        "bitcoin": 30, "crypto": 30, "western union": 30, "moneygram": 30,
        "target gift card": 50, "apple gift card": 50, "google play": 50,
        "don't tell anyone": 40, "stay on the phone": 40, "secret": 30,
        "remote access": 40, "anydesk": 50, "teamviewer": 50,
        "refund": 30, "overcharged": 30, "accidental deposit": 40
    }
    score = 0
    
    for phrase, points in coercive_phrases.items():
        if phrase in transcript_lower:
            score += points
            
    # Check for urgency cues
    urgency_cues = ["right now", "today", "urgent", "last warning", "final notice"]
    if any(cue in transcript_lower for cue in urgency_cues):
        score += 25
            
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
        
        if st.button("Deep Sandbox Scan", key="btn_link"):
            if user_link.strip():
                sandbox = LinkSandbox()
                st.info("🚀 Initiating Sandbox Detonation...", icon="🔒")
                
                # UI elements for dynamic updates
                status_text = st.empty()
                progress_bar = st.progress(0)
                
                # Run sandbox logic
                status, message, score, findings, steps = sandbox.detonate(user_link)
                
                # Simulate step-by-step progress
                for i, step in enumerate(steps):
                    status_text.text(f"Sandbox Action: {step}")
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(0.4) # Simulating processing time
                
                status_text.empty()
                progress_bar.empty()
                
                # Format findings as bullet points
                findings_html = "".join([f"<li>{f}</li>" for f in findings]) if findings else "<li>No immediate red flags detected during sandbox execution.</li>"
                
                st.markdown(f"""
                <div class="report-card {status}">
                    <h3>🛡️ Sandbox Report</h3>
                    <p><strong>Status:</strong> {status.upper()}</p>
                    <p><strong>Threat Score:</strong> {score}/100</p>
                    <p><strong>Analysis:</strong> {message}</p>
                    <hr style="border-top: 1px solid rgba(255,255,255,0.3);">
                    <p><strong>Sandbox Findings:</strong></p>
                    <ul>
                        {findings_html}
                    </ul>
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
