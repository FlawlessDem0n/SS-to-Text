import streamlit as st
from PIL import Image
import pytesseract

st.set_page_config(page_title="Screenshot-to-Text Tool", page_icon=":camera:")

st.title("Screenshot-to-Text Tool")

st.markdown("""
Welcome! This free tool lets you extract text from screenshots or photos.  
Just upload your image, and the text will appear below.
""")

uploaded_file = st.file_uploader("Upload an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.success("Image uploaded successfully!")
    st.image(image, caption='Uploaded Image', use_column_width=True)

    text = pytesseract.image_to_string(image)
    st.write("**Extracted Text:**")
    st.code(text, language='text')

st.markdown("""
---
Made with Streamlit ❤️ by FlawlessDem0n • [GitHub Repo](https://github.com/FlawlessDem0n/SS-to-Text)
""")
