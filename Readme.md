# AI Prompt & Automation Outreach Demo

This repository contains a working demonstration of how to generate and send tailored outreach emails using structured prompt engineering and a small Python automation workflow. The goal of this project is simple: instead of submitting a cold application for the AI Prompt & Automation Analyst role at Raisin, I wanted to show what I can build in a short time and how I approach automation, LLM workflows, and prompt design.

This project generated (and sent) the outreach email that accompanied my application.

---

## 🚀 Why This Project Exists

The role I’m applying for focuses on:
- AI-driven workflow automation  
- Prompt engineering  
- Process simplification  
- Reducing manual friction  
- Clear documentation and logic  

So rather than explain what I can do, I decided to demonstrate it.

This project shows:
- How I structure prompts for stability, predictability, and token efficiency  
- How I build small automations quickly  
- How LLMs can fit cleanly inside workflow boundaries  
- How to reduce manual work through automated communication  
- How to turn a simple task (outreach) into a structured, scalable system  

---

## 🧠 High-Level Workflow

- input_contact_data.json 
    #### Local only, private (ignored in Git)

- prompt_template.txt 
    #### Structured prompt with variables

- generate_email.py 
    #### Builds prompt → OpenAI → email text

- OpenAI API 
    #### Returns JSON: { "subject": "...", "body": "..." }

- Gmail API (OAuth) 
    #### Sends the email automatically

- Automated Outreach Delivered


The workflow is intentionally simple, but the design principles are the same ones used in real automations: clarity, structure, separation of concerns, and predictable outputs.

---

## ✍️ Structured Prompt Engineering

The prompt template follows a structured pattern I use in real automation work:

- **Goal** – What the model must produce  
- **Context** – Job summary, my profile, contact info  
- **Instructions** – Tone, constraints, email style  
- **Constraints** – Two short paragraphs, simple language  
- **Output format** – Strict JSON for automated parsing  
- **Quality checks** – Must reference role + background  

Using structure keeps:
- token usage low  
- outputs stable  
- results easy to automate  
- prompts maintainable for long-term workflows  

---

## ⚙️ Tech Stack

- Python 3  
- OpenAI API (gpt-4.1-mini)  
- Gmail API (OAuth2)  
- dotenv for secrets  
- JSON-based templating  
- Email MIME handling  

---

## 🔒 Security & Privacy

All sensitive data is kept local and excluded using `.gitignore`:

- Contact information  
- OAuth credentials  
- Gmail tokens  
- `.env` with API keys  
- Résumé files  

The repo includes a **public-safe example** file for demonstration only.

---

## 🛠️ How It Works (Summary)

1. You place your contact data in a local JSON file.  
2. A template prompt defines structure + constraints.  
3. The script injects job details, profile summary, and contact data.  
4. OpenAI returns an email subject + body in JSON.  
5. Gmail API sends the email (optionally with a PDF résumé).  
6. The workflow completes with zero manual typing.

---

## 🔧 Future Extensions (Optional Ideas)

This workflow can easily be extended into:
- Multi-contact outreach campaigns  
- Apollo API integration  
- LinkedIn scraping  
- Email routing logic  
- Prompt A/B testing  
- Token-cost monitoring  
- Zapier/Make integrations  
- Legal ops intake automations  
- Document triage workflows  

---

## 📄 Example Files

- `src/generate_email.py` – Main automation script  
- `src/prompt_template.txt` – Structured prompt for LLM  
- `data/example_contact_public.json` – Safe demo contact file  

---

## 🙌 About

This project was built in a few hours as a proof-of-work demonstration of my approach to automation and AI-assisted workflows. If you're reviewing this as part of the hiring process — thank you for taking a look. I’d be glad to walk through the system design in more detail.

---

## 📬 Contact

**Sathya Prabhala**  
NYC, USA  
sprabhala@binghamton.edu  
607-245-6637
