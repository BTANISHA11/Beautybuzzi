<div align="center">

# 💄 BeautyBuzzi

### AI-Powered Beauty & Grooming Platform for Everyone

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?logo=streamlit)](https://streamlit.io)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.6-orange?logo=pytorch)](https://pytorch.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.10%2B-green?logo=opencv)](https://opencv.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**BeautyBuzzi** is a full-featured AI beauty and grooming assistant built with **Streamlit** and **PyTorch**. It delivers virtual makeup try-on, AI skin analysis, personalised skincare routines, hairstyle recommendations, occasion-specific looks, curated product recommendations, and expert consultation booking — for **women, men, and non-binary users**. A FastAPI commerce backend layer is available for product offer integration with eBay.

</div>

---

## ✨ Features

### 💄 Virtual Makeup Try-On (`app.py`)
- Upload a face photo, capture a webcam snapshot, or use the built-in sample image
- **Gender-aware controls:**
  - *Women / Non-binary* — Lip colour, eyeshadow, blush, eyeliner, hair colour
  - *Men* — Beard tint, brow styling, hair colour
- MediaPipe landmark rendering with BiSeNet fallback
- Intensity slider for subtle-to-bold adjustments
- Smart look presets, compare slider, and saved-look session history
- Foundation shade matching with cheek tone sampling
- Side-by-side before / after comparison
- One-click **Download Result** as PNG

### 🔬 AI Skin Analysis (`pages/2_Skin_analysis.py`)
- Computer-vision heuristics analysing texture, tone and moisture from a photo
- **Skin Health Score** (0–100) with colour-coded badge
- Gender / Age Group / Lifestyle selectors for fully personalised output
- Upload or webcam snapshot analysis flow
- 5-tab report: **Analysis · Product Picks · Daily Routine · Tone Match · History**
- Age-aware recommendations (retinol intro at 36+, collagen focus at 46+)
- JSON skin report export, tone matching, and in-session progress tracking
- Lifestyle-specific advice: urban pollution, active/outdoor, dry/humid climate

### 💇 Hairstyle Recommendations (`pages/4_Hairstyles.py`)
- OpenCV Haar-cascade **face shape detection** (Oval, Round, Square, Heart, Oblong)
- Comprehensive style databases for **women** and **men** — keyed by face shape × preferred length × vibe
- Texture selector (Straight / Wavy / Curly / Coily / Fine)
- Hair care guide per texture, "styles to avoid" section, Trending 2025 styles
- Pro salon tips expander for each gender

### 🎭 Occasions (`pages/3_Occasions.py`)
- **9 occasions for women** with AI colour try-on (lip + hair overlay):
  Office, Wedding, Date Night, Birthday, Casual, Night Out, Festival, Graduation, Gym
- **8 grooming guides for men** with product lists, beard and skin-prep tips per occasion
- Occasion quick-reference grid
- Download the AI-applied look as PNG

### 🛒 Product Recommendations (`pages/5_Product_recommendations.py`)
- **Men's Grooming Guide**: skin-type matched products, beard care range, simple routine builder, age-aware additions
- **Women / Non-binary**: full product database across all 5 skin types
- Budget range slider ($0–$200), cruelty-free / vegan / fragrance-free filters
- Morning / Evening / Weekly treatment tabs
- Concern-specific sections (acne, wrinkles, dark spots, pores, sensitivity…)

### 🌿 Skincare Tips (`pages/skincare_tips.py`)
- **5 interactive tabs:**
  1. **Daily Routine** — AM + PM steps personalised by gender, age, and skin type
  2. **Ingredients Glossary** — 12 key ingredients explained (Retinol, Vit C, HA, Niacinamide, AHA/BHA, Peptides…)
  3. **Tips & Myths** — Expert tips + 7 common skincare myths debunked with science
  4. **Diet & Lifestyle** — Skin-boosting foods, hydration, sleep, exercise, what to avoid
  5. **Seasonal Guide** — Spring / Summer / Autumn / Winter skincare adjustments

### 📅 Consultations (`pages/6_Consultations.py`)
- Expert profile cards: Dermatologist, Men's Grooming Specialist, Makeup Artist, Trichologist
- Full booking form with **client-side validation** and booking confirmation summary
- Gender, age group, skin profile, and goals captured for expert preparation
- **7-question FAQ accordion**

---

## 🏗️ System Design

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      BeautyBuzzi App                         │
│               Streamlit Multi-Page Application               │
└───────────────────────┬──────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
 ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
 │  AI / ML    │  │  CV Layer   │  │  UI Layer   │
 │  Layer      │  │             │  │             │
 └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
        │                │                │
        ▼                ▼                ▼
 BiSeNet Face     MediaPipe /       Streamlit Pages
 Parsing Model    OpenCV CV Layer   + Custom CSS /
 (PyTorch)        Landmark Tracking Google Fonts
        │
        ▼
 ResNet-18 Backbone
 (ImageNet pretrained)
        │
        ▼
 FastAPI Commerce Backend (optional)
 eBay Browse API Integration
```

### Project Structure

```
beautybuzzi/
│
├── app.py                            # Main page — Virtual Makeup Try-On
│
├── pages/
│   ├── 1_About.py                    # App introduction & feature overview
│   ├── 2_Skin_analysis.py            # AI skin scoring & personalised routine
│   ├── 3_Occasions.py                # Occasion-based looks (AI try-on + grooming)
│   ├── 4_Hairstyles.py               # Face-shape detection + style database
│   ├── 5_Product_recommendations.py  # Gender-aware curated product guide
│   ├── 6_Consultations.py            # Expert booking form + FAQ
│   ├── Features.py                   # Feature showcase page
│   └── skincare_tips.py              # 5-tab skincare education hub
│
├── model.py                          # BiSeNet face parsing model definition
├── mediapipe_makeup.py               # Landmark-based LAB blending + tone matching
├── resnet.py                         # ResNet-18 backbone (feature encoder)
├── test.py                           # evaluate() — inference → segmentation mask
├── makeup.py                         # apply_makeup(), apply_region_blend()
├── recommend_hairstyle.py            # get_face_shape() helper
│
├── backend/
│   ├── commerce_api.py               # FastAPI eBay Browse API integration
│   ├── requirements.txt              # Backend dependencies
│   └── .env.example                  # eBay credentials template
│
├── services/
│   ├── product_catalog.py            # Product data normalization
│   └── product_offers.py             # Retailer offer lookup
│
├── static/
│   ├── constants.py                  # DEFAULT_IMAGE_PATH, TABLE (part index map)
│   └── styles.css                    # Shared CSS variables
│
├── cp/
│   └── 79999_iter.pth                # BiSeNet trained weights (face parsing)
│
├── imgs/                             # Sample input images
├── makeup/                           # Sample makeup output images
├── hairstyles/                       # Hairstyle reference images
│
└── requirements.txt                  # Dependency versions
```

### AI Pipeline — Makeup Try-On

```
User Photo (PIL Image / file path)
          │
          ▼
        MediaPipe Face Landmarker
          │
          ├─ precise lips / eyes / cheeks / jaw
          └─ fallback path if landmarks unavailable
          │
          ▼
        test.evaluate()
  ┌──────────────────────────────────────────┐
  │  1. Resize image → 512 × 512            │
  │  2. Normalise (ImageNet mean / std)      │
  │  3. BiSeNet forward pass (PyTorch)       │
  │     ├─ ResNet-18 encoder (context path)  │
  │     ├─ Spatial path (3-layer conv)       │
  │     ├─ Feature Fusion Module             │
  │     └─ Segmentation head (19 classes)   │
  │  4. argmax → pixel-level part mask      │
  └──────────────────────────────────────────┘
          │  parsing map  (H × W, int)
          ▼
    mediapipe_makeup.py / makeup.py
  ┌──────────────────────────────────────────┐
  │  1. Build region masks from landmarks    │
  │  2. Feather masks with Gaussian blur     │
  │  3. Blend in LAB space to preserve       │
  │     texture and luminance                │
  │  4. Use BiSeNet for hair segmentation    │
  └──────────────────────────────────────────┘
          │
          ▼
  Result image (NumPy → PIL → st.image / download)
```

### Face Part Index Map

| Index | Region     | Used For                |
|-------|------------|-------------------------|
| 1     | Skin/Face  | Foundation              |
| 12    | Upper Lip  | Lip colour              |
| 13    | Lower Lip  | Lip colour              |
| 14    | Eyeliner   | Liner effect            |
| 15    | Eyeshadow  | Eyeshadow blending      |
| 16    | Blush      | Cheek colour            |
| 17    | Hair       | Hair colour + sharpening|

---

## �️ Commerce Backend

A FastAPI commerce backend is included to fetch live product offers from eBay Browse API and provide them to the Streamlit app.

### Features
- ✅ eBay Browse API integration with OAuth credentials
- ✅ Product offer lookup with retailer search hints
- ✅ Mock fallback when API credentials missing or unavailable
- ✅ Product catalog normalization with stable SKUs
- ✅ Streamlit-compatible JSON responses

### Running the Backend Locally

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Copy environment template
cp backend/.env.example backend/.env

# Fill in your eBay credentials:
# EBAY_CLIENT_ID=your_client_id
# EBAY_CLIENT_SECRET=your_client_secret
# EBAY_MARKETPLACE_ID=EBAY_US (optional)

# Start the server
uvicorn backend.commerce_api:app --host 127.0.0.1 --port 8000 --reload
```

Available at **http://127.0.0.1:8000/offers**

### Streamlit Integration

Point your Streamlit app to the backend:
```
# .streamlit/secrets.toml
BEAUTYBUZZI_COMMERCE_API = "http://127.0.0.1:8000/offers"
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Streamlit Frontend** | Streamlit 1.35+, HTML/CSS, Google Fonts |
| **Commerce Backend** | FastAPI 0.115.2+, Uvicorn, Pydantic, eBay Browse API |
| **Deep Learning** | PyTorch 2.6, BiSeNet (face parsing), ResNet-18 backbone |
| **Computer Vision** | OpenCV 4.10+, MediaPipe face landmarks, LAB-space blending |
| **Image Processing** | Pillow 12+, NumPy 2+, scikit-image |
| **Data** | pandas 2+, Python dicts (product / style databases) |
| **Runtime** | Python 3.10–3.13, venv |

---

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.10 or higher
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/beautybuzzi.git
cd beautybuzzi

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

> **Note:** The BiSeNet weights (`cp/79999_iter.pth`) are included in the repo.  
> The ResNet-18 pretrained weights are downloaded automatically from the PyTorch model zoo on first run.

### Optional: Run Commerce Backend

```bash
# Install backend dependencies (in separate venv recommended)
pip install -r backend/requirements.txt

# Configure eBay credentials
cp backend/.env.example backend/.env
# Edit backend/.env with your EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_MARKETPLACE_ID

# Start the server
uvicorn backend.commerce_api:app --host 127.0.0.1 --port 8000 --reload
```

Then set `BEAUTYBUZZI_COMMERCE_API = "http://127.0.0.1:8000/offers"` in Streamlit secrets.

---

## 📦 Requirements

```
torch==2.6.0
torchvision==0.21.0
scikit-image==0.25.2
streamlit>=1.35.0
numpy>=2.0.0
opencv-python>=4.10.0
Pillow>=11.0.0
protobuf>=3.20.3
pandas>=2.0.0
setuptools>=65.0.0
mediapipe>=0.10.0
```

---

## 🗺️ Roadmap

### ✅ Implemented — Streamlit App
- [x] MediaPipe landmark-based try-on
- [x] Webcam snapshot input
- [x] LAB-space feathered makeup blending
- [x] Foundation shade matching via cheek tone detection
- [x] Session-based saved looks & skin progress history
- [x] Gender-aware makeup controls (women, men, non-binary)
- [x] AI skin analysis with personalised recommendations
- [x] Hairstyle recommendations based on face shape
- [x] Occasion-specific grooming guides
- [x] Skincare education hub with 5 interactive tabs
- [x] Expert consultation booking form

### ✅ Implemented — Commerce Backend
- [x] FastAPI commerce backend with eBay Browse API integration
- [x] Product offer lookup with mock fallback
- [x] Product catalog normalization with SKUs

### 🔮 Future Enhancements
- [ ] PostgreSQL / MongoDB persistent storage
- [ ] User authentication (JWT / OAuth)
- [ ] Full FastAPI backend (30+ endpoints for users, consultations, IoT)
- [ ] Next.js web frontend (7 pages)
- [ ] Mobile app (React Native)
- [ ] Real-time WebRTC streaming
- [ ] Payment integration (Stripe / Razorpay)
- [ ] Smart mirror IoT support
- [ ] Admin dashboard
- [ ] Multi-language support
- [ ] Advanced analytics & reporting

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit: `git commit -m 'Add my feature'`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [zllrunning/face-parsing.PyTorch](https://github.com/zllrunning/face-parsing.PyTorch) — BiSeNet face parsing model
- [Streamlit](https://streamlit.io) — UI framework
- [PyTorch](https://pytorch.org) — deep learning framework

---

<div align="center">
Made with ❤️ by the BeautyBuzzi team
</div>
