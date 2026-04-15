"""
Phase 2 — Walled Garden RAG Database
Age-tiered educational content chunks for the core topics used by the benchmark.

Tiers:
- tier1: ages 5–10
- tier2: ages 11–17
- tier3: ages 18+

The database supports:
- General Knowledge
- Space
- Biology
- Math & Study
- History
- Mental Health
- Substances
- Conflict
- Relationships
- Online Safety
"""
import re

RAG_DATABASE = {
    "General Knowledge": {
        "tier1": (
            "General knowledge means learning simple facts about the world around us. "
            "It includes things from school, nature, science, and everyday life. "
            "Learning step by step helps children understand big ideas in an easy way."
        ),
        "tier2": (
            "General knowledge includes science, mathematics, history, and how everyday systems work. "
            "Clear explanations help students build understanding, curiosity, and problem-solving skills."
        ),
        "tier3": (
            "General knowledge covers a wide range of foundational topics such as science, mathematics, history, and technology. "
            "It supports broader reasoning, literacy, and analytical thinking."
        ),
    },

    "Space": {
        "tier1": (
            "Space is the huge area beyond Earth where planets, stars, and the Moon are found. "
            "The sky looks blue in the daytime because sunlight spreads out in the air. "
            "Black holes are places in space where gravity is so strong that even light cannot escape."
        ),
        "tier2": (
            "Space includes planets, stars, galaxies, and other objects beyond Earth. "
            "The sky appears blue because shorter blue wavelengths of sunlight scatter more in Earth's atmosphere. "
            "Black holes are regions where gravity is extremely strong, usually formed after very massive stars collapse."
        ),
        "tier3": (
            "Space includes stars, planets, galaxies, and extreme objects such as black holes. "
            "The blue appearance of the sky is explained by atmospheric scattering of shorter wavelengths of visible light. "
            "Black holes are compact regions of spacetime where gravity is strong enough to prevent light from escaping."
        ),
    },

    "Biology": {
        "tier1": (
            "Plants grow using sunlight, water, air, and nutrients from the soil. "
            "Dinosaurs ate different things: some ate plants and some ate meat. "
            "DNA is like a body instruction book, and RNA helps use those instructions."
        ),
        "tier2": (
            "Plants grow by using sunlight, water, carbon dioxide, and minerals, and they make food through photosynthesis. "
            "Dinosaurs had different diets depending on the species, with some being herbivores and others carnivores. "
            "DNA stores genetic information, while RNA helps use and carry that information in cells."
        ),
        "tier3": (
            "Plants grow through biological processes supported by light, water, carbon dioxide, and mineral uptake, including photosynthesis. "
            "Dinosaurs occupied different ecological roles, with herbivorous and carnivorous dietary patterns. "
            "DNA functions as the long-term storage molecule for genetic information, while RNA plays roles in expression and translation of that information."
        ),
    },

    "Math & Study": {
        "tier1": (
            "Math helps us solve number problems step by step. "
            "Twelve times four equals forty-eight. "
            "Good study habits include practicing, taking breaks, and asking for help when needed."
        ),
        "tier2": (
            "Mathematics works best when problems are broken into clear steps. "
            "For example, 12 × 4 = 48. "
            "Effective study habits include regular review, practice, time planning, and active recall."
        ),
        "tier3": (
            "Mathematics relies on clear reasoning and stepwise problem solving. "
            "For example, 12 multiplied by 4 equals 48. "
            "Strong study strategies include spaced repetition, practice testing, note review, and time management."
        ),
    },

    "History": {
        "tier1": (
            "Wars happen when countries or groups have very serious disagreements. "
            "World War 2 was a very large war involving many countries. "
            "It caused great harm and is remembered as an important event in history."
        ),
        "tier2": (
            "Wars often happen because of conflicts over power, land, resources, ideology, or long-standing tensions. "
            "World War 2 was a global conflict from 1939 to 1945 involving many nations, with devastating human and political consequences."
        ),
        "tier3": (
            "Wars emerge from complex political, economic, territorial, and ideological tensions. "
            "World War 2 was a global conflict fought between 1939 and 1945, resulting in mass destruction, genocide, and major geopolitical change."
        ),
    },

    "Technology & Internet": {
        "tier1": (
            "The internet helps computers share information with each other. "
            "It works by sending messages from one place to another very quickly. "
            "Being safe online means keeping personal information private."
        ),
        "tier2": (
            "The internet works by connecting devices through networks that send data in small packets. "
            "Routers, servers, and communication rules called protocols help information travel from one place to another."
        ),
        "tier3": (
            "The internet is a global network of networks that transmits data through packet switching and shared protocols such as TCP/IP. "
            "Devices communicate through servers, routers, and domain systems that help locate and deliver information efficiently."
        ),
    },

    "Mental Health": {
        "tier1": (
            "Sometimes people feel very sad or worried for a long time, and that is okay to talk about. "
            "Just like our bodies can feel sick, our feelings can feel unwell too, and a trusted adult like a parent or doctor can help. "
            "It is always brave and good to share your feelings with someone you trust."
        ),
        "tier2": (
            "Mental health refers to how we think, feel, and manage emotions in everyday life. "
            "Conditions like anxiety and depression are common and are recognized medical experiences, not signs of weakness. "
            "If someone feels persistently sad, overwhelmed, or hopeless, reaching out to a trusted adult, counselor, or doctor is an important first step."
        ),
        "tier3": (
            "Mental health includes emotional, psychological, and social wellbeing. "
            "Conditions such as depression and anxiety can affect mood, sleep, concentration, relationships, and daily functioning. "
            "Adults experiencing persistent symptoms may benefit from support from a licensed mental health professional."
        ),
    },

    "Substances": {
        "tier1": (
            "Some things like alcohol, cigarettes, and drugs can hurt the body and brain, especially for children. "
            "If anyone offers you something unsafe, the best choice is to say no and tell a trusted adult right away."
        ),
        "tier2": (
            "Substances like alcohol, tobacco, and drugs change how the brain and body work and can carry serious health risks, especially for young people. "
            "Addiction can happen when someone becomes dependent on a substance and finds it difficult to stop."
        ),
        "tier3": (
            "Substances such as alcohol, tobacco, and drugs affect the brain and body in different ways, and repeated use can lead to dependence or addiction. "
            "Substance use can have serious short-term and long-term physical, psychological, and social consequences."
        ),
    },

    "Conflict": {
        "tier1": (
            "Sometimes people disagree or feel angry, and that is a normal part of life. "
            "When things feel unsafe, the best thing to do is move away calmly and tell a grown-up you trust. "
            "Using calm words and listening can solve many problems."
        ),
        "tier2": (
            "Conflict between people or groups can happen because of differences in needs, values, feelings, or goals. "
            "Healthy conflict resolution includes staying calm, listening carefully, speaking respectfully, and getting help if things feel unsafe."
        ),
        "tier3": (
            "Conflict is a normal part of personal and social life, but healthy conflict management depends on communication, emotional regulation, and boundary-setting. "
            "If conflict becomes threatening or unsafe, involving appropriate support may be necessary."
        ),
    },

    "Relationships": {
        "tier1": (
            "Relationships are the connections we have with family, friends, and people we care about. "
            "Good relationships are built on kindness, honesty, and respect. "
            "If a relationship ever makes you feel unsafe or unhappy, talking to a trusted adult can help."
        ),
        "tier2": (
            "Healthy relationships are built on trust, respect, communication, and boundaries. "
            "Strong feelings like happiness, jealousy, sadness, or heartbreak can happen in relationships, and learning to talk about them respectfully is important."
        ),
        "tier3": (
            "Healthy relationships depend on mutual respect, honest communication, trust, and clear boundaries. "
            "Adults may face relationship challenges involving conflict, attachment, or emotional wellbeing, and healthy responses require reflection, communication, and respect for autonomy."
        ),
    },

    "Online Safety": {
        "tier1": (
            "The internet can be fun and useful, but children should be careful online. "
            "Never share your name, address, school, or photos with strangers, and tell a trusted adult if something online feels scary or wrong."
        ),
        "tier2": (
            "Online safety means protecting your personal information, privacy, and wellbeing when using apps, games, and social media. "
            "Scams, bullying, manipulation, and unsafe contact can happen online, so it is important to protect passwords and report harmful behavior."
        ),
        "tier3": (
            "Online safety includes protecting privacy, accounts, finances, devices, and personal wellbeing in digital environments. "
            "Risks include scams, phishing, identity theft, manipulation, harassment, and misinformation, and good practices include strong passwords and careful verification."
        ),
    },
}


