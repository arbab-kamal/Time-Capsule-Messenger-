import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Securely fetch OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("❌ OpenAI API key not found. Please set it in the .env file.")
    st.stop()

openai.api_key = openai_api_key

# Streamlit App
st.set_page_config(page_title="Time Capsule Messenger", page_icon="🚀", layout="centered")
st.title("Time Capsule Messenger 🚀")
st.subheader("Write a message to the future and receive a response!")

# User Input Section
st.write("💡 *Send a message to your future self or someone else and imagine what the future might say back!*")
message = st.text_area("📜 Your message to the future:", placeholder="Dear future me...")
year = st.slider("📅 Select the future year:", min_value=2025, max_value=2100, value=2050)
tone = st.selectbox("🎭 Choose the tone of the response:", ["Optimistic", "Humorous", "Sci-Fi", "Realistic"])

# Validate Input
if st.button("📨 Send to the Future"):
    if not message.strip():
        st.warning("⚠️ Please write a message before sending it to the future.")
    else:
        with st.spinner("🔮 Time-traveling to the future..."):
            # Generate AI Response
            prompt = f"""
            You are an AI writing from the year {year}. Respond to this message:
            ---
            {message}
            ---
            Write in a {tone.lower()} tone. Include references to futuristic technologies, slang, and cultural changes."""

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Use gpt-3.5-turbo or gpt-4
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that roleplays as an AI from the future."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                future_response = response['choices'][0]['message']['content'].strip()

                st.success("📩 Message from the Future:")
                st.write(future_response)

            except Exception as e:
                st.error(f"❌ Error generating response: {e}")

# Optional: Futuristic Visualization
st.divider()
st.write("🎨 *Want to see the future? Generate a glimpse of the futuristic world!*")

if st.button("🔍 Generate Futuristic Visual"):
    with st.spinner("🖌️ Rendering the future..."):
        # Replace this description with your own customization
        description = "A futuristic portrait of a person in 2050, surrounded by advanced AI technologies, sleek cybernetic designs, and glowing neon lights."
        try:
            dalle_response = openai.Image.create(
                prompt=description,
                n=1,  # Number of images
                size="1024x1024"  # Resolution of the generated image
            )
            image_url = dalle_response['data'][0]['url']
            st.image(image_url, caption="🔮 A glimpse of the future world")

        except Exception as e:
            st.error(f"❌ Error generating futuristic visual: {e}")


# Footer
st.divider()
st.write("🌟 **Time Capsule Messenger** | Powered by AI | Built with ❤️ in Streamlit")
