# Streamlit Image Browser

A simple Streamlit application for browsing, previewing, and downloading images from the repository's `outputs/` directory.

## Features

- **Gallery View**: Browse all images in a thumbnail grid
- **Image Selection**: Click on thumbnails or use the sidebar dropdown to select an image
- **Full-size Preview**: View the selected image at full resolution
- **Metadata Display**: See filename, path, file size, and image dimensions
- **Download**: Download any image with a single click
- **Sorting Options**: Sort images by name, size, or modification date
- **Customizable Layout**: Adjust the number of thumbnails per row (2-6)

## Supported Image Formats

- PNG
- JPG/JPEG
- GIF
- BMP
- WEBP
- SVG

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

From the repository root, run:

```bash
streamlit run apps/streamlit_app/app.py
```

The application will automatically detect the repository root and load images from the `outputs/` directory.

## Usage

1. **Browse**: View all available images in the gallery
2. **Sort**: Use the sidebar to sort images by name, size, or modification date
3. **Adjust Layout**: Use the slider to change the number of thumbnails per row
4. **Select**: Click "Select" under a thumbnail or use the dropdown in the sidebar
5. **View Details**: The selected image will be displayed full-size with metadata
6. **Download**: Click the "Download Image" button to save the image locally

## Notes

- The app uses caching for better performance when loading images
- Images are loaded from the `outputs/` directory relative to the repository root
- The application is designed for local development and exploration
