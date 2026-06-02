from few_shot import FewShotPosts
from llm_helper import get_llm_response

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    elif length == "Medium":
        return "6 to 10 lines"
    elif length == "Long":
        return "11 to 15 lines"
    else:
        return "6 to 10 lines"


def generate_post(length, language, tag):
    prompt = f"""
Generate a LinkedIn post using the below information.

Topic: {tag}
Length: {get_length_str(length)}
Language: {language}

Rules:
1. Write like a student/professional learning and building projects.
2. Keep the tone simple, clear, and professional.
3. Add useful hashtags at the end.
4. Do not add extra explanations outside the post.
"""

    examples = few_shot.get_filtered_posts(length, language, tag)

    if examples:
        prompt += "\n\nUse these examples only for writing style:\n"
        for i, post in enumerate(examples[:2], start=1):
            prompt += f"\nExample {i}:\n{post.get('text', '')}\n"

    return get_llm_response(prompt)
