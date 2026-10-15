# AerishuAI — Streamlit starter

Personal AI chat, image generation, and image downloads.

## Windows setup
1. Install Python from https://www.python.org/downloads/ (check “Add Python to PATH”).
2. Open Command Prompt in this folder.
3. Run:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install -r requirements.txt
   ```
4. Create `.streamlit/secrets.toml` and put this in it:
   ```toml
   OPENAI_API_KEY = "your_real_key_here"
   ```
5. Start the app:
   ```bash
   streamlit run app.py
   ```
6. Open the local address printed in the terminal, usually http://localhost:8501.

Get an API key at https://platform.openai.com/api-keys. API billing is separate from a ChatGPT subscription. If `gpt-image-2` is not available to your account, change that model name in `app.py` to an image model you can access.

## Deploy to Streamlit Community Cloud
1. Upload `app.py`, `requirements.txt`, and `.gitignore` to a GitHub repository. Do NOT upload `.streamlit/secrets.toml`.
2. Visit https://share.streamlit.io and create an app from that repository, selecting `app.py` as the entrypoint.
3. In deployment Advanced settings / app settings, add the secret `OPENAI_API_KEY = "your_real_key_here"`.
4. Deploy and test.

Official docs:
- https://docs.streamlit.io/get-started/installation
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/develop/concepts/connections/secrets-management

## Limitations
This starter is for personal testing. It has no login, persistent cloud database, spending-limit enforcement, or multi-user protections. Community Cloud local files may not survive restarts/redeployments; download images you want to keep or add durable object storage. API calls may cost money and image generation is not unlimited for free.
