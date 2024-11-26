
# Normal Map Intensity Editor

A web-based application for artists to edit the intensity of normal maps using an intuitive masking interface. The application allows you to draw masks over areas of a normal map where you want to reduce the intensity and see the results in real-time.

## Features

- **Real-time Editing:** Draw masks over your normal maps and see the intensity reduction applied instantly.
- **Drawing Tools:** Use various drawing tools like freedraw, line, rectangle, circle, transform, and erase.
- **Undo/Redo Functionality:** Utilize the toolbar for undoing or redoing actions.
- **Customizable Parameters:** Adjust intensity reduction levels and stroke properties.
- **Save Results:** Save the modified normal map and the mask image.

## Requirements

- **Python Version:** 3.7 or higher
- **Packages:**
  - `streamlit`
  - `opencv-python`
  - `numpy`
  - `Pillow`
  - `streamlit-drawable-canvas`

## Installation

1. **Clone or Download the Repository**

   ```bash
   git clone https://github.com/lordbenz/intensity-editor
   ```

   *If you don't have Git, you can download the repository as a ZIP file and extract it.*

2. **Navigate to the Project Directory**

   ```bash
   cd normal-map-intensity-editor
   ```

3. **Create a Virtual Environment (Recommended)**

   ```bash
   python -m venv venv
   ```

4. **Activate the Virtual Environment**

   - **Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

5. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

   *If `requirements.txt` is not provided, install the packages manually:*

   ```bash
   pip install streamlit opencv-python numpy Pillow streamlit-drawable-canvas
   ```

## Running the Application

1. **Start the Streamlit App**

   ```bash
   streamlit run app.py
   ```

2. **Access the Application**

   - The application will automatically open in your default web browser.
   - If it doesn't, open your browser and go to `http://localhost:8501`.

## Usage Instructions

### 1. Select Image Folder

- In the sidebar on the left, enter the path to the folder containing your normal map images.
  - Example:
    - Windows: `C:\Users\YourName\Pictures\NormalMaps`
    - macOS/Linux: `/home/yourname/Pictures/NormalMaps`
- Press `Enter` after typing the path.

### 2. Select an Image

- A dropdown menu will appear with the list of image files in the specified folder.
- Select the image you wish to edit.

### 3. Adjust Parameters

- **Intensity Reduction:**
  - Use the slider to set the level of intensity reduction (from 0.0 to 1.0).
  - The default value is 0.5.
- **Reduce Noise:**
  - Check this box if you want to apply noise reduction within the masked areas (optional).
- **Drawing Tool:**
  - Choose from `freedraw`, `line`, `rect`, `circle`, `transform`, or `erase`.
- **Stroke Width:**
  - Adjust the stroke width for your drawing tool (range: 1 to 50).
- **Stroke Color:**
  - Choose the color of the stroke.
- **Background Color:**
  - Set the background color of the canvas if needed.

### 4. Draw Mask

- In the **Draw Mask** panel, use your mouse or stylus to draw over the areas where you want to reduce the intensity.
- **Undo/Redo:**
  - Use the toolbar above the canvas to undo or redo your actions.
- **Eraser Tool:**
  - Select `erase` from the drawing tools to erase parts of your mask.

### 5. View Result

- As you draw, the **Result Image** panel updates in real-time to show the effect of the intensity reduction.
- The result image aligns perfectly with your mask for accurate editing.

### 6. Save Your Work

- **Save Result:**
  - Click this button to save the modified normal map.
  - The image will be saved in the same directory as the original image, with `_modified.png` appended to the filename.
- **Save Mask:**
  - Click this button to save the mask image.
  - The mask will be saved with `_mask.png` appended to the filename.

### 7. Clear Canvas

- To start over, click the **Clear Canvas** button in the sidebar to reset the canvas.

## Troubleshooting

- **Canvas and Image Misalignment:**
  - Ensure your browser zoom is set to 100% to prevent scaling issues.
- **Application Not Loading:**
  - Check the terminal for any error messages.
  - Ensure all required packages are installed.
- **Image Not Displaying:**
  - Verify that the image files are valid and in a supported format (`.png`, `.jpg`, `.jpeg`, `.bmp`).
- **Permission Issues:**
  - Ensure you have read and write permissions for the image directory.

## Notes

- **Zoom Functionality:**
  - The application does not support zooming within the canvas.
  - Use your browser's zoom feature as a workaround.
- **Supported Image Formats:**
  - The application supports `.png`, `.jpg`, `.jpeg`, and `.bmp` files.
- **File Overwriting:**
  - Saving multiple times will overwrite existing `_modified.png` and `_mask.png` files.

## Dependencies

List of major dependencies:

- [Streamlit](https://streamlit.io/)
- [OpenCV](https://opencv.org/)
- [NumPy](https://numpy.org/)
- [Pillow](https://pillow.readthedocs.io/)
- [Streamlit Drawable Canvas](https://github.com/andfanilo/streamlit-drawable-canvas)
