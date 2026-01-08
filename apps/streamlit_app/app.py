# Streamlit app to browse images in the repository outputs/ folder
# Save as: apps/streamlit_app/app.py

import io
from pathlib import Path
from PIL import Image
import streamlit as st

st.set_page_config(page_title="Repo Outputs Viewer", layout="wide")

# Resolve repository root (two levels up from this file)
REPO_ROOT = Path(__file__).resolve().parents[2]
IMAGES_DIR = REPO_ROOT / "outputs"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg"}

st.title("Repository Outputs Viewer")
st.markdown("Browse images from the repository `outputs/` directory.")

def list_images(images_dir: Path):
    if not images_dir.exists():
        return []
    images = [p for p in sorted(images_dir.iterdir()) if p.suffix.lower() in IMAGE_EXTS and p.is_file()]
    return images

@st.cache_data
def load_image(path: Path):
    # For SVG we just return bytes (streamlit handles svg via st.image if bytes are passed)
    try:
        if path.suffix.lower() == ".svg":
            return path.read_bytes()
        img = Image.open(path)
        img.load()
        return img
    except Exception as e:
        return None

def image_info(path: Path):
    try:
        size_bytes = path.stat().st_size
        kb = size_bytes / 1024
        info = {"filename": path.name, "path": str(path.relative_to(REPO_ROOT)), "size_kb": round(kb, 2)}
        if path.suffix.lower() != ".svg":
            img = Image.open(path)
            info["width"], info["height"] = img.size
        return info
    except Exception:
        return {"filename": path.name, "path": str(path), "size_kb": None}

images = list_images(IMAGES_DIR)

if not images:
    st.info(f"No images found in `{IMAGES_DIR}`. Make sure the repository has an `outputs/` directory with images.")
    st.stop()

# Sidebar controls
st.sidebar.header("Controls")
sort_order = st.sidebar.radio("Sort images by", ["name", "size", "modified"], index=0)
thumbs_per_row = st.sidebar.slider("Thumbnails per row", min_value=2, max_value=6, value=4)

# sort images
if sort_order == "size":
    images = sorted(images, key=lambda p: p.stat().st_size if p.exists() else 0, reverse=True)
elif sort_order == "modified":
    images = sorted(images, key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
else:
    images = sorted(images, key=lambda p: p.name.lower())

selected = st.sidebar.selectbox("Select image", [p.name for p in images])

# Gallery
st.subheader("Gallery")
cols = st.columns(thumbs_per_row)
for idx, img_path in enumerate(images):
    col = cols[idx % thumbs_per_row]
    with col:
        data = load_image(img_path)
        if data is None:
            st.error(f"Could not load {img_path.name}")
            continue
        # show thumbnail (Streamlit will scale)
        st.image(data, caption=img_path.name, use_column_width=True)

# Show selected image full-size and metadata
st.markdown("---")
st.header("Selected image")
sel_path = IMAGES_DIR / selected
sel_data = load_image(sel_path)
if sel_data is None:
    st.error("Unable to load the selected image.")
else:
    if isinstance(sel_data, bytes):
        st.image(sel_data, use_column_width=True)
        file_bytes = sel_data
    else:
        st.image(sel_data, use_column_width=True)
        buf = io.BytesIO()
        sel_data.save(buf, format=sel_data.format or "PNG")
        file_bytes = buf.getvalue()

    info = image_info(sel_path)
    st.markdown("**Metadata**")
    st.write(info)

    # download button
    st.download_button(
        label="Download image",
        data=file_bytes,
        file_name=sel_path.name,
        mime="image/" + (sel_path.suffix.replace(".", "") or "png")
    )

st.markdown("---")
st.caption(f"Images loaded from `{IMAGES_DIR}` (repo root: `{REPO_ROOT}`).")
