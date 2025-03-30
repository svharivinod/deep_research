# 📘 FactFlux: AI-Powered Deep Research Assistant

**FactFlux** is an intelligent research agent built with the OpenAI Agents SDK and Firecrawl. It allows you to automate deep web research and generate insightful, well-structured reports on any topic in minutes—no manual browsing required.

---

<details>
<summary>🚀 Introduction</summary>

FactFlux simplifies the process of gathering and synthesizing information from across the web. It uses Firecrawl for structured web scraping and OpenAI agents for analysis, making it a powerful tool for researchers, analysts, students, and anyone looking to save time and effort on information discovery.

</details>

---

<details>
<summary>✨ Features</summary>

- 🔎 Deep web research with Firecrawl API  
- 🧠 Insight generation and content enhancement using OpenAI agents  
- 🧾 Structured research report with citations and source analysis  
- 📥 Downloadable report in Markdown format  
- 🧩 Modular and extendable agent system  
- 🔐 Secure API key handling via Streamlit Secrets

</details>

---

<details>
<summary>⚙️ How It Works</summary>

1. You enter a research topic.
2. The **Research Agent** uses Firecrawl to gather and analyze web sources.
3. The **Elaboration Agent** enhances the report with examples, context, and insights.
4. The final output is displayed in Streamlit with an option to download.

</details>

---

<details>
<summary>📋 Requirements</summary>

- Python 3.8+
- Streamlit
- openai-agents
- firecrawl
- asyncio

> Optional: `python-dotenv` if running locally with `.env` (local dev only)

</details>

---

<details>
<summary>🧑‍💻 Installation</summary>

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/factflux.git
   cd factflux

2. **Create a virtual environment**
   python -m venv venv
   source venv/bin/activate   # For Linux/Mac
   .\venv\Scripts\activate    # For Windows

3. **Install Dependencies**
   pip install -r requirements.txt

4. **Setup API Keys**
   OPENAI_API_KEY = "your-openai-api-key"
   FIRECRAWL_API_KEY = "your-firecrawl-api-key"

</details>

---

<details>
<summary>💡 Example Research Topics</summary>

Try one of the following prompts:

- The future of quantum computing in artificial intelligence  
- How climate change is affecting global food security  
- Impact of remote work on employee productivity  
- Latest advancements in gene editing technologies  
- Ethical challenges of AI-generated content

</details>

---

<details> 
<summary>🛠️ Technical Details</summary>

**Tech Stack:**

- **Frontend:** Streamlit  
- **Backend Agents:** OpenAI Agents SDK  
- **Web Scraping:** Firecrawl API  
- **Key Management:** Streamlit Secrets  
- **Async Execution:** `asyncio` is used to handle agent flows  

**Agent Architecture:**

- `research_agent`: Performs web research using the `deep_research()` function tool  
- `elaboration_agent`: Enhances reports by adding depth, examples, and context  

</details>






