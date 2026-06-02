import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]


def main():
    st.set_page_config(
        page_title="LinkedIn Post Generator",
        page_icon="📝",
        layout="centered"
    )

    st.title("📝 LinkedIn Post Generator")
    st.write("Generate LinkedIn posts using AI based on topic, length, and language.")

    try:
        fs = FewShotPosts()
        tags = fs.get_tags()

        if not tags:
            st.error("No tags found. Please check data/processed_posts.json file.")
            return

    except FileNotFoundError:
        st.error("data/processed_posts.json file not found.")
        st.info("Create a data folder and add processed_posts.json inside it.")
        return

    except Exception as e:
        st.error("Error loading few-shot data.")
        st.exception(e)
        return

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        selected_language = st.selectbox("Language", options=language_options)

    if st.button("Generate Post"):
        with st.spinner("Generating LinkedIn post..."):
            try:
                post = generate_post(
                    selected_length,
                    selected_language,
                    selected_tag
                )

                st.subheader("Generated LinkedIn Post")
                st.write(post)

            except ValueError as e:
                st.error("API key missing.")
                st.exception(e)

            except Exception as e:
                st.error("Groq API connection failed.")
                st.warning(
                    "Check Streamlit Secrets, Groq API key, model name, and Groq account status."
                )
                st.exception(e)


if __name__ == "__main__":
    main()
