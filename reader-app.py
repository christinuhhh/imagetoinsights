# app.py

import os
import io

import streamlit as st
from PIL import Image
import google.generativeai as genai

# —————————————————————————————————————————————————————————————————————————————
# 1) CONFIGURE YOUR API KEY
#
# You can either hard-code it (not recommended for production) or set it as an
# environment variable. Example:
#
#   export GENAI_API_KEY="YOUR_ACTUAL_KEY_HERE"
#
# Then, uncomment the line below to read from the environment.
# —————————————————————————————————————————————————————————————————————————————

API_KEY = os.getenv("GENAI_API_KEY", "AIzaSyBV2FmASb4qUKssZhWmVfx2iPHacWSZuGE")
genai.configure(api_key=API_KEY)

# —————————————————————————————————————————————————————————————————————————————
# 2) CHOOSE WHICH GEMINI VARIANT TO USE
#
# Replace "models/gemini-1.5-flash" with whatever model you want (e.g., "models/gemini-2.0-flash").
# —————————————————————————————————————————————————————————————————————————————

MODEL_NAME = "models/gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# —————————————————————————————————————————————————————————————————————————————
# 3) FIXED PROMPT (no more typing every time)
# —————————————————————————————————————————————————————————————————————————————

FIXED_PROMPT = (
   " Identify this document and extract all text, including checkboxes (including what is checked) and signatures."
)

# —————————————————————————————————————————————————————————————————————————————
# 4) STREAMLIT LAYOUT
# —————————————————————————————————————————————————————————————————————————————

st.set_page_config(
    page_title="Document OCR + Signatures/Tick-Mark Detector",
    layout="centered",
)

# … (rest of your imports and configuration)

st.title("BPI Document Text Extractor")

st.markdown(
    """
    
    Upload a scanned document (image).  

    The app will call Gemini with a fixed prompt to:
    1. Identify what type of document it is,  
    2. Extract both printed and handwritten text and indicate tick marks and signatures   
    """
)

uploaded_file = st.file_uploader(
    "Step 1: Upload your document image (PNG, JPG, etc.)",
    type=["png", "jpg", "jpeg", "bmp", "tiff"],
)

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded document", use_container_width=True)

    image_bytes = uploaded_file.read()
    try:
        pil_image = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        st.error(f"❌ Could not open image: {e}")
        st.stop()

    st.markdown("Step 2: Click on the button")
    if st.button("▶️ Read the document"):
        with st.spinner("Analyzing…"):
            try:
                response = model.generate_content([FIXED_PROMPT, pil_image])
                st.success("✅ Done!")
                st.subheader("Gemini’s Response:")
                st.text_area(
                    label="",
                    value=response.text,
                    height=300,
                    max_chars=None,
                    key="gemini_output",
                )
            except Exception as e:
                st.error(f"❌ Error calling Gemini: {e}")
