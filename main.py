import streamlit as st
from post_generator import (
    generate_linkedin_post,
    improve_post,
    generate_hashtags,
    generate_carousel_content,
    score_post
)

st.set_page_config(
    page_title="AI LinkedIn Content Studio",
    page_icon="🚀",
    layout="wide"
)

CUSTOM_CSS = """
<style>
.main {
    background-color: #f8fafc;
}
.big-title {
    font-size: 42px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 5px;
}
.subtitle {
    font-size: 18px;
    color: #475569;
    margin-bottom: 25px;
}
.feature-card {
    background-color: white;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.06);
    margin-bottom: 15px;
}
.result-box {
    background-color: #ffffff;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #cbd5e1;
    box-shadow: 0px 4px 14px rgba(15, 23, 42, 0.08);
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def initialize_session_state():
    if "generated_post" not in st.session_state:
        st.session_state.generated_post = ""

    if "improved_post" not in st.session_state:
        st.session_state.improved_post = ""

    if "hashtags" not in st.session_state:
        st.session_state.hashtags = ""

    if "carousel" not in st.session_state:
        st.session_state.carousel = ""

    if "score" not in st.session_state:
        st.session_state.score = ""


def app_header():
    st.markdown('<div class="big-title">🚀 AI LinkedIn Content Studio</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Generate LinkedIn posts, improve content, create hashtags, score posts, and build carousel ideas using AI.</div>',
        unsafe_allow_html=True
    )


def sidebar_info():
    with st.sidebar:
        st.title("📌 About App")
        st.write(
            """
            This app helps students, job seekers, creators, and professionals create better LinkedIn content.
            """
        )

        st.markdown("---")

        st.subheader("✨ Features")
        st.write("✅ Custom topic input")
        st.write("✅ Ready-made topic options")
        st.write("✅ Tone-based generation")
        st.write("✅ Hashtag generator")
        st.write("✅ Post improvement")
        st.write("✅ LinkedIn post score")
        st.write("✅ Carousel content generator")

        st.markdown("---")

        st.subheader("👩‍💻 Built With")
        st.write("Python")
        st.write("Streamlit")
        st.write("LangChain")
        st.write("Groq LLM")


def get_topic_input():
    st.markdown("### 1️⃣ Choose Topic Input Method")

    input_method = st.radio(
        "How do you want to give the topic?",
        ["Select from ready-made topics", "Write my own topic"],
        horizontal=True
    )

    ready_topics = [
        "Internship Experience",
        "Project Showcase",
        "AI/ML Learning Journey",
        "Data Science Project",
        "Generative AI Project",
        "Streamlit App Launch",
        "Course Completion",
        "Certification Achievement",
        "Interview Preparation",
        "Job Search Update",
        "Resume Building Tips",
        "LinkedIn Personal Branding",
        "Python Learning Journey",
        "SQL Learning Journey",
        "Machine Learning Concept",
        "RAG / Agentic AI Concept",
        "College Achievement",
        "Hackathon Experience",
        "Motivational Career Post",
        "Daily Learning Update"
    ]

    if input_method == "Select from ready-made topics":
        topic = st.selectbox("Choose a topic", ready_topics)
    else:
        topic = st.text_area(
            "Write your own topic",
            placeholder="Example: I built a Multi-Agent AI Career Assistant using CrewAI, Groq, and Streamlit.",
            height=120
        )

    return topic


def get_generation_settings():
    st.markdown("### 2️⃣ Customize Your LinkedIn Post")

    col1, col2, col3 = st.columns(3)

    with col1:
        post_type = st.selectbox(
            "Post Type",
            [
                "Project Showcase",
                "Achievement Post",
                "Learning Journey",
                "Storytelling Post",
                "Technical Explanation",
                "Job Seeker Post",
                "Internship Update",
                "Course Completion",
                "Motivational Post",
                "Professional Announcement"
            ]
        )

    with col2:
        tone = st.selectbox(
            "Tone",
            [
                "Professional",
                "Friendly",
                "Motivational",
                "Storytelling",
                "Beginner-Friendly",
                "Recruiter-Attractive",
                "Confident",
                "Simple and Clear"
            ]
        )

    with col3:
        audience = st.selectbox(
            "Target Audience",
            [
                "Students",
                "Recruiters",
                "Data Science Professionals",
                "AI/ML Learners",
                "Job Seekers",
                "LinkedIn Network",
                "College Faculty",
                "Hiring Managers",
                "Beginners"
            ]
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        length = st.selectbox("Post Length", ["Short", "Medium", "Long"])

    with col5:
        language = st.selectbox("Language", ["English", "Hinglish"])

    with col6:
        st.write("Options")
        include_hashtags = st.checkbox("Add Hashtags", value=True)
        include_emojis = st.checkbox("Add Emojis", value=True)
        include_cta = st.checkbox("Add CTA", value=True)

    extra_details = st.text_area(
        "Add extra details",
        placeholder="Mention tools used, project link, GitHub link, what you learned, result, problem solved, etc.",
        height=130
    )

    return post_type, tone, audience, length, language, extra_details, include_hashtags, include_emojis, include_cta


def show_generated_post():
    if st.session_state.generated_post:
        st.markdown("### ✅ Generated LinkedIn Post")
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.write(st.session_state.generated_post)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            label="⬇️ Download Post as TXT",
            data=st.session_state.generated_post,
            file_name="linkedin_post.txt",
            mime="text/plain"
        )


def post_tools(topic, post_type, audience):
    if not st.session_state.generated_post:
        return

    st.markdown("---")
    st.markdown("### 3️⃣ Improve, Score, or Repurpose Your Post")

    tool_col1, tool_col2, tool_col3 = st.columns(3)

    with tool_col1:
        improvement_style = st.selectbox(
            "Improvement Style",
            [
                "Make it more professional",
                "Make it more engaging",
                "Make it shorter",
                "Make it more storytelling",
                "Make it recruiter-attractive",
                "Make it beginner-friendly"
            ]
        )

        if st.button("✨ Improve Post"):
            with st.spinner("Improving your post..."):
                st.session_state.improved_post = improve_post(
                    st.session_state.generated_post,
                    improvement_style
                )

    with tool_col2:
        if st.button("📊 Score Post"):
            with st.spinner("Scoring your post..."):
                st.session_state.score = score_post(st.session_state.generated_post)

    with tool_col3:
        if st.button("🏷️ Generate Hashtags"):
            with st.spinner("Generating hashtags..."):
                st.session_state.hashtags = generate_hashtags(topic, post_type, audience)

    if st.button("📑 Generate Carousel Content"):
        with st.spinner("Creating carousel content..."):
            st.session_state.carousel = generate_carousel_content(topic, post_type, audience)

    if st.session_state.improved_post:
        st.markdown("### ✨ Improved Post")
        st.write(st.session_state.improved_post)

        st.download_button(
            label="⬇️ Download Improved Post",
            data=st.session_state.improved_post,
            file_name="improved_linkedin_post.txt",
            mime="text/plain"
        )

    if st.session_state.score:
        st.markdown("### 📊 LinkedIn Post Score")
        st.write(st.session_state.score)

    if st.session_state.hashtags:
        st.markdown("### 🏷️ Suggested Hashtags")
        st.write(st.session_state.hashtags)

    if st.session_state.carousel:
        st.markdown("### 📑 LinkedIn Carousel Content")
        st.write(st.session_state.carousel)

        st.download_button(
            label="⬇️ Download Carousel Content",
            data=st.session_state.carousel,
            file_name="linkedin_carousel_content.txt",
            mime="text/plain"
        )


def main():
    initialize_session_state()
    sidebar_info()
    app_header()

    tab1, tab2, tab3 = st.tabs(
        [
            "✍️ Generate Post",
            "📌 How to Use",
            "🎯 Project Explanation"
        ]
    )

    with tab1:
        topic = get_topic_input()

        (
            post_type,
            tone,
            audience,
            length,
            language,
            extra_details,
            include_hashtags,
            include_emojis,
            include_cta
        ) = get_generation_settings()

        generate_btn = st.button("🚀 Generate LinkedIn Post", type="primary")

        if generate_btn:
            if not topic.strip():
                st.warning("Please enter or select a topic first.")
            else:
                with st.spinner("Generating your LinkedIn post..."):
                    st.session_state.generated_post = generate_linkedin_post(
                        topic=topic,
                        post_type=post_type,
                        tone=tone,
                        audience=audience,
                        length=length,
                        language=language,
                        extra_details=extra_details,
                        include_hashtags=include_hashtags,
                        include_emojis=include_emojis,
                        include_cta=include_cta
                    )

        show_generated_post()
        post_tools(topic, post_type, audience)

    with tab2:
        st.markdown("## How to Use This App")
        st.write(
            """
            1. Select a ready-made topic or write your own topic.
            2. Choose post type, tone, audience, length, and language.
            3. Add extra details like tools, project name, GitHub link, or live app link.
            4. Click Generate LinkedIn Post.
            5. Improve the post, generate hashtags, score the post, or create carousel content.
            """
        )

        st.markdown("## Example Custom Topic")
        st.code(
            "I built a Multi-Agent AI Career Assistant using CrewAI, Groq, LangChain, and Streamlit.",
            language="text"
        )

    with tab3:
        st.markdown("## Project Explanation")
        st.write(
            """
            This project is an AI-powered LinkedIn Content Studio built using Streamlit and Groq LLM.
            It helps users generate professional LinkedIn posts based on custom topics, post type,
            tone, audience, language, and length.
            """
        )

        st.markdown("### Innovative Features")
        st.write("✅ Custom topic input instead of only fixed dropdown options")
        st.write("✅ AI-based post generation")
        st.write("✅ Post improvement")
        st.write("✅ Hashtag generation")
        st.write("✅ LinkedIn post scoring")
        st.write("✅ Carousel content generation")
        st.write("✅ Download option")

        st.markdown("### Resume Point")
        st.code(
            "Built an AI-powered LinkedIn Content Studio using Streamlit, LangChain, and Groq LLM to generate professional LinkedIn posts, improve content quality, create hashtags, score posts, and generate carousel content for personal branding.",
            language="text"
        )


if __name__ == "__main__":
    main()