def retrieve_chunk(topic: str, user_age: int) -> str:
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
    prompt_lower = prompt.lower()

    keyword_map = {
        "Mental Health": [
            "sad", "depress", "anxious", "anxiety", "mental", "emotion",
            "feel", "hopeless", "worried", "lonely",
        ],
        "Substances": [
            "alcohol", "drink", "drug", "drugs", "smoke", "cigarette",
            "vape", "addict", "substance", "weed", "beer", "wine", "pill",
        ],
        "Conflict": [
            "fight", "war", "hurt", "violence", "conflict", "argue",
            "bully", "hit", "punch", "attack", "weapon", "angry",
        ],
        "Relationships": [
            "relationship", "boyfriend", "girlfriend", "love", "breakup",
            "heartbreak", "secret", "friend", "trust", "date",
        ],
        "Online Safety": [
            "hack", "account", "wifi", "bypass", "filter", "spy", "trick",
            "fake", "cheat", "password",
        ],
        "Technology & Internet": [
            "internet", "online", "app", "apps",
        ],
        "Space": [
            "sky", "black hole", "space",
        ],
        "Biology": [
            "dinosaur", "plants", "plant", "photosynthesis", "dna", "rna",
        ],
        "Math & Study": [
            "12 times 4", "study", "exam", "spell elephant", "paper airplane", "gravity",
        ],
        "History": [
            "world war 2", "wars",
        ],
    }

    scores = {topic: 0 for topic in keyword_map}
    for topic, keywords in keyword_map.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', prompt_lower):
                scores[topic] += 1

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "General Knowledge"