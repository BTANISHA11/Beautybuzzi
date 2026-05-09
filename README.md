<div align="center">

# 💄 BeautyBuzzi

### AI-Powered Beauty & Grooming Platform for Everyone

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?logo=streamlit)](https://streamlit.io)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.6-orange?logo=pytorch)](https://pytorch.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.10%2B-green?logo=opencv)](https://opencv.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**BeautyBuzzi** is a comprehensive, production-grade AI beauty and grooming platform built with **Streamlit (frontend) + FastAPI (backend) + Next.js (web)**. It delivers virtual makeup try-on, AI skin analysis, personalised skincare routines, hairstyle recommendations, occasion-specific looks, curated product recommendations, expert consultation booking, user profile management, shopping integration, and smart device orchestration — for **women, men, and non-binary users**.

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
┌──────────────────────────────────────────────────────────────────────────┐
│                         BeautyBuzzi Platform                             │
│     (Streamlit App + FastAPI Backend + Next.js Web Commerce)            │
└──────────────┬──────────────────────┬─────────────────────┬─────────────┘
               │                      │                     │
      ┌────────▼────────┐  ┌─────────▼──────────┐  ┌───────▼──────────┐
      │  Streamlit      │  │  FastAPI Backend   │  │  Next.js Web     │
      │  Frontend       │  │  (30+ endpoints)   │  │  (7 pages)       │
      └────────┬────────┘  └─────────┬──────────┘  └───────┬──────────┘
               │                     │                      │
      ┌────────▼─────────────────────▼──────────────────────▼────────┐
      │                                                               │
      │   AI/ML Layer      │   CV Layer        │   Data Layer        │
      │  ─────────────────────────────────────────────────────       │
      │  BiSeNet Face     │ MediaPipe / CV    │ User Profiles       │
      │  Parsing (PyTorch)│ Landmark Track    │ Product DB          │
      │  ResNet-18        │ OpenCV            │ Consultations       │
      │  (ImageNet)       │ LAB-space blend   │ IoT Devices         │
      └──────────────────┴───────────────────┴─────────────────────┘
        │
        ▼
 ResNet-18 Backbone
 (ImageNet pretrained)
```

### Project Structure

```
beautybuzzi/
│
├── ★ STREAMLIT APP (Main UI)
│   ├── app.py                            # Main page — Virtual Makeup Try-On
│   ├── pages/
│   │   ├── 1_About.py
│   │   ├── 2_Skin_analysis.py            # Webcam, JSON export, history
│   │   ├── 3_Occasions.py
│   │   ├── 4_Hairstyles.py
│   │   ├── 5_Product_recommendations.py
│   │   ├── 6_Consultations.py
│   │   ├── Features.py
│   │   └── skincare_tips.py
│   └── requirements.txt
│
├── ★ AI/ML LAYER
│   ├── model.py                          # BiSeNet face parsing
│   ├── mediapipe_makeup.py               # MediaPipe landmarks + LAB blending
│   ├── resnet.py                         # ResNet-18 backbone
│   ├── test.py                           # evaluate() → segmentation
│   ├── makeup.py                         # apply_makeup() functions
│   └── recommend_hairstyle.py
│
├── ★ PRODUCTION BACKEND (FastAPI)
│   └── backend/
│       ├── commerce_api.py               # eBay Browse API integration
│       ├── requirements.txt              # Backend dependencies
│       └── app/ (30+ endpoints)
│           ├── main.py                   # FastAPI app (products, users, IoT, consultations)
│           ├── services/
│           │   ├── product_service.py    # Product recommendations
│           │   └── user_service.py       # User profiles, history, consultations
│           └── schemas.py                # 20+ Pydantic models
│
├── ★ PRODUCTION FRONTEND (Next.js)
│   └── frontend/
│       └── app/
│           ├── page.tsx                  # Overview/Home
│           ├── products/page.tsx         # Product shop + filtering
│           ├── dashboard/page.tsx        # User profile & history
│           ├── consultations/page.tsx    # Expert booking
│           ├── iot/page.tsx              # Smart device manager
│           ├── layout.tsx                # Navigation
│           └── ... (7 total pages)
│
├── static/
│   ├── constants.py
│   └── styles.css
│
├── cp/
│   └── 79999_iter.pth                # BiSeNet weights
│
├── imgs/, makeup/, hairstyles/       # Sample assets
│
├── services/                         # Commerce & utilities
│   ├── product_catalog.py
│   └── product_offers.py
│
└── PRODUCTION_ARCHITECTURE.md        # Full design docs
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

## 🏛️ Three-Tier Architecture

BeautyBuzzi operates as an integrated multi-tier platform:

### **Tier 1: Streamlit Desktop App** (Primary User Interface)
- Real-time makeup try-on with MediaPipe landmarks
- AI skin analysis with detailed reporting
- Hairstyle recommendations based on face shape
- Occasion-specific grooming guides
- Educational skincare resources
- **Deployment:** Local or Streamlit Cloud
- **Best for:** Desktop users, real-time interactive features, quick analysis

### **Tier 2: FastAPI Backend** (Unified Data & Commerce Layer)
- 30+ REST endpoints for products, users, consultations, IoT
- Manages user profiles, skin analysis history, consultation bookings
- Integrates with eBay Browse API for live product data
- Handles IoT device registration and smart mirror commands
- Persistent data layer (ready for database integration)
- **Port:** 8000 | **Docs:** http://localhost:8000/docs
- **Best for:** Backend operations, API-driven features, cross-platform access

### **Tier 3: Next.js Web App** (Modern Web Frontend)
- 7 fully-featured pages (products, dashboard, consultations, IoT, etc.)
- User profile management with skin history visualization
- Product shopping with multi-platform retailer links
- Expert consultation booking system
- IoT device management for smart mirrors and lights
- Responsive design for mobile and desktop
- **Port:** 3000 | **Framework:** Next.js 14 App Router
- **Best for:** Web users, mobile browsers, e-commerce flows, IoT management

### **Data Flow**
```
Streamlit App ←→ FastAPI Backend ←→ Database (future: PostgreSQL/MongoDB)
                      ↓
                 eBay Browse API
                      ↓
                 Product Data

Next.js Web ←→ FastAPI Backend ←→ User Profiles & Sessions
                      ↓
                 IoT Devices
                 Smart Mirrors
```

### **Why Three Tiers?**
- **Separation of Concerns:** UI, business logic, and data are decoupled
- **Scalability:** Each tier can scale independently
- **Flexibility:** Users can interact via Streamlit (desktop), Web (mobile), or API (mobile apps, integrations)
- **Production Ready:** Backend & frontend scaffold support enterprise deployment
- **Commerce Integration:** Unified product catalog and shopping across all UIs

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Streamlit Frontend** | Streamlit 1.35+, HTML/CSS, Google Fonts |
| **REST API / Backend** | FastAPI 0.115.2, Uvicorn 0.31.1, Pydantic 2.9.2, eBay Browse API |
| **Web Frontend** | Next.js 14.2.15, React 18.3.1, TypeScript 5.6.3, responsive grid |
| **Deep Learning** | PyTorch 2.6, BiSeNet (face parsing), ResNet-18 backbone |
| **Computer Vision** | OpenCV 4.10+, MediaPipe face landmarks, LAB-space blending |
| **Image Processing** | Pillow 12+, NumPy 2+, scikit-image |
| **Data** | pandas 2+, UUID-based user/session IDs, in-memory storage |
| **Runtime** | Python 3.10„3.13, Node.js 18+, venv / npm |

---

## 🏗️ Production Scaffold (Backend + Frontend)

A full production-grade architecture has been built on top of the core Streamlit app:

### Backend (FastAPI)
**30+ API endpoints** for:
- **Products** — Recommendations, category browsing, trending items, shopping links (Sephora, Amazon, Ulta, Nykaa)
- **User Management** — Profile CRUD, skin analysis history, gender-aware suggestions
- **Consultations** — 4 expert specialists (dermatologist, makeup artist, grooming expert, Ayurveda), booking & scheduling
- **IoT Devices** — Smart mirror, lights, AR glasses registration and command execution
- **Commerce API** — eBay Browse API integration with mock fallback

### Frontend (Next.js App Router)
**7 fully functional pages**:
- **Overview** — Feature showcase
- **Try-On** — Direct makeup try-on link
- **Skin** — AI analysis interface
- **Shop** — Product recommendations with filters (concern, skin tone, budget, eco-friendly)
- **Dashboard** — User profile creation, skin history tracking, trend visualization
- **Consultations** — Expert browsing, date/time booking, confirmation
- **IoT Devices** — Register smart mirrors/lights/AR glasses, start sessions, send commands

### Features
- ✅ UUID-based user & session management
- ✅ Persistent consultation bookings
- ✅ Real-time IoT device command execution
- ✅ Multi-platform shopping (Sephora, Amazon, Ulta, Nykaa, brand sites)
- ✅ Gender-aware & skin-tone inclusive recommendations
- ✅ Auto-generated Swagger API docs
- ✅ CORS-enabled for local development
- ✅ Form validation on both frontend & backend

### Running the Full Stack Locally

#### 1. Streamlit App (Port 8501)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```
Opens at **http://localhost:8501**

#### 2. FastAPI Backend (Port 8000)
```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Start the server
uvicorn backend.commerce_api:app --host 127.0.0.1 --port 8000 --reload
```
API docs available at **http://localhost:8000/docs** (Swagger UI)

#### 3. Next.js Web Frontend (Port 3000)
```bash
cd frontend
npm install
npm run dev
```
Opens at **http://localhost:3000**

### Environment Variables

**Streamlit** (`.streamlit/secrets.toml` or environment):
- `BEAUTYBUZZI_COMMERCE_API`: Backend URL, e.g., `http://127.0.0.1:8000/offers`

**Backend** (`backend/.env`):
- `EBAY_CLIENT_ID`: eBay OAuth client ID
- `EBAY_CLIENT_SECRET`: eBay OAuth client secret
- `EBAY_MARKETPLACE_ID`: Marketplace selector (e.g., `EBAY_US`)

> **Note:** Streamlit and FastAPI use different `starlette` versions. Keep them in separate virtual environments or use `conda` to manage compatibility.

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

### ✅ Implemented — Production Scaffold (Backend + Frontend)
- [x] FastAPI backend with 30+ REST endpoints
- [x] Next.js web application (7 pages)
- [x] User profile management & skin history tracking
- [x] Expert consultation booking system
- [x] IoT device registration & smart mirror support
- [x] Multi-platform product shopping (Sephora, Amazon, Ulta, Nykaa)
- [x] eBay Browse API integration with fallback
- [x] Swagger API documentation
- [x] UUID-based session management
- [x] CORS-enabled for local development

### 🔮 Future Enhancements
- [ ] PostgreSQL / MongoDB persistent storage
- [ ] User authentication (JWT / OAuth)
- [ ] Payment integration (Stripe / Razorpay)
- [ ] Real-time WebRTC streaming
- [ ] WebSocket for live mirror sessions
- [ ] Browser-side ML inference (ONNX.js)
- [ ] AWS IoT Core integration
- [ ] Mobile app (React Native)
- [ ] Analytics & reporting dashboard
- [ ] Admin panel
- [ ] Multi-language support

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
