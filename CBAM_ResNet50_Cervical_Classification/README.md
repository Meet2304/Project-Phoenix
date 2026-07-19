# CBAM-ResNet50 Cervical Cancer Cell Classifier

🔬 **Complete Pipeline**: Raw Image → Preprocessing → Classification → Explainability

## Features

- **Advanced Model Architecture**: CBAM-ResNet50 with Channel & Spatial Attention
- **Preprocessing Pipeline**: Resize → NLM Denoising → CLAHE Enhancement
- **Explainable AI**: GradCAM++ visualization
- **Interactive Dashboard**: Built with Streamlit
- **High Performance**: 94.32% accuracy on test set

## Cell Types Classified

1. Dyskeratotic
2. Koilocytotic
3. Metaplastic
4. Parabasal
5. Superficial-Intermediate

## Quick Start

### Local Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd CBAM_ResNet50_Cervical_Classification

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Streamlit Cloud Deployment

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository
5. Set main file path: `CBAM_ResNet50_Cervical_Classification/app.py`
6. Click "Deploy"

**Important**: Ensure these files are in your repository:
- `cbam_resnet50_cervical/best_model.pth` (trained model)
- `sample_image/original_images/` (sample images)
- `requirements.txt`
- `packages.txt`
- `.streamlit/config.toml`

## Usage

### Upload Image
1. Use the sidebar to upload a cervical cell microscopy image
2. Supported formats: BMP, PNG, JPG, JPEG

### Use Sample Images
1. Select "Use Sample Images" in the sidebar
2. Choose from pre-loaded sample images
3. View instant results

### View Results
- **Step 1**: Image preprocessing visualization
- **Step 2**: Classification results with confidence scores
- **Step 3**: GradCAM++ explainability heatmaps

### Download Results
- Preprocessed image
- GradCAM++ visualization
- Complete results (JSON)

## Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 94.32% |
| Precision | 94.40% |
| Recall | 94.32% |
| F1-Score | 94.34% |

## Technical Details

- **Parameters**: 24,214,989
- **Training Dataset**: 4,049 images (3,239 train / 405 val / 405 test)
- **Preprocessing**: NLM (h=3), CLAHE (clipLimit=1.2)
- **Input Size**: 224×224
- **Framework**: PyTorch

## Dependencies

- Python >= 3.8
- PyTorch >= 2.0.0
- Streamlit >= 1.28.0
- OpenCV (headless for deployment)
- scikit-image
- plotly

## Notes

⚠️ **Disclaimer**: This tool is for research purposes only. Always consult medical professionals for diagnosis.

## License

This project is for educational and research purposes.
