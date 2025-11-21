import os
import json
import base64
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# ---------------------------
# Paths and OpenAI setup
# ---------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
GITHUB_LINK = "https://github.com/Sathya0990/AI-Automation-Reachout"


# ---------------------------
# Loaders and Prompt Builder
# ---------------------------

def load_contacts(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_prompt_template(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(template: str, job_summary: str, profile_summary: str, contact: dict) -> str:
    prompt = template
    prompt = prompt.replace("{{JOB_SUMMARY}}", job_summary)
    prompt = prompt.replace("{{PROFILE_SUMMARY}}", profile_summary)
    prompt = prompt.replace("{{NAME}}", contact.get("Name", ""))
    prompt = prompt.replace("{{ROLE}}", contact.get("Job Title", ""))
    prompt = prompt.replace("{{COMPANY}}", contact.get("Company", ""))
    prompt = prompt.replace("{{EXTRA_CONTEXT}}", contact.get("LinkedIn Experience for Raisin", "") or contact.get("Location", ""))
    prompt = prompt.replace("{{GITHUB_LINK}}", GITHUB_LINK)
    return prompt


def generate_email(prompt: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a precise assistant that outputs strictly valid JSON with keys 'subject' and 'body'."
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=0.4,
    )

    content = response.choices[0].message.content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("Model did not return valid JSON. Raw content was:\n")
        print(content)
        raise


# ---------------------------
# Gmail API Setup
# ---------------------------

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_gmail_service():
    creds = None
    token_path = BASE_DIR / "token.json"

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(BASE_DIR / "credentials" / "oauth_client.json"),
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def create_message(sender, to, subject, body_text, attachment_path=None):
    message = MIMEMultipart()
    message["To"] = to
    message["From"] = sender
    message["Bcc"] = "sprabhala@binghamton.edu"
    message["Subject"] = subject

    message.attach(MIMEText(body_text, "plain"))

    if attachment_path:
        with open(attachment_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        message.attach(part)

    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": encoded}


def send_message(service, user_id, message):
    sent = service.users().messages().send(userId=user_id, body=message).execute()
    print(f"Email sent. Gmail ID: {sent.get('id')}")


# ---------------------------
# Main Flow
# ---------------------------

def main():
    job_summary = (
    "The role involves building, maintaining, and improving low-code and AI-driven workflows "
    "that support legal and compliance operations, such as intake, triage, document review, "
    "reporting, and knowledge management. It requires designing and refining prompt structures "
    "for generative AI tools, automating recurring tasks, and documenting logic clearly to ensure "
    "transparency and scalability. The ideal candidate is curious, analytical, and experienced with "
    "automation, prompt engineering, and process efficiency, especially in data or operations-focused environments."
)


    profile_summary = (
    "I come from a data analysis and automation background and have built end-to-end workflows "
    "using several generations of modern language models. My experience includes designing structured "
    "prompt systems, building a RAG-based document analysis platform, and creating automation pipelines "
    "that significantly reduced manual review time. I focus on clarity, reproducibility, and practical "
    "impact when designing automations, and I enjoy turning complex processes into simple, efficient workflows."
)


    contacts = load_contacts(BASE_DIR / "data" / "example_contact.json")
    template = load_prompt_template(BASE_DIR / "src" / "prompt_template.txt")

    gmail_service = get_gmail_service()
    sender_email = "sprabhala@binghamton.edu"    # <-- Use YOUR email here
    resume_path = BASE_DIR / "resume" / "SathyaPrabhala_Resume.pdf" # <-- Add résumé later

    for contact in contacts:
        print(f"\nGenerating email for: {contact.get('Name')}")

        prompt = build_prompt(template, job_summary, profile_summary, contact)
        result = generate_email(prompt)

        subject = result.get("subject", "")
        body = result.get("body", "")

        print("\nSubject:", subject)
        print("\nBody:", body)

        msg = create_message(
            sender=sender_email,
            to=contact["Email"],       # Send to YOUR email for test
            subject=subject,
            body_text=body,
            attachment_path=resume_path,
        )

        send_message(gmail_service, "me", msg)


if __name__ == "__main__":
    main()
