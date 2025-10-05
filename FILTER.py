import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import random, time, io

st.set_page_config(page_title="👑 Photo Effects App", layout="wide")
st.title("👑 Photo Effects with Crown & Flower Rain")
st.write("Upload your photo and try effects below!")

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
            st.warning("⚠️ Please add **flower.png** in the same folder.")
            flower = None

        if flower:
            # Simulated animation
            frames = []
            for frame_num in range(10):  # 10 falling frames
                frame = edited.copy()
                for _ in range(15):
                    x = random.randint(0, frame.width - 50)
                    y = random.randint(frame.height//10 * frame_num//2, frame.height - 50)
                    frame.alpha_composite(flower, (x, y))
                frames.append(frame)

            # Show animation-like effect
            placeholder = st.empty()
            for f in frames:
                placeholder.image(f, use_container_width=True)
                time.sleep(0.2)
            edited = frames[-1]

    elif effect == "Crown Effect":
        edited = image.copy()
        try:
            crown = Image.open("crown.png").convert("RGBA").resize((150, 80))
        except:
            st.warning("⚠️ Please add **crown.png** in the same folder.")
            crown = None

        if crown:
            st.subheader("🎚️ Adjust Crown Position")
            x_offset = st.slider("Move Crown Left/Right", 0, edited.width - 150, (edited.width - 150)//2)
            y_offset = st.slider("Move Crown Up/Down", 0, edited.height - 80, 10)
            edited.alpha_composite(crown, (x_offset, y_offset))
            st.image(edited, caption="Crown Adjusted", use_container_width=True)

    else:
        edited = image

    # Download button
    buf = io.BytesIO()
    edited.save(buf, format="PNG")
    st.download_button("📥 Download Edited Image", buf.getvalue(), file_name="edited_image.png", mime="image/png")

else:
    st.info("👆 Upload your photo to start editing.")
