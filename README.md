# 🛡️ Walled Garden — Age-Aware AI Safety System

A child-safe AI system that combines **Retrieval-Augmented Generation (RAG)** with **age-aware guardrails** to deliver safe, accurate, and developmentally appropriate responses for users aged **5–17**.

---

## 🚀 Overview

This project implements a **defense-in-depth architecture** for AI safety:

- 🔍 **RAG (Retrieval-Augmented Generation)** → grounded answers  
- 🧠 **Age-aware guardrails** → safe + appropriate responses  
- 🛡️ **Adversarial resistance** → blocks harmful prompts  
- 📊 **Evaluation engine** → measures safety & performance  

Unlike standard chatbots, this system ensures:
> **“Safe + Useful + Age-Appropriate” responses simultaneously**

---

## 🧱 Architecture

User prompt + age  
→ Topic Router → RAG Context → Guardrails + Logic → Safe Response

---

## 📁 Project Structure

AI_Project/
├── app.py  
├── main.py  
├── simulator.py  
├── requirements.txt  
├── README.md  
├── data/  
│   └── prompts.py  
├── rag/  
│   ├── database.py  
│   └── metaprompts.py  
├── evaluation/  
│   └── evaluator.py  
└── visualization/  
    └── charts.py  

---

## ⚙️ Setup (Local)

pip install -r requirements.txt

---

## 💬 Usage

Run Chat:
py main.py --mode chat --age 12 --prompt "what is depression"

Run Evaluation:
py main.py --mode eval

Generate Charts:
py main.py --mode charts --demo

---

## 🌐 API Endpoints (Cloud Run)

Base URL:
https://aiproject-250112486278.europe-west1.run.app

Health:
GET /health

Chat:
POST /chat

Example Body:
{
  "prompt": "what is depression",
  "age": 12,
  "system": "Proposed"
}

Evaluate:
POST /evaluate

---

## 🧪 Systems Compared

Baseline — No RAG, No Guardrails  
RAG — Grounded but not safe  
Guardrails — Safe but not grounded  
Proposed — Full system  

---

## 📊 Evaluation Metrics

- Safety  
- Accuracy  
- Hallucination Resistance  
- Age Alignment  

---

## 📈 Results Summary

Baseline: Safety 0.60 | Accuracy 0.00  
RAG: Safety 1.00 | Accuracy 0.72  
Guardrails: Safety 1.00 | Accuracy 1.00  
Proposed: Safety 0.98 | Accuracy 0.98  

---

## 🚀 Deployment

Google Cloud Run + GitHub CI/CD

---

## 👥 Authors
