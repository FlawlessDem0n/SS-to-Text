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

API_KEY = st.secrets["OCR_SPACE_API_KEY"]



def ocr_space_file_upload(file, api_key):
    url_api = "https://api.ocr.space/parse/image"
    payload = {'isOverlayRequired': False}
    headers = {'apikey': api_key}
    r = requests.post(url_api,
                      files={'filename': file},
                      data=payload,
                      headers=headers)
    result = r.json()
    try:
        text = result["ParsedResults"][0]["ParsedText"]
    except Exception:
        text = "No text found or error with OCR."
    return text

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

st.markdown("""
---
Made with ❤️ by FlawlessDem0n • [GitHub Repo](https://github.com/FlawlessDem0n/SS-to-Text)
""")
