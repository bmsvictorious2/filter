import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import random
import io

st.set_page_config(page_title="👑 Photo Effects with Crown & Flowers", layout="wide")

st.title("👑 Photo Effects with Crown & Flowers")
st.write("Upload your photo and apply fun effects below!")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGBA")
    st.image(image, caption="Original Image", use_container_width=True)

    effect = st.radio("Choose an Effect", ["None", "Grayscale", "Flower Rain", "Crown Effect"], horizontal=True)

    if effect == "Grayscale":
        edited = image.convert("L").convert("RGBA")

    elif effect == "Flower Rain":
        edited = image.copy()
        try:
            flower = Image.open("flower.png").convert("RGBA").resize((50, 50))
        except:
            st.warning("⚠️ Please add a file named **flower.png** in the same folder.")
            flower = None
        if flower:
            for _ in range(20):
                x = random.randint(0, edited.width - 50)
                y = random.randint(0, edited.height - 50)
                edited.alpha_composite(flower, (x, y))

    elif effect == "Crown Effect":
        edited = image.copy()
        try:
            crown = Image.open("crown.png").convert("RGBA").resize((150, 80))
        except:
            st.warning("⚠️ Please add a file named **crown.png** in the same folder.")
            crown = None
        if crown:
            x = (edited.width - crown.width) // 2
            y = 10
            edited.alpha_composite(crown, (x, y))

    else:
        edited = image

    # Show result
    st.image(edited, caption=f"Effect Applied: {effect}", use_container_width=True)

    # Download option
    buf = io.BytesIO()
    edited.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 Download Edited Image",
        data=byte_im,
        file_name="edited_image.png",
        mime="image/png"
    )

else:
    st.info("👆 Upload a photo to start editing.")
