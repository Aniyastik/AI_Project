"""
Phase 2 — Walled Garden RAG Database
Age-tiered educational content chunks for the 5 core sensitive topics.
Each topic has a Tier 1 (ages 5-10), Tier 2 (ages 11-17), and Tier 3 (ages 18+) chunk.
These are the ONLY chunks the RAG system is allowed to retrieve and surface.
"""

RAG_DATABASE = {
    "Mental Health": {
        "tier1": (
            "Sometimes people feel very sad or worried for a long time, and that is okay to talk about. "
            "Just like our bodies can feel sick, our feelings can feel unwell too, and a trusted adult like a parent "
            "or doctor can always help us feel better. It is always brave and good to share your feelings with someone you trust."
        ),
        "tier2": (
            "Mental health refers to how we think, feel, and manage emotions in everyday life. "
            "Conditions like anxiety and depression are common and are recognized medical experiences, "
            "not signs of weakness, and effective support is available through trusted adults, counselors, or doctors. "
            "If you or someone you know feels persistently sad, overwhelmed, or hopeless, reaching out to a trusted adult "
            "or school counselor is always the right first step."
        ),
        "tier3": (
            "Mental health includes emotional, psychological, and social wellbeing. Conditions such as depression and anxiety "
            "can affect mood, sleep, concentration, relationships, and daily functioning. Adults experiencing persistent symptoms "
            "may benefit from support from a licensed mental health professional."
        ),
    },
    "Substances": {
        "tier1": (
            "Some things like medicines, alcohol, and cigarettes are only for grown-ups and can make children very sick. "
            "If anyone ever offers you something to eat, drink, or smell that is not food, always say no and tell a trusted adult right away. "
            "Your body is important and keeping it safe is always the right choice."
        ),
        "tier2": (
            "Substances like alcohol, tobacco, and drugs are chemicals that change how the brain and body work, "
            "and they carry serious health risks especially for developing brains in people under 18. "
            "Addiction can happen when the brain becomes dependent on a substance, making it very hard to stop even when someone wants to. "
            "If you ever feel pressured to try any substance, talking to a trusted adult, school counselor, or calling a helpline "
            "is always a safe and confidential option."
        ),
        "tier3": (
            "Substances such as alcohol, tobacco, and drugs affect the brain and body in different ways, and repeated use can lead to dependence "
            "or addiction. Substance use can have serious short-term and long-term health, social, and psychological effects. Adults concerned "
            "about substance use may benefit from medical advice, counseling, or addiction support services."
        ),
    },
    "Conflict": {
        "tier1": (
            "Sometimes people disagree or feel angry, and that is a normal part of life. "
            "When things feel unsafe or someone is being unkind, the best thing to do is walk away calmly and tell a grown-up you trust. "
            "Using kind words and listening to each other can solve most problems peacefully."
        ),
        "tier2": (
            "Conflict between people or groups often arises from differences in needs, values, or resources, "
            "and is a normal part of human relationships when managed constructively. "
            "Healthy conflict resolution involves active listening, expressing feelings calmly, and seeking compromise "
            "rather than using aggression or intimidation. "
            "If a conflict ever feels threatening or physically unsafe, removing yourself from the situation and "
            "informing a trusted adult or authority figure is always the right course of action."
        ),
        "tier3": (
            "Conflict is a normal part of personal and social life, but constructive conflict management depends on communication, emotional regulation, "
            "and boundary-setting. Healthy approaches include listening actively, expressing concerns clearly, and seeking de-escalation or mediation "
            "when needed. If a conflict becomes threatening or unsafe, involving appropriate support or authorities may be necessary."
        ),
    },
    "Relationships": {
        "tier1": (
            "Relationships are the special connections we have with family, friends, and people we care about. "
            "Good relationships are built on kindness, honesty, and treating each other with respect. "
            "If anyone in a relationship ever makes you feel unsafe or unhappy, it is always okay to talk to a parent or trusted adult."
        ),
        "tier2": (
            "Healthy relationships — whether friendships or romantic ones — are built on mutual respect, "
            "honest communication, and the freedom to set personal boundaries. "
            "It is normal for relationships to involve strong emotions including happiness, jealousy, or sadness, "
            "and learning to communicate feelings clearly and respectfully is an important life skill. "
            "Any relationship where someone pressures you, makes you feel unsafe, or asks you to keep secrets from "
            "your parents or guardians should be discussed with a trusted adult immediately."
        ),
        "tier3": (
            "Healthy relationships are built on mutual respect, honest communication, trust, and clear personal boundaries. "
            "Adults may face relationship challenges involving attachment, conflict, commitment, or emotional wellbeing, and addressing them constructively "
            "requires communication, reflection, and respect for consent and autonomy. Relationships that involve pressure, fear, or control are unhealthy and may require support."
        ),
    },
    "Online Safety": {
        "tier1": (
            "The internet is like a big city — most of it is wonderful, but just like in real life, "
            "there are some places and people children should stay away from. "
            "Never share your name, address, school, or photos with people you do not know online, "
            "and always tell a parent or trusted adult if something online makes you feel scared or uncomfortable. "
            "Your parents and guardians are always there to help you stay safe."
        ),
        "tier2": (
            "Online safety means protecting your personal information, your wellbeing, and your privacy "
            "when using the internet, apps, and social media. "
            "Sharing personal details, passwords, or images online can have serious and lasting consequences, "
            "and interactions with strangers online carry real risks even when they seem friendly. "
            "Cyberbullying, scams, and manipulation are real threats — if you ever encounter anything online "
            "that feels wrong, threatening, or inappropriate, screenshot it and report it to a trusted adult or "
            "use the platform's reporting tools immediately."
        ),
        "tier3": (
            "Online safety for adults includes protecting privacy, accounts, devices, finances, and personal wellbeing in digital environments. "
            "Risks include scams, phishing, identity theft, harassment, misinformation, and coercive or manipulative interactions. Good practices include "
            "using strong passwords, enabling multi-factor authentication, verifying sources, and reporting suspicious behavior through appropriate channels."
        ),
    },
}


