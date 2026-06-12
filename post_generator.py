from llm_helper import llm


def get_length_instruction(length):
    length_map = {
        "Short": "Write 5 to 7 lines only.",
        "Medium": "Write 10 to 14 lines.",
        "Long": "Write 16 to 22 lines with strong storytelling."
    }
    return length_map.get(length, "Write 10 to 14 lines.")


def generate_linkedin_post(
    topic,
    post_type,
    tone,
    audience,
    length,
    language,
    extra_details,
    include_hashtags=True,
    include_emojis=True,
    include_cta=True
):
    length_instruction = get_length_instruction(length)

    hashtag_instruction = (
        "Add 8 to 12 relevant LinkedIn hashtags at the end."
        if include_hashtags else
        "Do not add hashtags."
    )

    emoji_instruction = (
        "Use professional emojis where suitable, but do not overuse them."
        if include_emojis else
        "Do not use emojis."
    )

    cta_instruction = (
        "End with a clear call-to-action question for engagement."
        if include_cta else
        "Do not add a call-to-action."
    )

    prompt = f"""
You are an expert LinkedIn content writer.

Create a high-quality LinkedIn post using the details below.

Topic:
{topic}

Post Type:
{post_type}

Tone:
{tone}

Target Audience:
{audience}

Length:
{length_instruction}

Language:
{language}
If language is Hinglish, use English script only.

Extra Details:
{extra_details}

Rules:
1. Make the post professional and human-like.
2. Start with a strong hook.
3. Use short paragraphs.
4. Avoid fake claims.
5. Avoid over-promising.
6. Make it useful for students, job seekers, or professionals.
7. {hashtag_instruction}
8. {emoji_instruction}
9. {cta_instruction}

Return only the final LinkedIn post.
"""

    response = llm.invoke(prompt)
    return response.content


def improve_post(existing_post, improvement_style):
    prompt = f"""
You are a LinkedIn personal branding expert.

Improve the LinkedIn post below.

Improvement Style:
{improvement_style}

Original Post:
{existing_post}

Rules:
1. Keep the meaning same.
2. Improve clarity, hook, structure, and engagement.
3. Make it professional and natural.
4. Add better formatting.
5. Return only the improved post.
"""

    response = llm.invoke(prompt)
    return response.content


def generate_hashtags(topic, post_type, audience):
    prompt = f"""
Generate 15 relevant LinkedIn hashtags for this content.

Topic: {topic}
Post Type: {post_type}
Target Audience: {audience}

Rules:
1. Include a mix of broad and niche hashtags.
2. Return only hashtags.
3. Do not explain.
"""

    response = llm.invoke(prompt)
    return response.content


def generate_carousel_content(topic, post_type, audience):
    prompt = f"""
Create LinkedIn carousel content for the topic below.

Topic:
{topic}

Post Type:
{post_type}

Target Audience:
{audience}

Create 6 carousel slides.

Format:
Slide 1: Title
Slide 2: Problem
Slide 3: Key Insight
Slide 4: Solution / Framework
Slide 5: Example / Application
Slide 6: Final Takeaway + CTA

Rules:
1. Keep each slide short.
2. Make it beginner-friendly.
3. Use professional wording.
4. Return only carousel slide content.
"""

    response = llm.invoke(prompt)
    return response.content


def score_post(post):
    prompt = f"""
You are a LinkedIn content evaluator.

Score the LinkedIn post below out of 100.

Post:
{post}

Evaluate:
1. Hook strength
2. Clarity
3. Professional tone
4. Engagement potential
5. Hashtag quality
6. Call-to-action
7. Readability

Return in this format only:

Overall Score: __/100

Breakdown:
- Hook:
- Clarity:
- Professional Tone:
- Engagement:
- Hashtags:
- CTA:
- Readability:

Suggestions:
1.
2.
3.
"""

    response = llm.invoke(prompt)
    return response.content
