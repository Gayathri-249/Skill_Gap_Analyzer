
import re

SKILL_DICTIONARY = {
    "python": ["python"],
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "machine learning": ["machine learning", "scikit-learn", "sklearn"],
    "deep learning": ["deep learning"],
    "natural language processing": ["natural language processing", "nlp"],
    "generative ai": ["generative ai", "gen ai"],
    "large language models": ["large language models", "large language model", "llm", "llms"],
    "langchain": ["langchain"],
    "langgraph": ["langgraph"],
    "retrieval augmented generation": ["retrieval augmented generation", "rag"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization", "matplotlib", "seaborn", "tableau", "power bi"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "django": ["django"],
    "streamlit": ["streamlit"],
    "computer vision": ["computer vision", "opencv"],
    "git": ["git", "github"],
    "docker": ["docker"],
    "aws": ["aws", "amazon web services"],
    "azure": ["microsoft azure", "azure"],
    "html": ["html"],
    "css": ["css"],
    "javascript": ["javascript"],
    "java": ["java"],
    "c++": ["c++"],
    "excel": ["microsoft excel", "excel"],
    "statistics": ["statistics", "statistical analysis"],
    "data structures": ["data structures", "data structures and algorithms"],
    "transformers": ["transformers", "hugging face", "huggingface"],
    "vector databases": ["vector database", "vector databases", "chromadb", "pinecone", "faiss"],
    "api development": ["rest api", "restful api", "api development"]
}

LEARNING_RESOURCES = {
    "python": ("Python Tutorial", "https://docs.python.org/3/tutorial/"),
    "sql": ("SQLBolt", "https://sqlbolt.com/"),
    "machine learning": ("Scikit-learn Tutorials", "https://scikit-learn.org/stable/tutorial/"),
    "deep learning": ("DeepLearning.AI", "https://www.deeplearning.ai/"),
    "natural language processing": ("Hugging Face NLP Course", "https://huggingface.co/learn/nlp-course/"),
    "generative ai": ("Google Cloud Skills Boost", "https://www.cloudskillsboost.google/"),
    "large language models": ("Hugging Face Learn", "https://huggingface.co/learn"),
    "langchain": ("LangChain Documentation", "https://python.langchain.com/docs/"),
    "langgraph": ("LangGraph Documentation", "https://docs.langchain.com/oss/python/langgraph/overview"),
    "retrieval augmented generation": ("Hugging Face Learn", "https://huggingface.co/learn"),
    "tensorflow": ("TensorFlow Tutorials", "https://www.tensorflow.org/tutorials"),
    "pytorch": ("PyTorch Tutorials", "https://pytorch.org/tutorials/"),
    "pandas": ("Pandas Getting Started", "https://pandas.pydata.org/docs/getting_started/"),
    "numpy": ("NumPy Learn", "https://numpy.org/learn/"),
    "flask": ("Flask Documentation", "https://flask.palletsprojects.com/"),
    "fastapi": ("FastAPI Tutorial", "https://fastapi.tiangolo.com/tutorial/"),
    "streamlit": ("Streamlit Documentation", "https://docs.streamlit.io/"),
    "computer vision": ("OpenCV Documentation", "https://docs.opencv.org/"),
    "git": ("Pro Git Book", "https://git-scm.com/book/en/v2"),
    "docker": ("Docker Get Started", "https://docs.docker.com/get-started/"),
    "aws": ("AWS Skill Builder", "https://skillbuilder.aws/"),
    "azure": ("Microsoft Learn", "https://learn.microsoft.com/training/"),
    "javascript": ("MDN JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"),
    "java": ("Dev.java Learn", "https://dev.java/learn/"),
    "statistics": ("Khan Academy Statistics", "https://www.khanacademy.org/math/statistics-probability"),
    "transformers": ("Hugging Face Learn", "https://huggingface.co/learn"),
    "vector databases": ("Chroma Documentation", "https://docs.trychroma.com/"),
    "api development": ("FastAPI Tutorial", "https://fastapi.tiangolo.com/tutorial/")
}



def extract_skills(text):
    text = str(text or "").lower()
    found = set()

    for skill, aliases in SKILL_DICTIONARY.items():
        for alias in aliases:
            pattern = r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)"
            if re.search(pattern, text):
                found.add(skill)
                break

    # Normalize aliases to canonical skill names
    normalized = set()

    for skill in found:
        normalized.add(SKILL_ALIASES.get(skill, skill))

    return sorted(normalized)



def analyze_skill_gap(resume_text, job_description):
    user_skills = set(extract_skills(resume_text))
    required_skills = set(extract_skills(job_description))

    matched = sorted(user_skills & required_skills)
    missing = sorted(required_skills - user_skills)

    coverage = (
        round(len(matched) / len(required_skills) * 100, 2)
        if required_skills else 0.0
    )

    recommendations = []
    for skill in missing:
        resource_name, resource_url = LEARNING_RESOURCES.get(
            skill,
            ("Search learning resources", "https://www.coursera.org/")
        )
        recommendations.append({
            "skill": skill,
            "resource": resource_name,
            "url": resource_url
        })

    return {
        "user_skills": sorted(user_skills),
        "required_skills": sorted(required_skills),
        "matched_skills": matched,
        "missing_skills": missing,
        "coverage": coverage,
        "recommendations": recommendations
    }

def prioritized_recommendations(missing_skills):
    recommendations = []

    for skill in missing_skills:
        resource_name, resource_url = LEARNING_RESOURCES.get(
            skill,
            (
                "Search for learning resources",
                "https://www.coursera.org/"
            )
        )

        related = RELATED_SKILLS.get(skill, [])

        recommendations.append({
            "skill": skill,
            "priority": "High" if skill in {
                "python",
                "sql",
                "machine learning",
                "large language models",
                "retrieval augmented generation"
            } else "Medium",
            "resource": resource_name,
            "url": resource_url,
            "supporting_skills": related,
        })

    priority_order = {"High": 0, "Medium": 1}

    recommendations.sort(
        key=lambda item: (
            priority_order[item["priority"]],
            item["skill"]
        )
    )

    return recommendations


SKILL_ALIASES = {
    "python programming": "python",
    "scikit learn": "machine learning",
    "sklearn": "machine learning",
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "gen ai": "generative ai",
    "llm": "large language models",
    "llms": "large language models",
    "rag": "retrieval augmented generation",
    "hugging face": "transformers",
    "huggingface": "transformers",
    "chromadb": "vector databases",
    "pinecone": "vector databases",
    "faiss": "vector databases",
    "rest api": "api development",
    "restful api": "api development",
    "postgresql": "sql",
    "mysql": "sql",
}

RELATED_SKILLS = {
    "machine learning": ["python", "statistics", "scikit-learn"],
    "deep learning": ["machine learning", "python", "pytorch"],
    "natural language processing": ["python", "transformers"],
    "generative ai": ["large language models", "natural language processing"],
    "large language models": ["transformers", "generative ai"],
    "retrieval augmented generation": ["large language models", "vector databases"],
    "langchain": ["large language models", "retrieval augmented generation"],
    "langgraph": ["langchain", "large language models"],
    "vector databases": ["retrieval augmented generation"],
    "api development": ["python", "fastapi"],
    "computer vision": ["python", "deep learning"],
}
