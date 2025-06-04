import os
import io

import streamlit as st
from PIL import Image
import google.generativeai as genai

# —————————————————————————————————————————————————————————————————————————————
# 1) CONFIGURE YOUR API KEY
# —————————————————————————————————————————————————————————————————————————————

API_KEY = os.getenv("GENAI_API_KEY", "AIzaSyBV2FmASb4qUKssZhWmVfx2iPHacWSZuGE")
genai.configure(api_key=API_KEY)

# —————————————————————————————————————————————————————————————————————————————
# 2) DEFINE AVAILABLE MODELS
# —————————————————————————————————————————————————————————————————————————————

AVAILABLE_MODELS = [
    "models/gemini-1.5-flash",
    "models/gemini-2.0-flash",
]

# —————————————————————————————————————————————————————————————————————————————
# 3) PAGE CONFIG
# —————————————————————————————————————————————————————————————————————————————

st.set_page_config(
    page_title="BPI Document Text Extractor",
    layout="centered",
)

st.title("BPI Document Text Extractor")

st.markdown(
    """
    This app will:
    1. Let you choose a Gemini variant.  
    2. Upload a scanned document.  
    3. Run text extraction.  
    """
)

# —————————————————————————————————————————————————————————————————————————————
# STEP 0: CHOOSE GEMINI VARIANT (HEADER + SELECTBOX)
# —————————————————————————————————————————————————————————————————————————————

st.header("Step 1: Choose a Gemini variant")
selected_model = st.selectbox(
    "",  # empty label because the header already says “Step 0”
    AVAILABLE_MODELS,
    index=0,
)
model = genai.GenerativeModel(selected_model)

# —————————————————————————————————————————————————————————————————————————————
# STEP 1: UPLOAD THE DOCUMENT (HEADER + FILE_UPLOADER)
# —————————————————————————————————————————————————————————————————————————————

st.header("Step 2: Upload your document")
uploaded_file = st.file_uploader(
    "",  # empty label because the header already says “Step 1”
    type=["png", "jpg", "jpeg", "bmp", "tiff"],
)

# —————————————————————————————————————————————————————————————————————————————
# STEP 2: CLICK BUTTON TO RUN
# —————————————————————————————————————————————————————————————————————————————

if uploaded_file:
    # Show a thumbnail of the uploaded document
    st.image(uploaded_file, caption="Uploaded document", use_container_width=True)

    # Convert to PIL.Image
    image_bytes = uploaded_file.read()
    try:
        pil_image = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        st.error(f"❌ Could not open image: {e}")
        st.stop()

    st.header("Step 3: Click the button extract text")
    if st.button("▶️ Read Document"):
        with st.spinner(f"Analyzing with {selected_model}…"):
            try:
                FIXED_PROMPT = (
                    "Identify this document and extract all text, "
                    "including checkboxes (and state which ones are checked) and signatures."
                )
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
                st.error(f"❌ Error calling {selected_model}: {e}")

# —————————————————————————————————————————————————————————————————————————————
# FOOTER / NOTES
# —————————————————————————————————————————————————————————————————————————————

st.markdown("---")
st.markdown(
    """
    > You can switch models at any time using the “Step 1” dropdown above.  
    """
)
