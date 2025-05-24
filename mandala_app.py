import streamlit as st
from openai import OpenAI
import requests
import base64
from io import BytesIO

st.set_page_config(page_title="Mandala Generator", layout="centered")

st.title("🌀 Mandala Art Generator")
st.write("Enter one word for inspiration. We'll generate a black & white mandala using DALL·E 3.")

# Step 1: Get user API key securely
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)

    # Step 2: Get word input
    prompt_word = st.text_input("🌟 Enter an inspiring word:", max_chars=30)

    if st.button("🎨 Generate Mandala") and prompt_word:
        with st.spinner("Generating your mandala..."):
            full_prompt = (
                f"A highly detailed black and white mandala inspired by the concept of '{prompt_word}'. "
                f"Intricate symmetrical spiritual zen art, elegant linework, 8K resolution."
            )

            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=full_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )

                image_url = response.data[0].url
                st.image(image_url, caption="🖼️ Your Mandala Art", use_column_width=True)

                # Fetch image content
                img_data = requests.get(image_url).content
                b64 = base64.b64encode(img_data).decode()

                # Create download link
                href = f'<a href="data:file/jpg;base64,{b64}" download="mandala.jpg">📥 Download Mandala</a>'
                st.markdown(href, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠️ Error: {e}")
else:
    st.info("Please enter your OpenAI API key to continue.")