def retrieve_chunk(topic: str, user_age: int) -> str:
    """
    Retrieve the age-appropriate RAG chunk for a given topic and user age.
    Returns empty string if topic is not in the database.
    """
    if topic not in RAG_DATABASE:
        return ""

    if user_age <= 10:
        tier = "tier1"
    elif user_age <= 17:
        tier = "tier2"
    else:
        tier = "tier3"

    return RAG_DATABASE[topic][tier]


def find_relevant_topic(prompt: str) -> str:
    """
    Simple keyword-based topic router.
    Returns the best matching topic key or empty string if no match.
    """
    prompt_lower = prompt.lower()
    keyword_map = {
        "Mental Health": [
            "sad", "depress", "anxious", "anxiety", "mental", "emotion",
            "feel", "angry", "anger", "worry", "hopeless", "lonely",
        ],
        "Substances": [
            "alcohol", "drink", "drug", "smoke", "cigarette", "addict",
            "substance", "weed", "beer", "wine", "pill",
        ],
        "Conflict": [
            "fight", "war", "hurt", "violence", "conflict", "argue",
            "bully", "hit", "punch", "attack", "weapon",
        ],
        "Relationships": [
            "relationship", "boyfriend", "girlfriend", "love", "breakup",
            "heartbreak", "secret", "friend", "trust", "date",
        ],
        "Online Safety": [
            "internet", "online", "hack", "account", "wifi", "bypass",
            "filter", "spy", "trick", "fake", "cheat", "password", "app",
        ],
    }
    scores = {topic: 0 for topic in keyword_map}
    for topic, keywords in keyword_map.items():
        for kw in keywords:
            if kw in prompt_lower:
                scores[topic] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else ""