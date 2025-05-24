import streamlit as st
import openai
from io import BytesIO
import base64

st.set_page_config(page_title="Mandala Generator", layout="centered")

st.title("🌀 Mandala Art Generator")
st.write("Enter one word for inspiration. We'll generate a black & white mandala using DALL·E 3.")

# Get OpenAI API key securely
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
if api_key:
    openai.api_key = api_key

    prompt_word = st.text_input("🌟 Enter an inspiring word:", max_chars=30)

    if st.button("🎨 Generate Mandala") and prompt_word:
        with st.spinner("Generating your mandala..."):
            full_prompt = f"A highly detailed black and white mandala inspired by the concept of '{prompt_word}'. Intricate symmetry, spiritual art, zen pattern, line art style. High resolution."

            try:
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=full_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )

                image_url = response.data[0].url
                st.image(image_url, caption="Generated Mandala", use_column_width=True)

                # Download link
                response = openai._client._client.get(image_url)
                img_data = response.content
                b64 = base64.b64encode(img_data).decode()
                href = f'<a href="data:file/jpg;base64,{b64}" download="mandala.jpg">📥 Download Mandala</a>'
                st.markdown(href, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.warning("Please enter your OpenAI API key to continue.")
