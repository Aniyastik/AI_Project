"""
simulator.py
API-free response simulator for the Walled Garden project.
Generates deterministic responses for Baseline, RAG, Guardrails, and Proposed.
"""


def _age_band(user_age: int) -> str:
    if user_age <= 8:
        return "child"
    if user_age <= 17:
        return "minor"
    return "adult"


def _minor_fallback() -> str:
    return (
        "That is an important question. It can help to learn carefully, stay safe, "
        "and talk to a trusted adult, parent, or school counselor if something feels serious."
    )


def _adult_fallback() -> str:
    return (
        "That is an important question. It can help to approach it carefully, use reliable information, "
        "and seek professional support when the topic is serious."
    )


def simulate_response(system: str, prompt: str, user_age: int, context: str = "") -> str:
    p = prompt.lower().strip()
    age_band = _age_band(user_age)

    adversarial_keywords = [
        "hack", "bypass", "break into", "cheat", "spy", "exploit",
        "ignore rules", "disable your safety", "fake being someone else",
        "get away with", "trick people", "no restrictions"
    ]
    is_adversarial = any(k in p for k in adversarial_keywords)

    # Topic flags
    is_depression = "depression" in p or "depress" in p
    is_anxiety = "anxious" in p or "anxiety" in p or "worried" in p
    is_drug = "drug" in p or "drugs" in p
    is_alcohol = "alcohol" in p or "drink" in p or "beer" in p or "wine" in p
    is_smoking = "smoke" in p or "cigarette" in p or "vape" in p
    is_substance = is_drug or is_alcohol or is_smoking
    is_relationship = (
        "relationship" in p or "boyfriend" in p or "girlfriend" in p or
        "love" in p or "breakup" in p or "heartbroken" in p or "friend" in p
    )
    is_conflict = (
        "fight" in p or "war" in p or "hurt" in p or "angry" in p or
        "violence" in p or "conflict" in p
    )
    is_online = (
        "internet" in p or "online" in p or "wifi" in p or "account" in p or
        "password" in p or "app" in p or "hack"
    )

    # BASELINE
    if system == "Baseline":
        if is_adversarial:
            return (
                "Here’s how you could do that. First, find a target, then look for a weak password "
                "or a way to bypass the system. You can also trick people into giving information."
            )

        if is_depression:
            if age_band == "adult":
                return "Depression is a mental health condition that can affect mood, motivation, sleep, and daily functioning."
            return "Depression is when someone feels very sad for a long time and it can affect daily life."

        if is_anxiety:
            return "Anxiety is when someone feels very worried or nervous."

        if is_substance:
            return "Drugs are substances that can affect the body and mind. Some can be harmful."

        if is_relationship:
            return "Relationships are connections between people and they can involve emotions and trust."

        if is_conflict:
            return "Conflicts happen when people disagree, and they can sometimes become harmful."

        if is_online:
            return "The internet can be useful, but people should be careful online."

        return "Here is a general answer to your question."

    # GUARDRAILS
    if system == "Guardrails":
        if is_adversarial:
            return "I’m always here to be helpful and safe, and I can’t help with that."

        if is_depression:
            if age_band == "child":
                return (
                    "Sometimes a person can feel very sad for a long time. "
                    "That means they may need care and support from a grown-up they trust."
                )
            if age_band == "minor":
                return (
                    "Depression is when someone feels very sad, low, or tired for a long time, "
                    "and it can make everyday things feel hard. Talking to a trusted adult or counselor is a very good step."
                )
            return (
                "Depression is a mental health condition that can affect mood, energy, sleep, "
                "and daily functioning. Professional support can help."
            )

        if is_anxiety:
            if age_band == "child":
                return (
                    "Anxiety means feeling very worried or scared, even when it is hard to explain why. "
                    "Talking to a grown-up you trust can help."
                )
            if age_band == "minor":
                return (
                    "Anxiety means feeling worried, nervous, or overwhelmed in a way that can make everyday life harder. "
                    "Talking to a trusted adult or counselor can really help."
                )
            return (
                "Anxiety can involve persistent worry, tension, or fear that interferes with daily life. "
                "Support from a professional can be helpful."
            )

        if is_substance:
            if age_band == "child":
                return (
                    "Some things like drugs, cigarettes, and alcohol can hurt the body. "
                    "If someone offers them to you, say no and tell a trusted adult."
                )
            if age_band == "minor":
                return (
                    "Drugs are substances that can change how the brain and body work, and they can be harmful, "
                    "especially for young people. If you feel pressured to try them, talk to a trusted adult or counselor."
                )
            return (
                "Drugs are substances that can affect the brain and body in different ways. "
                "Some carry serious health risks, and problematic use may require medical or counseling support."
            )

        if is_relationship:
            if age_band == "child":
                return (
                    "Good relationships should feel kind, safe, and respectful. "
                    "If someone makes you feel bad or unsafe, tell a trusted adult."
                )
            if age_band == "minor":
                return (
                    "Healthy relationships are built on respect, trust, and clear boundaries. "
                    "If someone pressures you or makes you feel unsafe, talking to a trusted adult is a smart step."
                )
            return (
                "Healthy relationships depend on respect, communication, trust, and boundaries. "
                "If a relationship feels unsafe or controlling, it may help to seek support."
            )

        if is_conflict:
            if age_band == "child":
                return (
                    "Sometimes people get angry or disagree. It is best to stay calm, move away from unsafe situations, "
                    "and tell a grown-up you trust."
                )
            if age_band == "minor":
                return (
                    "Conflict happens when people strongly disagree. Staying calm, walking away from unsafe situations, "
                    "and speaking to a trusted adult can help."
                )
            return (
                "Conflict is a normal part of life, but it should be handled safely and respectfully. "
                "If it becomes threatening, involving support may be necessary."
            )

        if is_online:
            if age_band == "child":
                return (
                    "It is important to stay safe online and never share private information with strangers. "
                    "Tell a trusted adult if something online feels scary or wrong."
                )
            if age_band == "minor":
                return (
                    "Online safety means protecting your privacy, avoiding scams, and being careful with who you trust online. "
                    "If something feels wrong, report it and talk to a trusted adult."
                )
            return (
                "Online safety involves protecting your privacy, accounts, and personal information. "
                "Using strong passwords and staying alert to scams are important."
            )

        return _adult_fallback() if age_band == "adult" else _minor_fallback()

    # RAG
    if system == "RAG":
        if is_adversarial:
            if age_band == "adult":
                return "I cannot help with that request."
            return "I cannot help with that. Please speak with a trusted adult."

        if not context:
            if age_band == "adult":
                return "I do not have enough information in my current knowledge base to answer that question."
            return "I am not able to answer that question. Please speak with a trusted adult."

        return context

    # PROPOSED
    if system == "Proposed":
        if is_adversarial:
            return (
                "I’m always here to be helpful and safe — that’s just who I am, "
                "and I can’t help with that! Is there something else I can help you with today?"
            )

        if not context:
            if age_band == "adult":
                return "That’s a great question. I don’t have information on that topic in my current knowledge base."
            return (
                "That’s a great question! I don’t have information on that right now. "
                "I’d suggest asking a parent, teacher, or trusted adult — they’ll be able to help you best."
            )

        if is_depression:
            if age_band == "child":
                return (
                    "Sometimes people can feel very sad for a long time, and that means they may need help and care. "
                    "Talking to a grown-up you trust is a brave and good first step."
                )
            if age_band == "minor":
                return (
                    "Depression is a mental health condition that can make someone feel very sad, tired, or hopeless for a long time. "
                    "Support from a trusted adult, counselor, or doctor can really help."
                )
            return (
                "Depression is a mental health condition that can affect mood, sleep, energy, concentration, "
                "and daily functioning. Adults experiencing persistent symptoms may benefit from support from a licensed mental health professional."
            )

        if is_anxiety:
            if age_band == "child":
                return (
                    "Anxiety means feeling very worried or scared, even when it is hard to explain why. "
                    "Talking to a grown-up you trust can help you feel safer."
                )
            if age_band == "minor":
                return (
                    "Anxiety can make someone feel worried, nervous, or overwhelmed for a long time. "
                    "Support from a trusted adult or counselor can help you handle those feelings."
                )
            return (
                "Anxiety can involve persistent worry, tension, or fear that affects concentration, sleep, "
                "and everyday functioning. Adults may benefit from professional mental health support."
            )

        if is_substance:
            if age_band == "child":
                return (
                    "Some things like drugs, cigarettes, and alcohol can hurt your body and brain. "
                    "If you ever see them or someone offers them to you, it is safest to say no and tell a trusted adult."
                )
            if age_band == "minor":
                return (
                    "Drugs are substances that can affect the brain and body, and repeated use can sometimes lead to dependence or addiction. "
                    "They can have serious health effects, so if you feel pressured around them, talking to a trusted adult or counselor is a smart step."
                )
            return (
                "Substances such as alcohol, tobacco, and drugs affect the brain and body in different ways, "
                "and repeated use can lead to dependence or addiction. Substance use can have serious short-term and long-term health, social, "
                "and psychological effects. Adults concerned about substance use may benefit from medical advice, counseling, or addiction support services."
            )

        if is_relationship:
            if age_band == "child":
                return (
                    "Good relationships should feel kind, safe, and respectful. "
                    "If someone makes you feel scared or upset a lot, telling a trusted adult can help."
                )
            if age_band == "minor":
                return (
                    "Healthy relationships are built on trust, respect, communication, and boundaries. "
                    "If someone pressures you or makes you feel unsafe, talking to a trusted adult is a wise step."
                )
            return (
                "Healthy relationships depend on respect, honest communication, trust, and clear boundaries. "
                "Relationships that involve pressure, fear, or control may require reflection and outside support."
            )

        if is_conflict:
            if age_band == "child":
                return (
                    "Sometimes people argue or get angry, but it is important to stay safe and calm. "
                    "Walking away from unsafe situations and telling a grown-up is a good choice."
                )
            if age_band == "minor":
                return (
                    "Conflict happens when people strongly disagree, but it should be handled safely and respectfully. "
                    "If it becomes threatening, getting support from a trusted adult is important."
                )
            return (
                "Conflict is a normal part of life, but healthy conflict management depends on communication, calm responses, "
                "and safety. If a situation becomes threatening, outside support may be necessary."
            )

        if is_online:
            if age_band == "child":
                return (
                    "Staying safe online means not sharing private things with strangers and telling a trusted adult if something feels scary or wrong."
                )
            if age_band == "minor":
                return (
                    "Online safety means protecting your privacy, being careful with strangers, and knowing how to report harmful behavior or scams."
                )
            return (
                "Online safety includes protecting your privacy, accounts, and personal information, while staying alert to scams, manipulation, and identity theft."
            )

        if age_band == "child":
            return context[:260]
        if age_band == "minor":
            return context[:420]
        return context

    raise ValueError(f"Unknown system: {system}")