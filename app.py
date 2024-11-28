import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
from PIL import Image
import io
from utils import apply_intensity_reduction

def edit_image(image, image_path):
    st.header("Normal Map Editor")

    with st.sidebar:
        st.subheader("Parameters")
        intensity_reduction = st.slider("Intensity Reduction:", min_value=0.0, max_value=1.0, value=0.5)
        isReduceNoise = st.checkbox("Reduce Noise", value=False)

        drawing_mode = st.selectbox(
            "Drawing Tool:",
            ("freedraw", "line", "rect", "circle", "transform", "erase"),
        )

        stroke_width = st.slider("Stroke width:", 1, 50, 5)
        stroke_color = st.color_picker("Stroke Color:", "#FF0000")
        bg_color = st.color_picker("Background Color:", "#FFFFFF")

        if st.button("Clear Canvas"):
            st.session_state['canvas_key'] += 1  # Change the key to force canvas reset

    if 'canvas_key' not in st.session_state:
        st.session_state['canvas_key'] = 0

    # Get image dimensions
    img_height, img_width = image.shape[:2]

    # Create columns with fixed width
    col1, col2 = st.columns([img_width, img_width])

    with col1:
        st.write("Draw Mask")
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",  # Fixed fill color with some opacity
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            background_image=Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)),
            height=img_height,
            width=img_width,
            drawing_mode=drawing_mode,
            key=f"canvas_{st.session_state['canvas_key']}",
            display_toolbar=True,
        )

    with col2:
        st.write("Result Image")
        if canvas_result.image_data is not None:
            mask_data = canvas_result.image_data[:, :, 3]  # Alpha channel as mask
            mask = np.where(mask_data > 0, 255, 0).astype(np.uint8)

            result = apply_intensity_reduction(
                image.astype(np.float32),
                mask,
                intensity_reduction=intensity_reduction,
                isReduceNoise=isReduceNoise
            )
            result_display = np.clip(result, 0, 255).astype(np.uint8)
            result_display_rgb = cv2.cvtColor(result_display, cv2.COLOR_BGR2RGB)

            st.image(result_display_rgb, caption='Result Image', width=img_width)
        else:
            st.write("Draw on the canvas to see the result here.")

    # Save options
    save_col1, save_col2 = st.columns(2)
    with save_col1:
        if 'result_display_rgb' in locals():
            result_pil_image = Image.fromarray(result_display_rgb)
            result_bytes = io.BytesIO()
            result_pil_image.save(result_bytes, format='PNG')
            result_bytes.seek(0)
            st.download_button(
                label="Download Result",
                data=result_bytes,
                file_name=f"{os.path.splitext(image_path)[0]}_modified.png",
                mime="image/png"
            )
    with save_col2:
        if 'mask' in locals():
            mask_pil_image = Image.fromarray(mask)
            mask_bytes = io.BytesIO()
            mask_pil_image.save(mask_bytes, format='PNG')
            mask_bytes.seek(0)
            st.download_button(
                label="Download Mask",
                data=mask_bytes,
                file_name=f"{os.path.splitext(image_path)[0]}_mask.png",
                mime="image/png"
            )

def main():
    st.set_page_config(layout="wide")
    st.title("Normal Map Intensity Editor")

    st.markdown(
        """
        <style>
        [data-testid="stHorizontalBlock"] {
            align-items: start;
        }
        canvas {
            max-width: none !important;
        }
        img {
            max-width: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.header("Image Selection")

    uploaded_file = st.sidebar.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg', 'bmp'])
    if uploaded_file is not None:
        try:
            image = np.array(Image.open(uploaded_file).convert('RGB'))
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_path = uploaded_file.name
            edit_image(image, image_path)
        except Exception:
            st.error("Failed to load the image. Please ensure it's a valid image file.")
    else:
        st.sidebar.write("Please upload an image file.")

if __name__ == "__main__":
    main()
