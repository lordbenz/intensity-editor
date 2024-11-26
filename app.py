import streamlit as st
from streamlit_drawable_canvas import st_canvas
import os
import cv2
import numpy as np
from PIL import Image
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
        if st.button("Save Result"):
            output_path = os.path.splitext(image_path)[0] + f"_modified.png"
            cv2.imwrite(output_path, cv2.cvtColor(result_display_rgb, cv2.COLOR_RGB2BGR))
            st.success(f"Modified image saved to {output_path}")

    with save_col2:
        if st.button("Save Mask"):
            mask_output_path = os.path.splitext(image_path)[0] + "_mask.png"
            cv2.imwrite(mask_output_path, mask)
            st.success(f"Mask image saved to {mask_output_path}")

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

    folder_path = st.sidebar.text_input("Enter the folder path containing images:", value=".")

    if os.path.isdir(folder_path):
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        if image_files:
            selected_image = st.sidebar.selectbox("Select an image:", image_files)
            image_path = os.path.join(folder_path, selected_image)

            image = cv2.imread(image_path)
            if image is not None:
                edit_image(image, image_path)
            else:
                st.error("Failed to load the image.")
        else:
            st.error("No image files found in the selected directory.")
    else:
        st.error("The provided folder path is invalid.")

if __name__ == "__main__":
    main()
