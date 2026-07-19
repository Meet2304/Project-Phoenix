"""
Streamlit Dashboard for CBAM-ResNet50 Cervical Cancer Cell Classification
Complete Pipeline: Raw Image → Preprocessing → Classification → Explainability
"""

import streamlit as st
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, models
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
import pandas as pd
import plotly.express as px
from skimage.metrics import structural_similarity as ssim

# Grad-CAM libraries
from pytorch_grad_cam import GradCAMPlusPlus
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

# ============================================================================
# MODEL ARCHITECTURE DEFINITION
# ============================================================================

class ChannelAttention(nn.Module):
    """Channel Attention Module - focuses on 'what' is meaningful."""
    def __init__(self, in_channels, reduction_ratio=16):
        super(ChannelAttention, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        self.fc = nn.Sequential(
            nn.Conv2d(in_channels, in_channels // reduction_ratio, 1, bias=False),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels // reduction_ratio, in_channels, 1, bias=False)
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = self.fc(self.avg_pool(x))
        max_out = self.fc(self.max_pool(x))
        out = self.sigmoid(avg_out + max_out)
        return x * out


class SpatialAttention(nn.Module):
    """Spatial Attention Module - focuses on 'where' is meaningful."""
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        padding = 3 if kernel_size == 7 else 1
        self.conv = nn.Conv2d(2, 1, kernel_size, padding=padding, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        out = torch.cat([avg_out, max_out], dim=1)
        out = self.sigmoid(self.conv(out))
        return x * out


class CBAM(nn.Module):
    """Convolutional Block Attention Module (CBAM)."""
    def __init__(self, in_channels, reduction_ratio=16, kernel_size=7):
        super(CBAM, self).__init__()
        self.channel_attention = ChannelAttention(in_channels, reduction_ratio)
        self.spatial_attention = SpatialAttention(kernel_size)

    def forward(self, x):
        x = self.channel_attention(x)
        x = self.spatial_attention(x)
        return x


class CBAM_ResNet50(nn.Module):
    """ResNet50 with CBAM attention modules."""
    def __init__(self, num_classes=5, pretrained=False):
        super(CBAM_ResNet50, self).__init__()
        
        resnet = models.resnet50(weights=None)

        self.conv1 = resnet.conv1
        self.bn1 = resnet.bn1
        self.relu = resnet.relu
        self.maxpool = resnet.maxpool

        self.layer1 = resnet.layer1
        self.cbam1 = CBAM(256)

        self.layer2 = resnet.layer2
        self.cbam2 = CBAM(512)

        self.layer3 = resnet.layer3
        self.cbam3 = CBAM(1024)

        self.layer4 = resnet.layer4
        self.cbam4 = CBAM(2048)

        self.avgpool = resnet.avgpool
        self.fc = nn.Linear(2048, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.cbam1(x)

        x = self.layer2(x)
        x = self.cbam2(x)

        x = self.layer3(x)
        x = self.cbam3(x)

        x = self.layer4(x)
        x = self.cbam4(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        logits = self.fc(x)
        return logits


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

@st.cache_resource
def load_model(model_path):
    """Load the trained CBAM-ResNet50 model."""
    # Get the directory where app.py is located
    app_dir = Path(__file__).parent
    full_model_path = app_dir / model_path
    
    if not full_model_path.exists():
        st.error(f"❌ Model file not found at {full_model_path}")
        st.stop()
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    checkpoint = torch.load(full_model_path, map_location=device)
    
    class_names = ['Dyskeratotic', 'Koilocytotic', 'Metaplastic', 'Parabasal', 'Superficial-Intermediate']
    num_classes = 5
    
    model = CBAM_ResNet50(num_classes=num_classes)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()
    
    return model


def preprocess_image_for_model(image_pil):
    """Preprocess PIL image for model inference."""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    img_tensor = transform(image_pil).unsqueeze(0).to(device)
    return img_tensor


def predict(image_pil, model):
    """Get model prediction."""
    class_names = ['Dyskeratotic', 'Koilocytotic', 'Metaplastic', 'Parabasal', 'Superficial-Intermediate']
    
    img_tensor = preprocess_image_for_model(image_pil)
    
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)
        pred_idx = torch.argmax(probs, dim=1).item()
        pred_class = class_names[pred_idx]
        confidence = probs[0, pred_idx].item() * 100
        
        # Get all probabilities
        all_probs = {class_names[i]: probs[0, i].item() * 100 for i in range(len(class_names))}
    
    return pred_class, confidence, all_probs


def generate_gradcam(image_pil, model, target_class):
    """Generate GradCAM++ visualization."""
    class_names = ['Dyskeratotic', 'Koilocytotic', 'Metaplastic', 'Parabasal', 'Superficial-Intermediate']
    
    img_tensor = preprocess_image_for_model(image_pil)
    
    # Prepare RGB image for overlay
    rgb_img = np.array(image_pil.resize((224, 224)))
    rgb_img = np.float32(rgb_img) / 255.0
    
    # GradCAM++
    target_layers = [model.layer4[-1]]
    cam = GradCAMPlusPlus(model=model, target_layers=target_layers)
    
    # If target class specified, use it
    if target_class in class_names:
        target_idx = class_names.index(target_class)
        targets = [ClassifierOutputTarget(target_idx)]
    else:
        targets = None
    
    grayscale_cam = cam(input_tensor=img_tensor, targets=targets)
    grayscale_cam = grayscale_cam[0, :]
    
    # Create heatmap
    heatmap = cv2.applyColorMap(np.uint8(255 * grayscale_cam), cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    
    # Create overlay
    visualization = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
    
    return heatmap, visualization


# ============================================================================
# PREPROCESSING FUNCTIONS (Training Pipeline)
# ============================================================================

def resize_with_aspect_ratio_mirroring(image, target_size=256):
    """Resize image while preserving aspect ratio using mirroring."""
    h, w = image.shape[:2]
    scale = min(target_size / h, target_size / w)
    new_h, new_w = int(h * scale), int(w * scale)
    
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    
    # Create canvas and center image
    canvas = np.zeros((target_size, target_size, 3), dtype=np.uint8)
    y_offset = (target_size - new_h) // 2
    x_offset = (target_size - new_w) // 2
    canvas[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized
    
    # Mirror padding - vertical (top and bottom)
    if y_offset > 0:
        # Top padding
        top_pad_size = y_offset
        top_mirror = resized[:min(top_pad_size, new_h), :]
        top_mirror = np.flip(top_mirror, axis=0)
        canvas[y_offset - top_mirror.shape[0]:y_offset, x_offset:x_offset + new_w] = top_mirror
        
        # Bottom padding
        bottom_start = y_offset + new_h
        bottom_pad_size = target_size - bottom_start
        bottom_mirror = resized[-min(bottom_pad_size, new_h):, :]
        bottom_mirror = np.flip(bottom_mirror, axis=0)
        canvas[bottom_start:bottom_start + bottom_mirror.shape[0], x_offset:x_offset + new_w] = bottom_mirror
    
    # Mirror padding - horizontal (left and right)
    if x_offset > 0:
        # Left padding
        left_pad_size = x_offset
        left_mirror = canvas[:, x_offset:x_offset + min(left_pad_size, new_w)]
        left_mirror = np.flip(left_mirror, axis=1)
        canvas[:, x_offset - left_mirror.shape[1]:x_offset] = left_mirror
        
        # Right padding
        right_start = x_offset + new_w
        right_pad_size = target_size - right_start
        right_mirror = canvas[:, x_offset + new_w - min(right_pad_size, new_w):x_offset + new_w]
        right_mirror = np.flip(right_mirror, axis=1)
        canvas[:, right_start:right_start + right_mirror.shape[1]] = right_mirror
    
    padding_info = {'scale_factor': scale, 'x_offset': x_offset, 'y_offset': y_offset}
    
    return canvas, padding_info


def apply_nlm_denoising(image, h=3, template_window_size=7, search_window_size=21):
    """Apply Non-Local Means denoising channel-wise."""
    denoised_channels = []
    for i in range(3):
        denoised = cv2.fastNlMeansDenoising(
            image[:, :, i], None, h, template_window_size, search_window_size
        )
        denoised_channels.append(denoised)
    
    return cv2.merge(denoised_channels)


def apply_clahe_enhancement(image, clip_limit=1.2, tile_grid_size=6):
    """Apply CLAHE channel-wise."""
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size, tile_grid_size))
    enhanced_channels = [clahe.apply(image[:, :, i]) for i in range(3)]
    
    return cv2.merge(enhanced_channels)


def apply_preprocessing_pipeline(image_bgr):
    """Complete preprocessing pipeline."""
    # Step 1: Resize
    resized, padding_info = resize_with_aspect_ratio_mirroring(image_bgr, target_size=256)
    
    # Step 2: NLM Denoising
    nlm_denoised = apply_nlm_denoising(resized)
    
    # Step 3: CLAHE Enhancement
    final_image = apply_clahe_enhancement(nlm_denoised)
    
    return resized, nlm_denoised, final_image, padding_info


def calculate_preprocessing_metrics(original, processed):
    """Calculate quality metrics between original and processed images."""
    def calculate_psnr(img1, img2):
        mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)
        if mse == 0:
            return float('inf')
        return 20 * np.log10(255.0 / np.sqrt(mse))
    
    def calculate_ssim(img1, img2):
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        return ssim(gray1, gray2, data_range=255)
    
    def calculate_contrast(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return np.std(gray)
    
    psnr = calculate_psnr(original, processed)
    ssim_val = calculate_ssim(original, processed)
    contrast_orig = calculate_contrast(original)
    contrast_proc = calculate_contrast(processed)
    contrast_improvement = contrast_proc / contrast_orig if contrast_orig != 0 else 0
    
    return {
        'PSNR (dB)': psnr,
        'SSIM': ssim_val,
        'Contrast Improvement': contrast_improvement
    }


# ============================================================================
# STREAMLIT APP
# ============================================================================

def main():
    # Page configuration
    st.set_page_config(
        page_title="Cervical Cancer Cell Classifier",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #555;
            text-align: center;
            margin-bottom: 2rem;
        }
        .prediction-box {
            background-color: #e8f4f8;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 5px solid #1f77b4;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">🔬 Cervical Cancer Cell Classifier</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">CBAM-ResNet50 | Complete Pipeline: Raw Image → Preprocessing → Classification → Explainability</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model path - use relative path for deployment
        default_model_path = "cbam_resnet50_cervical/best_model.pth"
        model_path = st.text_input(
            "Model Path",
            value=default_model_path,
            help="Relative path to model file"
        )
        
        st.markdown("---")
        
        # Image input options
        st.header("📤 Image Input")
        input_method = st.radio(
            "Choose input method:",
            ["Upload Image", "Use Sample Images"],
            help="Upload your own image or select from sample images"
        )
        
        uploaded_file = None
        sample_image_path = None
        
        if input_method == "Upload Image":
            uploaded_file = st.file_uploader(
                "Choose a cervical cell image",
                type=["bmp", "png", "jpg", "jpeg"],
                help="Upload a microscopy image of cervical cells"
            )
        else:
            # Sample images
            st.markdown("**Select a sample image:**")
            
            # Get sample images from relative path (relative to app.py location)
            app_dir = Path(__file__).parent
            sample_dir = app_dir / "sample_image" / "original_images"
            if sample_dir.exists():
                sample_images = sorted([f.name for f in sample_dir.iterdir() if f.suffix.lower() in ['.bmp', '.png', '.jpg', '.jpeg']])
                
                if sample_images:
                    selected_sample = st.selectbox(
                        "Sample Images:",
                        sample_images,
                        help="Select a sample image to analyze"
                    )
                    
                    if selected_sample:
                        sample_image_path = sample_dir / selected_sample
                        
                        # Show preview
                        preview_img = Image.open(sample_image_path)
                        st.image(preview_img, caption=selected_sample, use_container_width=True)
                        
                        # Create a virtual uploaded file for consistency
                        from io import BytesIO
                        buf = BytesIO()
                        preview_img.save(buf, format=preview_img.format if preview_img.format else 'PNG')
                        buf.seek(0)
                        buf.name = selected_sample
                        uploaded_file = buf
                else:
                    st.warning("No sample images found in sample_image/original_images/")
            else:
                st.warning("Sample image directory not found. Please ensure 'sample_image/original_images' exists.")
        
        st.markdown("---")
        
        # Visualization options
        st.header("🎨 Visualization Options")
        show_heatmap = st.checkbox("Show Heatmap Only", value=False)
        show_class_specific = st.checkbox("Show Class-Specific Activations", value=False)
        
        st.markdown("---")
        
        # Info
        st.info("""
        **About:**
        This dashboard demonstrates the complete pipeline from raw image to explainable predictions.
        
        **Cell Types:**
        - Dyskeratotic
        - Koilocytotic
        - Metaplastic
        - Parabasal
        - Superficial-Intermediate
        """)
    
    # Main content
    if uploaded_file is None:
        st.info("👈 Please upload a cervical cell image using the sidebar to begin the analysis pipeline.")
        
        # Show workflow diagram
        st.markdown("---")
        st.markdown("### 🔄 Analysis Pipeline Workflow")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**① Upload Image**")
            st.markdown("📤 Raw microscopy image")
        
        with col2:
            st.markdown("**② Preprocessing**")
            st.markdown("🔬 Resize → NLM → CLAHE")
        
        with col3:
            st.markdown("**③ Classification**")
            st.markdown("🎯 CBAM-ResNet50 prediction")
        
        with col4:
            st.markdown("**④ Explainability**")
            st.markdown("🔍 GradCAM++ visualization")
        
        # Display model info
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 Model Architecture")
            st.markdown("""
            - **Base:** ResNet50  
            - **Attention:** CBAM (Channel + Spatial)  
            - **Parameters:** 24,214,989  
            - **Explainability:** GradCAM++
            """)

        with col2:
            st.markdown("### 🔬 Preprocessing Steps")
            st.markdown("""
            - **Resize:** 256×256 with mirroring  
            - **NLM Denoising:** h=3, channel-wise  
            - **CLAHE:** clipLimit=1.2, 6×6 tiles  
            - **Quality Metrics:** PSNR, SSIM, Contrast
            """)

        with col3:
            st.markdown("### 📈 Model Performance")
            st.markdown("""
            **Test Set Results:**  
            - **Accuracy:** 94.32%  
            - **Precision:** 94.40%  
            - **Recall:** 94.32%  
            - **F1-Score:** 94.34%
            """)
    
    else:
        # STEP 1: PREPROCESSING PIPELINE
        st.markdown("---")
        st.markdown("## 🔬 Step 1: Image Preprocessing Pipeline")
        st.markdown("The uploaded raw image is preprocessed to enhance quality and remove noise before classification.")
        
        # Load the uploaded image
        image_pil = Image.open(uploaded_file).convert('RGB')
        image_bgr = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        
        with st.spinner("Applying preprocessing pipeline..."):
            # Apply preprocessing
            resized, nlm_denoised, final_image, padding_info = apply_preprocessing_pipeline(image_bgr)
            
            # Calculate metrics
            metrics = calculate_preprocessing_metrics(resized, final_image)
        
        # Display preprocessing steps
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**📸 Original**")
            st.image(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB), use_container_width=True)
            st.caption(f"Size: {image_bgr.shape[1]}×{image_bgr.shape[0]}")
        
        with col2:
            st.markdown("**① Resized (256×256)**")
            st.image(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB), use_container_width=True)
            st.caption(f"Scale: {padding_info['scale_factor']:.3f}")
        
        with col3:
            st.markdown("**② NLM Denoised**")
            st.image(cv2.cvtColor(nlm_denoised, cv2.COLOR_BGR2RGB), use_container_width=True)
            st.caption("Noise reduced")
        
        with col4:
            st.markdown("**✅ Final (+ CLAHE)**")
            st.image(cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB), use_container_width=True)
            st.caption("Enhanced contrast")
        
        # Show metrics
        st.markdown("")
        metric_cols = st.columns([1, 1, 1, 2])
        with metric_cols[0]:
            st.metric("PSNR", f"{metrics['PSNR (dB)']:.2f} dB", help="Peak Signal-to-Noise Ratio")
        with metric_cols[1]:
            st.metric("SSIM", f"{metrics['SSIM']:.4f}", help="Structural Similarity Index")
        with metric_cols[2]:
            st.metric("Contrast", f"{metrics['Contrast Improvement']:.2f}×", help="Contrast Improvement Ratio")
        
        with st.expander("⚙️ Preprocessing Parameters"):
            st.markdown("""
            **NLM Denoising:** h=3, template=7×7, search=21×21, channel-wise  
            **CLAHE Enhancement:** clipLimit=1.2, tileGrid=6×6, channel-wise  
            **Resize:** 256×256 with aspect ratio preservation + mirroring
            """)
        
        # STEP 2: CLASSIFICATION
        st.markdown("---")
        st.markdown("## 🎯 Step 2: Cell Classification")
        st.markdown("The **preprocessed image** is now fed into the CBAM-ResNet50 model for classification.")
        
        # Load model
        with st.spinner("Loading CBAM-ResNet50 model..."):
            model = load_model(model_path)
        
        # Convert preprocessed image to PIL for prediction
        preprocessed_pil = Image.fromarray(cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB))
        
        # Get prediction using preprocessed image
        with st.spinner("Making prediction on preprocessed image..."):
            pred_class, confidence, all_probs = predict(preprocessed_pil, model)
        
        # Display classification results
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### 📊 Classification Result")
            st.markdown(f"""
            <div class="prediction-box">
                <h3 style="color: #555;">Predicted Class: {pred_class}</h2>
                <h3 style="color: #555;">Confidence: {confidence:.2f}%</h3>
            </div>
            """, unsafe_allow_html=True)
            # st.markdown(f'<div class="prediction-box">', unsafe_allow_html=True)
            # st.markdown(f"**Predicted Class:** `{pred_class}`")
            # st.markdown(f"**Confidence:** `{confidence:.2f}%`")
            # st.markdown('</div>', unsafe_allow_html=True)
            
            # Download preprocessed image
            st.markdown("")
            from io import BytesIO
            buf = BytesIO()
            preprocessed_pil.save(buf, format='PNG')
            st.download_button(
                label="📥 Download Preprocessed Image",
                data=buf.getvalue(),
                file_name=f"preprocessed_{uploaded_file.name}",
                mime="image/png",
                use_container_width=True
            )
        
        with col2:
            st.markdown("#### 📈 Class Probabilities")
            # Create bar chart
            prob_df = pd.DataFrame({
                'Class': list(all_probs.keys()),
                'Probability': list(all_probs.values())
            })
            fig = px.bar(prob_df, x='Probability', y='Class', orientation='h',
                       color='Probability', color_continuous_scale='Blues')
            fig.update_layout(height=280, showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        
        # STEP 3: EXPLAINABILITY
        st.markdown("---")
        st.markdown("## 🔍 Step 3: Explainable AI (GradCAM++)")
        st.markdown("GradCAM++ highlights which regions of the **preprocessed image** were most important for the model's classification decision.")
        
        with st.spinner("Generating GradCAM++ visualization..."):
            heatmap, overlay = generate_gradcam(preprocessed_pil, model, pred_class)
        
        # col1, col2 = st.columns(2)
        
        if show_heatmap:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("#### 📸 Preprocessed Image")
                st.image(preprocessed_pil, use_container_width=True)
                st.caption("Input to the model")

            with col2:
                st.markdown("#### 🌡️ Activation Heatmap")
                st.image(heatmap, use_container_width=True)
                st.caption("Red = High activation, Blue = Low activation")
            
            with col3:
                st.markdown("#### 🎨 GradCAM++ Overlay")
                st.image(overlay, use_container_width=True)
                st.caption("Heatmap overlaid on preprocessed image")

        else:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📸 Preprocessed Image")
                st.image(preprocessed_pil, use_container_width=True)
                st.caption("Input to the model")

            with col2:
                st.markdown("#### 🎨 GradCAM++ Overlay")
                st.image(overlay, use_container_width=True)
                st.caption("Heatmap overlaid on preprocessed image")
            
            # with col2:
            #     st.markdown("#### 🌡️ Activation Heatmap")
            #     st.image(heatmap, use_container_width=True)
            #     st.caption("Red = High activation, Blue = Low activation")
        
        # Class-specific GradCAM
        if show_class_specific:
            st.markdown("---")
            st.markdown("#### 🎯 Class-Specific Activation Maps")
            st.markdown("See what the model looks for when predicting each cell type:")
            
            class_cols = st.columns(5)
            class_names = ['Dyskeratotic', 'Koilocytotic', 'Metaplastic', 'Parabasal', 'Superficial-Intermediate']
            
            for idx, class_name in enumerate(class_names):
                with class_cols[idx]:
                    with st.spinner(f"Generating {class_name}..."):
                        _, class_overlay = generate_gradcam(preprocessed_pil, model, class_name)
                    st.image(class_overlay, use_container_width=True)
                    st.caption(f"{class_name}")
                    prob_val = all_probs.get(class_name, 0)
                    st.caption(f"Prob: {prob_val:.1f}%")
        
        # Interpretation guide
        with st.expander("📖 How to Interpret GradCAM++ Results"):
            st.markdown("""
            ### Understanding the Visualization
            
            **Color Intensity:**
            - **Red/Yellow**: Regions with high importance for the prediction
            - **Green**: Moderate importance
            - **Blue/Purple**: Low importance
            
            ### What to Look For
            
            Each cell type has characteristic features:
            - **Dyskeratotic**: Abnormal keratinization patterns
            - **Koilocytotic**: HPV-related perinuclear halos
            - **Metaplastic**: Cell transformation indicators
            - **Parabasal**: Immature cell characteristics
            - **Superficial-Intermediate**: Normal mature cell features
            
            ### Model Confidence
            
            - **>90%**: High confidence - strong match to training data
            - **70-90%**: Good confidence - typical prediction
            - **50-70%**: Moderate confidence - may require review
            - **<50%**: Low confidence - uncertain classification
            """)
        
        # Download section
        st.markdown("---")
        st.markdown("### 💾 Download Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Preprocessed image already handled above
            pass
        
        with col2:
            # Save overlay as bytes for download
            overlay_pil = Image.fromarray(overlay)
            
            buf_overlay = BytesIO()
            overlay_pil.save(buf_overlay, format='PNG')
            
            st.download_button(
                label="📥 Download GradCAM++ Visualization",
                data=buf_overlay.getvalue(),
                file_name=f"gradcam_{pred_class}_{uploaded_file.name}",
                mime="image/png",
                use_container_width=True
            )
        
        with col3:
            # Create results JSON
            results_json = {
                "predicted_class": pred_class,
                "confidence": float(confidence),
                "probabilities": {k: float(v) for k, v in all_probs.items()},
                "preprocessing_metrics": {
                    "psnr_db": float(metrics['PSNR (dB)']),
                    "ssim": float(metrics['SSIM']),
                    "contrast_improvement": float(metrics['Contrast Improvement'])
                }
            }
            
            st.download_button(
                label="📥 Download Full Results (JSON)",
                data=str(results_json),
                file_name=f"results_{uploaded_file.name}.json",
                mime="application/json",
                use_container_width=True
            )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; padding: 1rem;">
        <p>CBAM-ResNet50 Cervical Cancer Cell Classifier | Powered by PyTorch & Streamlit</p>
        <p>⚠️ This tool is for research purposes only. Always consult medical professionals for diagnosis.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
