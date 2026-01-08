# Streamlit Outputs Viewer

A simple Streamlit application to browse, preview, and download images from the repository's `outputs/` directory.

## Features

- **Gallery view**: Browse all images in a grid layout with configurable thumbnails per row
- **Sorting**: Sort images by name, size, or modification date
- **Preview**: View selected images in full size
- **Metadata**: Display image information (filename, path, size, dimensions)
- **Download**: Download any image directly from the app

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app from the repository root:

```bash
streamlit run apps/streamlit_app/app.py
```

Or from this directory:

```bash
cd apps/streamlit_app
streamlit run app.py
```

The app will automatically browse images from the `outputs/` directory in the repository root.

## Controls

- **Sort images by**: Choose how to sort the image gallery (name, size, or modified date)
- **Thumbnails per row**: Adjust the number of thumbnails displayed per row (2-6)
- **Select image**: Choose an image from the dropdown to view full-size with metadata

## Supported Image Formats

- PNG
- JPEG/JPG
- GIF
- BMP
- WebP
- SVG
