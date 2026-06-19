import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
import platform

# 1. Page Configuration MUST be the absolute first Streamlit command executed
st.set_page_config(
    page_title="Axxello Onboarding Studio Pro", 
    page_icon="🎨",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 🎛️ GLOBAL CONFIGURATION CONSTANT
LOCKED_CROP_PCT = 84.6 

# Try loading branding assets safely without breaking the boot cycle
logo_main_path = "Axxello Only 1x3.png"
logo_main = None
if os.path.exists(logo_main_path):
    try:
        logo_main = Image.open(logo_main_path)
    except:
        pass

# Custom Corporate CSS Injection
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 100% !important;
    }
    h1, h2, h3 { color: #1F2937; font-weight: 800; }
    h3 { font-size: 1.15rem !important; margin-bottom: 6px !important; margin-top: 0px !important; }
    p { margin-bottom: 8px !important; color: #4B5563; font-size: 14px; }
    hr { margin: 8px 0 !important; border-top: 1px solid #E5E7EB; }
    .stFileUploader { margin-bottom: -10px; }
    
    div.stButton > button { 
        border-radius: 6px; 
        height: 2.8em; 
        font-weight: bold; 
        background-color: #E31B23 !important; 
        color: white !important;
        border: none !important;
        transition: background-color 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #B91C1C !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 700 !important;
        color: #4B5563 !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #E31B23 !important;
        border-bottom-color: #E31B23 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Executive Branded App Header Panel
col_header_logo, col_header_text = st.columns([1, 3.5])
with col_header_logo:
    if logo_main:
        st.image(logo_main, width='stretch')
    else:
        st.title("AXXELLO")
with col_header_text:
    st.markdown("<h2 style='margin-top: 5px; padding-left: 10px; font-size: 1.6rem;'>Corporate Onboarding Studio</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin-top: -12px; padding-left: 10px;'>Instant, zero-latency asset customization and vector typography alignment portal.</p>", unsafe_allow_html=True)

st.write("---")

# Reset Workspace Callback Handler
def reset_workspace_callback():
    st.session_state.input_welcome = "Insert Header"
    st.session_state.input_name = "Insert Name"
    st.session_state.input_role = "Insert Role"
    st.session_state.input_qual = "Insert Qualification"
    if "template_file_input" in st.session_state:
        del st.session_state["template_file_input"]
    if "photo_file_input" in st.session_state:
        del st.session_state["photo_file_input"]
    if "cached_photo_id" in st.session_state:
        del st.session_state["cached_photo_id"]
    if "processed_photo" in st.session_state:
        del st.session_state["processed_photo"]

# Typography Loader Engine (Schibsted Grotesk)
def get_custom_font(style="regular", size=24):
    font_files = {"regular": "SchibstedGrotesk-Regular.ttf", "bold": "SchibstedGrotesk-Bold.ttf", "italic": "SchibstedGrotesk-Italic.ttf"}
    target_file = font_files[style]
    if os.path.exists(target_file):
        return ImageFont.truetype(target_file, size)
    
    system = platform.system()
    if system == "Windows":
        font_dir = "C:\\Windows\\Fonts\\"
        font_map = {"regular": "arial.ttf", "bold": "arialbd.ttf", "italic": "ariali.ttf"}
    elif system == "Darwin": 
        font_dir = "/Library/Fonts/"
        font_map = {"regular": "Arial.ttf", "bold": "Arial Bold.ttf", "italic": "Arial Italic.ttf"}
    else: 
        font_dir = "/usr/share/fonts/truetype/dejavu/"
        font_map = {"regular": "DejaVuSans.ttf", "bold": "DejaVuSans-Bold.ttf", "italic": "DejaVuSans-Oblique.ttf"}
    try: return ImageFont.truetype(font_dir + font_map[style], size)
    except: return ImageFont.load_default()

# 3. Split Workspace Panels
col_controls, col_preview = st.columns([1, 1], gap="large")

with col_controls:
    st.subheader("📥 1. Upload Assets")
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        template_file = st.file_uploader("Base Template Layout", type=["png", "jpg", "jpeg"], key="template_file_input")
    with col_u2:
        new_photo_file = st.file_uploader("Candidate Portrait Photo", type=["png", "jpg", "jpeg"], key="photo_file_input")
    
    st.write("---")
    st.subheader("⚙️ 2. Configuration Console")
    
    tab_text, tab_image = st.tabs(["📝 Edit Text Strings", "🎛️ Image Transforms"])
    
    with tab_text:
        user_welcome = st.text_input("Header Greeting", "Enter Header", key="input_welcome")
        user_name = st.text_input("Full Name", "Enter Name", key="input_name")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            user_role = st.text_input("Job Title / Role", "Enter Role", key="input_role")
        with col_t2:
            user_qual = st.text_input("Qualifications", "Enter Qualification", key="input_qual")
            
        st.markdown("<p style='font-weight: bold; margin-top: 5px; margin-bottom: -5px;'>Text Position Fine-Tuning</p>", unsafe_allow_html=True)
        col_tx, col_ty = st.columns(2)
        with col_tx:
            text_x_pct = st.slider("Footer Left Position (%)", 0.0, 30.0, 2.7, 0.1)
            welcome_x_pct = st.slider("Header Left Position (%)", 0.0, 30.0, 2.7, 0.1)
        with col_ty:
            text_y_pct = st.slider("Footer Top Position (%)", 75.0, 98.0, 89.0, 0.1)
            welcome_y_pct = st.slider("Header Top Position (%)", 0.0, 20.0, 3.2, 0.1)

    with tab_image:
        enable_bg_removal = st.checkbox("Activate AI Background Removal Pipeline", value=True)
        edge_sharpness = st.slider("Edge Sharpness Filter (Cutout Trim)", 1, 255, 128)
        scale_factor = st.slider("Subject Scale Multiplier", 0.1, 2.5, 1.0, 0.05)
        
        col_ox, col_oy = st.columns(2)
        with col_ox:
            offset_x = st.slider("Horizontal Shifting (X)", -500, 500, 0, 5)
        with col_oy:
            offset_y = st.slider("Vertical Shifting (Y)", -500, 500, 50, 5)

    st.write("---")
    st.button("🔄 Reset Studio Engine Workspace", width='stretch', on_click=reset_workspace_callback)

# 4. Processing & Composite Engine Pipeline
if template_file and new_photo_file:
    try:
        template = Image.open(template_file).convert("RGBA")
        
        # Capping massive resolutions to secure cloud memory
        if template.width > 2000:
            t_w = 2000
            t_h = int(template.height * (t_w / template.width))
            template = template.resize((t_w, t_h), Image.Resampling.LANCZOS)
            
        t_width, t_height = template.size
        current_photo_id = f"{new_photo_file.name}_{new_photo_file.size}"
        
        if "cached_photo_id" not in st.session_state or st.session_state.cached_photo_id != current_photo_id:
            raw_photo = Image.open(new_photo_file).convert("RGBA")
            
            if raw_photo.width > 1000:
                p_w = 1000
                p_h = int(raw_photo.height * (p_w / raw_photo.width))
                raw_photo = raw_photo.resize((p_w, p_h), Image.Resampling.LANCZOS)
                
            if enable_bg_removal:
                with col_preview:
                    with st.spinner("🤖 Executing background extractor..."):
                        try:
                            from rembg import remove, new_session 
                            if "rembg_session" not in st.session_state:
                                st.session_state.rembg_session = new_session("u2netp")
                            processed_subject = remove(raw_photo, session=st.session_state.rembg_session)
                        except Exception as ai_err:
                            st.error(f"⚠️ AI Background Engine threw an error: {ai_err}")
                            st.info("💡 Processing with original background instead to prevent freezing.")
                            processed_subject = raw_photo
            else:
                processed_subject = raw_photo
            
            st.session_state.processed_photo = processed_subject
            st.session_state.cached_photo_id = current_photo_id
        else:
            processed_subject = st.session_state.processed_photo

        orig_w, orig_h = processed_subject.size
        
        target_width = int((t_width * 0.55) * scale_factor)
        target_height = int((orig_h * (target_width / orig_w)))
        resized_subject = processed_subject.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        r, g, b, a = resized_subject.split()
        sharp_alpha_lut = [255 if x >= edge_sharpness else 0 for x in range(256)]
        a = a.point(sharp_alpha_lut)
        resized_subject = Image.merge("RGBA", (r, g, b, a))
        
        paste_x = int((t_width - target_width) / 2) + offset_x
        paste_y = int(t_height - target_height) + offset_y 
        
        absolute_crop_y = int(t_height * (LOCKED_CROP_PCT / 100))
        current_image_bottom = paste_y + target_height
        
        if current_image_bottom > absolute_crop_y:
            allowed_height = absolute_crop_y - paste_y
            if allowed_height > 0:
                resized_subject = resized_subject.crop((0, 0, target_width, allowed_height))
            else:
                resized_subject = resized_subject.crop((0, 0, 1, 1))
                
        canvas = Image.new("RGBA", template.size)
        canvas.paste(template, (0, 0))
        canvas.paste(resized_subject, (paste_x, paste_y), resized_subject)
        
        draw = ImageDraw.Draw(canvas)
        
        bg_color_sample = template.getpixel((10, 10))
        mask_width = int(t_width * 0.65)
        mask_height = int(t_height * 0.082)
        draw.rectangle([0, 0, mask_width, mask_height], fill=bg_color_sample)
        
        base_font_unit = int(t_height / 1000)
        
        font_welcome = get_custom_font("regular", size=base_font_unit * 42)
        font_name = get_custom_font("bold", size=base_font_unit * 38)
        font_role = get_custom_font("regular", size=base_font_unit * 23)
        font_qual = get_custom_font("italic", size=base_font_unit * 21)
        
        start_x = int(t_width * (text_x_pct / 100))
        start_y = int(t_height * (text_y_pct / 100))
        w_start_x = int(t_width * (welcome_x_pct / 100))
        w_start_y = int(t_height * (welcome_y_pct / 100))
        
        line_spacing_1 = int(base_font_unit * 46)
        line_spacing_2 = int(base_font_unit * 28)
        
        text_color = (31, 41, 55, 255)
        
        draw.text((w_start_x, w_start_y), user_welcome, font=font_welcome, fill=text_color)
        draw.text((start_x, start_y), user_name, font=font_name, fill=text_color)
        draw.text((start_x, start_y + line_spacing_1), user_role, font=font_role, fill=text_color)
        draw.text((start_x, start_y + line_spacing_1 + line_spacing_2), user_qual, font=font_qual, fill=text_color)
        
        final_output = canvas.convert("RGB")
        
        with col_preview:
            st.subheader("🖥️ Production Canvas Preview")
            st.image(final_output, width='stretch')
            
            buffer = io.BytesIO()
            final_output.save(buffer, format="JPEG", quality=98)
            byte_arr = buffer.getvalue()
            
            st.write("")
            st.download_button(
                label="📥 Download Production Onboarding Asset",
                data=byte_arr,
                file_name=f"onboarding_{user_name.replace(' ', '_')}.jpg",
                mime="image/jpeg",
                width='stretch'
            )
    except Exception as image_engine_error:
        with col_preview:
            st.error(f"❌ Composite Engine Error: {image_engine_error}")
else:
    with col_preview:
        st.subheader("🖥️ Production Canvas Preview")
        st.info("💡 Studio Open: Drag and drop your base template backdrop and a portrait profile image inside the upload boxes to build the graphic.")
