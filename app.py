import streamlit as st
from PIL import Image
import requests
import io

st.set_page_config(page_title="Screenshot-to-Text Tool", page_icon=":camera:")

st.title("Screenshot-to-Text Tool")

st.markdown("""
Welcome! This free tool lets you extract text from screenshots or photos.  
Just upload your image, and the text will appear below.
""")

uploaded_file = st.file_uploader("Upload an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

# Use Streamlit secrets for your API key (set in Streamlit Cloud > App settings > Secrets)
API_KEY = st.secrets["OCR_SPACE_API_KEY"]

def ocr_space_file_upload(file_bytes, api_key):
    url_api = "https://api.ocr.space/parse/image"
    payload = {
        'isOverlayRequired': False,
        'OCREngine': 2  # Try engine 2 for more accuracy
    }
    headers = {'apikey': api_key}
    files = {'filename': ('uploaded_image.png', file_bytes, 'image/png')}
    try:
        r = requests.post(url_api, files=files, data=payload, headers=headers, timeout=30)
        result = r.json()
        st.write(result)  # <-- Debug: print full API response!
        if result.get("IsErroredOnProcessing", False):
            return "OCR API error: " + str(result.get("ErrorMessage", "Unknown error"))
        return result["ParsedResults"][0]["ParsedText"]
    except Exception as e:
        return f"OCR request failed: {e}"

if uploaded_file:
    image = Image.open(uploaded_file)
    st.success("Image uploaded successfully!")
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Convert image to bytes for API upload
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    with st.spinner('Extracting text...'):
        text = ocr_space_file_upload(img_byte_arr, API_KEY)
    st.write("**Extracted Text:**")
    st.code(text, language='text')
else:
    st.info("Upload a screenshot or image file to begin.")

st.markdown("""
---
Made with ❤️ by FlawlessDem0n • [GitHub Repo](https://github.com/FlawlessDem0n/SS-to-Text)
""")
