# 🛡️ Minor-Guard — Age-Aware AI Safety System

> A child-safe AI system that combines **Retrieval-Augmented Generation (RAG)** with **age-aware guardrails** to deliver safe, accurate, and developmentally appropriate responses for users aged **5–17**.

---

## 🚀 Overview

This project implements a **defense-in-depth architecture** for AI safety. Unlike standard chatbots, this system ensures that responses are **Safe + Useful + Age-Appropriate** simultaneously.

It achieves this through:
- 🔍 **RAG (Retrieval-Augmented Generation)**: Grounds answers in verified information to prevent hallucinations.
- 🧠 **Age-aware Guardrails**: Tailors the complexity, tone, and safety constraints based on the user's developmental stage.
- 🛡️ **Adversarial Resistance**: Actively detects and blocks harmful or jailbreak prompts.
- 📊 **Evaluation Engine**: Systematically measures safety, accuracy, and performance across different configurations.

---

## 🧱 Architecture Workflow

The system processes requests through a multi-stage pipeline to ensure safety and quality:

**`User prompt + age`** ➡️ **`Topic Router`** ➡️ **`RAG Context Retrieval`** ➡️ **`Guardrails + Logic`** ➡️ **`Safe Response`**

---

## 📁 Project Structure

```text
AI_Project/
├── app.py                  # Flask web application & API endpoints
├── main.py                 # CLI interface for chat, evaluation, and charts
├── simulator.py            # Core simulation and testing logic
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── data/
│   └── prompts.py          # System and test prompts
├── rag/
│   ├── database.py         # Vector/knowledge database integration
│   └── metaprompts.py      # Meta-level instructions for RAG
├── evaluation/
│   └── evaluator.py        # Scoring and metric computation
└── visualization/
    └── charts.py           # Generation of performance graphs
```

---

## ⚙️ Setup & Installation

### Local Environment

1. Clone the repository and navigate to the project directory:
   ```bash
   cd AI_Project
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💬 Usage

The project provides a comprehensive CLI (`main.py`) for various operations:

### 1. Interactive Chat
Run a simulated chat session with age-specific parameters:
```bash
python main.py --mode chat --age 12 --prompt "what is depression"
```

### 2. Run Evaluations
Execute the evaluation suite across different system configurations:
```bash
python main.py --mode eval
```

### 3. Generate Visualizations
Create charts comparing system performances:
```bash
python main.py --mode charts --demo
```

---

## 🌐 API Endpoints (Cloud Run)

The application is deployed on Google Cloud Run and exposed via a REST API.

**Base URL:**  
`https://ai-project-b5dl-d5pfcfjqf-aniyastiks-projects.vercel.app/`

### Endpoints

- **Health Check**
  - `GET /health`
  - Returns the operational status of the API.

- **Chat Interaction**
  - `POST /chat`
  - **Body Example:**
    ```json
    {
      "prompt": "what is depression",
      "age": 12,
      "system": "Proposed"
    }
    ```

- **Run Remote Evaluation**
  - `POST /evaluate`

---

## 🧪 Systems Compared

The evaluation engine tests our **Proposed** architecture against standard approaches:

1. **Baseline**: Standard LLM (No RAG, No Guardrails). Prone to hallucinations and unsafe content.
2. **RAG Only**: Grounded in facts but lacks safety filtering for sensitive topics.
3. **Guardrails Only**: Safe and filtered but not factually grounded (can still hallucinate safe responses).
4. **Proposed (Full System)**: Combines RAG and Guardrails for optimal performance.

---

## 📊 Evaluation Metrics & Results

The system is evaluated on four key pillars:
- **Safety**: Prevention of harmful content.
- **Accuracy**: Factual correctness of the response.
- **Hallucination Resistance**: Ability to avoid making up facts.
- **Age Alignment**: Appropriateness of the language and concepts for the target age.

### Results Summary

| System | Safety Score | Accuracy Score |
| :--- | :---: | :---: |
| **Baseline** | 0.60 | 0.00 |
| **RAG Only** | 1.00 | 0.72 |
| **Guardrails Only** | 1.00 | 1.00 |
| **Proposed (Full System)** | **0.98** | **0.98** |



---

## 🚀 Deployment
- **Frontend**: Deployed on **Vercel**
- **Infrastructure**: Google Cloud Run
- **Pipeline**: GitHub CI/CD

---

## 👥 Authors

*Aniya Baghirova, Shehana Byramli, Parviz Bayramli*
