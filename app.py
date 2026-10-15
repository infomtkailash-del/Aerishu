import base64
import os
from pathlib import Path
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AerishuAI", page_icon="✨", layout="wide")
IMAGE_DIR = Path("generated_images")
IMAGE_DIR.mkdir(exist_ok=True)
st.markdown("""
<style>
.stApp{background:#0f1117}[data-testid="stSidebar"]{background:#171a22}
.brand{font-size:2rem;font-weight:800;letter-spacing:-1px}.brand span{color:#b9f36b}
</style>""", unsafe_allow_html=True)

def api_key():
    try: key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception: key = ""
    return key or os.getenv("OPENAI_API_KEY", "")

key = api_key()
client = OpenAI(api_key=key) if key else None
with st.sidebar:
    st.markdown('<div class="brand">✨ Aerishu<span>AI</span></div>', unsafe_allow_html=True)
    st.caption("Your personal AI studio")
    page = st.radio("Workspace", ["AI Chat", "Image Studio", "Saved Images"])
    if st.button("＋ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("Keep your API key private.")
if "messages" not in st.session_state: st.session_state.messages = []
if not key:
    st.warning("Add your API key to .streamlit/secrets.toml to enable AI features.")
    st.code('OPENAI_API_KEY = "your_real_api_key_here"', language="toml")
    st.markdown("Get a key from [the OpenAI API keys page](https://platform.openai.com/api-keys). API billing is separate from a ChatGPT subscription.")

if page == "AI Chat":
    st.title("How can I help you today?")
    st.caption("Chat, brainstorm, learn, write, and plan with AerishuAI.")
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    prompt = st.chat_input("Message AerishuAI…")
    if prompt:
        st.session_state.messages.append({"role":"user", "content":prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            if not client:
                answer = "Please configure your API key in .streamlit/secrets.toml and restart the app."
                st.info(answer)
            else:
                try:
                    with st.spinner("AerishuAI is thinking…"):
                        result = client.chat.completions.create(
                            model="gpt-4.1-mini",
                            messages=[{"role":"system","content":"You are AerishuAI, a helpful, clear, friendly personal AI assistant."}, *st.session_state.messages])
                    answer = result.choices[0].message.content or "Please try again."
                    st.markdown(answer)
                except Exception as e:
                    answer = f"Request failed: {e}"
                    st.error(answer)
        st.session_state.messages.append({"role":"assistant", "content":answer})

elif page == "Image Studio":
    st.title("Image Studio")
    st.caption("Turn your imagination into images.")
    with st.form("image_form"):
        prompt = st.text_area("Describe the image you want", placeholder="A cinematic mountain lake at sunrise, mist, realistic photography…", height=120)
        a,b = st.columns(2)
        with a: quality = st.selectbox("Quality", ["low", "medium", "high"])
        with b: size = st.selectbox("Image shape", ["1024x1024", "1536x1024", "1024x1536"])
        count = st.selectbox("Number of images", [1,2,3,4])
        submitted = st.form_submit_button("✨ Generate images", use_container_width=True)
    if submitted:
        if not prompt.strip(): st.error("Enter an image description first.")
        elif not client: st.error("Configure your API key before generating images.")
        else:
            try:
                with st.spinner("Generating image(s)…"):
                    result = client.images.generate(model="gpt-image-2", prompt=prompt.strip(), size=size, quality=quality, n=count)
                for i,item in enumerate(result.data):
                    if not item.b64_json:
                        st.error("The provider returned no image data for this result."); continue
                    data = base64.b64decode(item.b64_json)
                    path = IMAGE_DIR / f"aerishuai_{len(list(IMAGE_DIR.glob('*.png')))+1}_{i+1}.png"
                    path.write_bytes(data)
                    st.image(data, caption=prompt.strip(), use_container_width=True)
                    st.download_button("⬇ Download image", data=data, file_name=path.name, mime="image/png", key=f"download_{path.name}")
            except Exception as e:
                st.error(f"Image generation failed: {e}")
                st.caption("Check your API access, billing, model availability, and the error details.")
else:
    st.title("Saved Images")
    files = sorted(IMAGE_DIR.glob("*.png"), key=lambda p:p.stat().st_mtime, reverse=True)
    if not files: st.info("No images saved yet. Visit Image Studio to create your first image.")
    for p in files:
        st.image(str(p), caption=p.name, use_container_width=True)
        st.download_button(f"⬇ Download {p.name}", data=p.read_bytes(), file_name=p.name, mime="image/png", key=f"saved_{p.name}")
st.divider()
st.caption("AerishuAI • AI generation requires a compatible API account and may incur charges.")
