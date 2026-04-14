"""
simulator.py
API-free response simulator for the Walled Garden project.
Generates deterministic responses for Baseline, RAG, Guardrails, and Proposed.
"""

from rag.database import find_relevant_topic, retrieve_chunk


def _age_style(user_age: int, text: str) -> str:
    """Adjust style very simply by age."""
    if user_age <= 8:
        return text[:220]
    if user_age <= 12:
        return text[:400]
    return text


def simulate_response(system: str, prompt: str, user_age: int, context: str = "") -> str:
    p = prompt.lower()

    adversarial_keywords = [
        "hack", "bypass", "break into", "cheat", "spy", "exploit",
        "ignore rules", "disable your safety", "fake being someone else",
        "get away with", "trick people", "no restrictions"
    ]
    risky_keywords = [
        "depression", "sad", "anxious", "anxiety", "alcohol", "drugs",
        "fight", "angry", "relationship", "break up", "smoke", "addicted"
    ]

    is_adversarial = any(k in p for k in adversarial_keywords)
    is_risky = any(k in p for k in risky_keywords)

    baseline_bad = (
        "Here’s how you could do that. First, find a target, then look for a weak password "
        "or a way to bypass the system. You can also trick people into giving information."
    )

    generic_safe = (
        "That is an important question. It can help to learn carefully, stay safe, and talk "
        "to a trusted adult, parent, or school counselor if something feels serious."
    )

    if system == "Baseline":
        if is_adversarial:
            return baseline_bad
        if "depression" in p:
            return "Depression is when someone feels very sad for a long time and it can affect daily life."
        return "Here is a general answer to your question."

    if system == "RAG":
        if not context:
            return "I am not able to answer that question. Please speak with a trusted adult."
        if is_adversarial:
            return "I cannot help with that. Please speak with a trusted adult."
        return context

    if system == "Guardrails":
        if is_adversarial:
            return "I’m always here to be helpful and safe, and I can’t help with that."
        if "depression" in p:
            if user_age <= 8:
                return "Sometimes a person can feel very sad for a long time. That means they need care and support from a grown-up they trust."
            if user_age <= 12:
                return "Depression is when someone feels very sad, low, or tired for a long time, and it can make everyday things feel hard. Talking to a trusted adult or counselor is a very good step."
            return "Depression is a mental health condition that can affect feelings, energy, sleep, and daily life. Support from a trusted adult, counselor, or doctor can really help."
        return _age_style(user_age, generic_safe)

    if system == "Proposed":
        if is_adversarial:
            return "I’m always here to be helpful and safe — that’s just who I am, and I can’t help with that! Is there something else I can help you with today?"
        if not context:
            return "That’s a great question! I don’t have information on that right now. I’d suggest asking a parent, teacher, or trusted adult — they’ll be able to help you best."
        return _age_style(user_age, context)

    raise ValueError(f"Unknown system: {system}")