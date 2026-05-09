# BeautyBuzzi Production Architecture

## Purpose

This document defines the target architecture for the roadmap items that do not fit the current Streamlit application shape, especially:

- true real-time video try-on
- WebRTC streaming
- browser-side inference
- persistent user profiles and saved looks
- e-commerce and social features
- multi-service AI deployment

## Current State

The current repository is now a stronger prototype with:

- MediaPipe landmark-based makeup rendering
- LAB-space feathered blending
- webcam snapshot input
- foundation shade matching
- skin analysis history
- session-based saved looks

That is the practical limit of the current Streamlit-first architecture.

## Target Architecture

```text
Next.js Frontend
  |
  +-- WebRTC Camera Pipeline
  +-- MediaPipe Face Tracking
  +-- ONNX Runtime Web / TensorFlow.js
  +-- Smart Mirror UI
  |
  v
API Gateway
  |
  +-- Auth Service
  +-- User Profile Service
  +-- Saved Looks Service
  +-- Product Catalog Service
  +-- Recommendation Service
  +-- Consultation Booking Service
  |
  v
AI Services
  |
  +-- Face Landmark Service
  +-- Makeup Rendering Service
  +-- Skin Analysis Service
  +-- Hair Simulation Service
  +-- Foundation Match Service
  +-- Beauty Copilot / LLM Service
  |
  v
Model Runtime Layer
  |
  +-- PyTorch
  +-- ONNX Runtime
  +-- TensorRT
  +-- TorchServe / custom FastAPI inference workers
  |
  v
Data Layer
  |
  +-- PostgreSQL
  +-- Redis
  +-- Blob Storage
  +-- Analytics Warehouse
```

## Service Boundaries

### Frontend

- Next.js app router
- Tailwind UI system
- WebRTC webcam streaming
- compare slider, smart mirror, shade wheel, fullscreen try-on
- account pages, saved looks, consultation dashboard, shop-this-look UI

### Backend API

- FastAPI for typed APIs and async workloads
- JWT auth and user profile APIs
- booking APIs for consultations
- recommendation orchestration
- product and look persistence

### Real-Time Rendering Service

- accepts landmarks or mesh stream
- applies makeup layers with texture-preserving blending
- handles temporal smoothing for video frames
- returns frame overlays or blend coefficients

### Skin Analysis Service

- image ingestion and normalization
- model inference for acne, pores, pigmentation, wrinkles, redness, hydration
- longitudinal progress scoring
- user report generation

### Recommendation Service

- undertone detection
- foundation and complexion product ranking
- product filtering by skin concerns, budget, allergens, finish, weather
- occasion-aware and profile-aware look generation

### Beauty Copilot Service

- LLM-backed Q&A
- ingredient explanation
- routine generation
- outfit-to-look suggestions
- safe prompt handling and cosmetic-policy rules

## Phase Mapping

### Phase 1 to 3: Real-Time AR

- frontend: WebRTC + MediaPipe tasks
- inference: temporal smoothing layer
- rendering: GPU-friendly mask generation + alpha blend compositor
- optional: 3D geometry via MediaPipe face geometry or ARKit/ARCore equivalents

### Phase 4 to 5: Skin Intelligence

- EfficientNet or MobileNetV3 classifiers for skin concerns
- cheek sampling plus illumination correction for tone matching
- longitudinal score store per user
- time-series charts and consultation escalation triggers

### Phase 6 to 7: Hair + Generative AI

- MODNet / DeepLabV3 hair segmentation
- hairstyle transfer or diffusion pipeline as asynchronous job
- LLM-driven look planning built on structured presets and safety filters

### Phase 8 to 10: Production Runtime

- Next.js frontend
- FastAPI microservices
- ONNX export for low-latency inference
- TensorRT for GPU deployment
- ONNX Runtime Web for browser-side experiments

### Phase 11 to 15: Product Features

- smart mirror mode
- persistent saved looks and user beauty profile
- product shopping integration
- social exports and community looks
- salon and brand dashboards

## Suggested Data Model

### users

- id
- email
- display_name
- skin_type
- undertone
- allergies
- preferences_json
- created_at

### saved_looks

- id
- user_id
- source_image_url
- output_image_url
- preset_name
- engine_name
- intensity
- metadata_json
- created_at

### skin_reports

- id
- user_id
- source_image_url
- score
- acne
- oiliness
- dryness
- sensitivity
- pigmentation
- wrinkles
- hydration
- report_json
- created_at

### consultations

- id
- user_id
- expert_type
- booking_time
- status
- notes
- intake_json
- created_at

## Deployment Path

### Prototype+

- keep Streamlit for demos
- export model utilities into reusable Python modules
- add ONNX export scripts

### Beta

- build Next.js frontend
- move AI routes to FastAPI
- deploy inference workers on GPU instances
- introduce PostgreSQL and Redis

### Production

- CDN + edge caching
- autoscaled inference workers
- object storage for media
- analytics pipeline
- observability with tracing, metrics, alerting

## What Should Stay in This Repo

- core blending logic
- face-region definitions
- tone matching heuristics
- prototype UX flows
- evaluation utilities for visual quality

## What Should Move Out

- long-running real-time rendering
- user accounts and persistent media storage
- product catalog and commerce logic
- video pipeline orchestration
- LLM-backed assistant APIs

## Recommended Next Build Order

1. Extract reusable beauty-engine Python package from current Streamlit code.
2. Add ONNX export and model benchmark scripts.
3. Create a Next.js webcam proof of concept with MediaPipe tracking.
4. Build FastAPI inference endpoints for skin analysis and preset generation.
5. Add persistent saved looks and user beauty profiles.
6. Add product recommendation and consultation APIs.