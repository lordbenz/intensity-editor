import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
from PIL import Image
import io
from utils import apply_intensity_reduction

def edit_image(image, image_name):
    st.header("Normal Map Editor")    

    if 'canvas_key' not in st.session_state:
        st.session_state['canvas_key'] = 0

    with st.sidebar:
        st.subheader("Parameters")
        intensity_reduction = st.slider(
            "Intensity Reduction:", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.5, 
            step=0.01
        )
        isReduceNoise = st.checkbox("Reduce Noise", value=False)

        drawing_mode = st.selectbox(
            "Drawing Tool:",
            ("freedraw", "line", "rect", "circle", "transform", "erase"),
        )

        stroke_width = st.slider("Stroke Width:", 1, 50, 5)
        stroke_color = st.color_picker("Stroke Color:", "#FF0000")
        bg_color = st.color_picker("Background Color:", "#FFFFFF")

        if st.button("Clear Canvas"):
            st.session_state['canvas_key'] += 1  # Change the key to force canvas reset

    try:
        img_height, img_width = image.shape[:2]

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Draw Mask")
            canvas_result = st_canvas(
                fill_color="rgba(255, 0, 0, 0.3)",  
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
            st.subheader("Result Image")
            if canvas_result.image_data is not None:
                # Extract the alpha channel as the mask
                mask_data = canvas_result.image_data[:, :, 3]
                mask = np.where(mask_data > 0, 255, 0).astype(np.uint8)

                # Apply intensity reduction
                result = apply_intensity_reduction(
                    image.astype(np.float32),
                    mask,
                    intensity_reduction=intensity_reduction,
                    isReduceNoise=isReduceNoise
                )
                result_display = np.clip(result, 0, 255).astype(np.uint8)
                result_display_rgb = cv2.cvtColor(result_display, cv2.COLOR_BGR2RGB)

                st.image(
                    result_display_rgb, 
                    caption='Result Image', 
                    use_container_width=True
                )
            else:
                st.info("Draw on the canvas to see the result here.")

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
                    file_name=f"{os.path.splitext(image_name)[0]}_modified.png",
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
                    file_name=f"{os.path.splitext(image_name)[0]}_mask.png",
                    mime="image/png"
                )
    except Exception as e:
        st.error("An unexpected error occurred while processing the image.")

def main():
    st.set_page_config(layout="wide")
    st.title("Normal Map Intensity Editor")
    st.text("version 0.0.1")

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

    uploaded_files = st.sidebar.file_uploader(
        "Choose image files", 
        type=['png', 'jpg', 'jpeg', 'bmp'], 
        accept_multiple_files=True
    )

    if uploaded_files:
        try:
            image_names = [file.name for file in uploaded_files]
            selected_image_name = st.sidebar.selectbox(
                "Select an image to edit:", 
                image_names
            )

            selected_file = next(
                (file for file in uploaded_files if file.name == selected_image_name), 
                None
            )

            if selected_file is not None:
                image = Image.open(selected_file).convert('RGB')
                image_np = np.array(image)
                image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

                if 'selected_image' not in st.session_state:
                    st.session_state['selected_image'] = selected_image_name
                    st.session_state['canvas_key'] = 0
                elif st.session_state['selected_image'] != selected_image_name:
                    st.session_state['selected_image'] = selected_image_name
                    st.session_state['canvas_key'] += 1  # Reset canvas for new image

                edit_image(image_bgr, selected_image_name)
            else:
                st.sidebar.error("Selected image not found.")
        except Exception as e:
            st.sidebar.error("Failed to load the image. Please ensure it's a valid image file.")
    else:
        st.sidebar.info("Please upload image files to get started.")

if __name__ == "__main__":
    main()
