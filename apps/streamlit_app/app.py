import os
import streamlit as st
from pathlib import Path
from PIL import Image

# Detect repository root relative to this file
SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT = SCRIPT_DIR.parent.parent
OUTPUTS_DIR = REPO_ROOT / "outputs"

# Supported image extensions
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg'}


@st.cache_data
def get_image_files(outputs_dir):
    """Get all image files from the outputs directory."""
    image_files = []
    if not outputs_dir.exists():
        return image_files
    
    for file_path in outputs_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
            image_files.append(file_path)
    
    return image_files


@st.cache_data
def load_image(file_path):
    """Load an image using Pillow."""
    try:
        img = Image.open(file_path)
        return img
    except Exception as e:
        st.error(f"Error loading image {file_path.name}: {e}")
        return None


@st.cache_data
def get_image_metadata(file_path):
    """Get metadata for an image file."""
    metadata = {
        'filename': file_path.name,
        'path': str(file_path),
        'size_kb': round(file_path.stat().st_size / 1024, 2),
        'modified': file_path.stat().st_mtime
    }
    
    # Try to get image dimensions
    try:
        img = Image.open(file_path)
        metadata['width'] = img.width
        metadata['height'] = img.height
    except Exception:
        metadata['width'] = None
        metadata['height'] = None
    
    return metadata


def sort_images(image_files, sort_by):
    """Sort image files based on the selected criteria."""
    if sort_by == "Name":
        return sorted(image_files, key=lambda x: x.name.lower())
    elif sort_by == "Size":
        return sorted(image_files, key=lambda x: x.stat().st_size, reverse=True)
    elif sort_by == "Modified":
        return sorted(image_files, key=lambda x: x.stat().st_mtime, reverse=True)
    return image_files


def main():
    st.set_page_config(
        page_title="Image Browser",
        page_icon="🖼️",
        layout="wide"
    )
    
    st.title("🖼️ Repository Outputs Image Browser")
    st.markdown(f"**Outputs Directory:** `{OUTPUTS_DIR}`")
    
    # Get all image files
    image_files = get_image_files(OUTPUTS_DIR)
    
    if not image_files:
        st.warning(f"No image files found in `{OUTPUTS_DIR}`")
        st.info(f"Supported formats: {', '.join(sorted(IMAGE_EXTENSIONS))}")
        return
    
    # Sidebar controls
    st.sidebar.header("⚙️ Controls")
    
    # Sort options
    sort_by = st.sidebar.selectbox(
        "Sort by",
        ["Name", "Size", "Modified"],
        index=0
    )
    
    # Number of thumbnails per row
    thumbnails_per_row = st.sidebar.slider(
        "Thumbnails per row",
        min_value=2,
        max_value=6,
        value=4,
        step=1
    )
    
    # Sort images
    sorted_images = sort_images(image_files, sort_by)
    
    # Image selection
    image_names = [img.name for img in sorted_images]
    selected_image_name = st.sidebar.selectbox(
        "Select an image",
        image_names,
        index=0
    )
    
    # Find the selected image file
    selected_image = next((img for img in sorted_images if img.name == selected_image_name), sorted_images[0])
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"**Total Images:** {len(image_files)}")
    
    # Main content area - split into gallery and details
    st.header("📸 Gallery")
    
    # Display thumbnails in a grid
    cols = st.columns(thumbnails_per_row)
    for idx, img_path in enumerate(sorted_images):
        col_idx = idx % thumbnails_per_row
        with cols[col_idx]:
            img = load_image(img_path)
            if img:
                st.image(img, caption=img_path.name, use_container_width=True)
                if st.button(f"Select", key=f"select_{idx}"):
                    # Update selection (this will trigger a rerun)
                    st.session_state['selected_image'] = img_path.name
    
    # If there's a selection in session state, use it
    if 'selected_image' in st.session_state:
        selected_image_name = st.session_state['selected_image']
        selected_image = next((img for img in sorted_images if img.name == selected_image_name), sorted_images[0])
    
    st.markdown("---")
    st.header("🔍 Selected Image Details")
    
    # Load selected image
    selected_img = load_image(selected_image)
    
    if selected_img:
        # Display full-size image
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Preview")
            st.image(selected_img, caption=selected_image.name, use_container_width=True)
        
        with col2:
            st.subheader("Metadata")
            metadata = get_image_metadata(selected_image)
            
            st.markdown(f"**Filename:** `{metadata['filename']}`")
            st.markdown(f"**Path:** `{metadata['path']}`")
            st.markdown(f"**Size:** {metadata['size_kb']} KB")
            
            if metadata['width'] and metadata['height']:
                st.markdown(f"**Dimensions:** {metadata['width']} × {metadata['height']} px")
            
            # Download button
            st.markdown("---")
            with open(selected_image, "rb") as file:
                file_data = file.read()
            btn = st.download_button(
                label="📥 Download Image",
                data=file_data,
                file_name=selected_image.name,
                mime=f"image/{selected_image.suffix[1:]}"
            )


if __name__ == "__main__":
    main()
