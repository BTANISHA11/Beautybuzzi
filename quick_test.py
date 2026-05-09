"""
🧪 QUICK VALIDATION TEST - SIMPLIFIED
Tests essential features only.
"""

import sys
import os

print("\n" + "="*70)
print("🧪 BEAUTYBUZZI QUICK VALIDATION")
print("="*70 + "\n")

# Test 1: Core module imports
print("✅ TEST 1: Core Module Imports")
print("-"*70)

test_results = []

try:
    from skin_analysis_v2 import DermatologyGradeSkinAnalyzer
    analyzer = DermatologyGradeSkinAnalyzer()
    print("✅ skin_analysis_v2.DermatologyGradeSkinAnalyzer")
    test_results.append(True)
except Exception as e:
    print(f"❌ skin_analysis_v2: {str(e)[:60]}")
    test_results.append(False)

try:
    from foundation_matcher import AIFoundationMatcher
    matcher = AIFoundationMatcher()
    print("✅ foundation_matcher.AIFoundationMatcher")
    test_results.append(True)
except Exception as e:
    print(f"❌ foundation_matcher: {str(e)[:60]}")
    test_results.append(False)

try:
    from ai_generative_features import AIBeautyLookGenerator, AIBeautyChatbot
    look_gen = AIBeautyLookGenerator()
    chatbot = AIBeautyChatbot()
    print("✅ ai_generative_features.AIBeautyLookGenerator")
    print("✅ ai_generative_features.AIBeautyChatbot")
    test_results.append(True)
    test_results.append(True)
except Exception as e:
    print(f"❌ ai_generative_features: {str(e)[:60]}")
    test_results.append(False)
    test_results.append(False)

try:
    from realtime_ar import RealtimeARPipeline
    ar = RealtimeARPipeline()
    print("✅ realtime_ar.RealtimeARPipeline")
    test_results.append(True)
except Exception as e:
    print(f"❌ realtime_ar: {str(e)[:60]}")
    test_results.append(False)

try:
    from rendering_engine import ProfessionalRenderingEngine
    renderer = ProfessionalRenderingEngine()
    print("✅ rendering_engine.ProfessionalRenderingEngine")
    test_results.append(True)
except Exception as e:
    print(f"❌ rendering_engine: {str(e)[:60]}")
    test_results.append(False)

try:
    from face_3d_tracker import Face3DTracker
    tracker = Face3DTracker()
    print("✅ face_3d_tracker.Face3DTracker")
    test_results.append(True)
except Exception as e:
    print(f"❌ face_3d_tracker: {str(e)[:60]}")
    test_results.append(False)

# Test 2: Basic method functionality
print("\n✅ TEST 2: Key Features")
print("-"*70)

try:
    analyzer = DermatologyGradeSkinAnalyzer()
    metrics = len(analyzer.analysis_metrics)
    print(f"✅ Skin Analyzer: {metrics} metrics")
    test_results.append(True)
except:
    test_results.append(False)

try:
    matcher = AIFoundationMatcher()
    shades = len(matcher.foundation_database)
    print(f"✅ Foundation Matcher: {shades} shades in DB")
    test_results.append(True)
except:
    test_results.append(False)

try:
    look_gen = AIBeautyLookGenerator()
    presets = len(look_gen.preset_looks)
    print(f"✅ Look Generator: {presets} preset looks")
    test_results.append(True)
except:
    test_results.append(False)

try:
    chatbot = AIBeautyChatbot()
    categories = len(chatbot.knowledge_base)
    print(f"✅ Chatbot: {categories} knowledge categories")
    test_results.append(True)
except:
    test_results.append(False)

# Test 3: Pages exist
print("\n✅ TEST 3: Streamlit Pages")
print("-"*70)

pages = [
    'pages/0_AR_Makeup.py',
    'pages/5_Foundation_Match.py',
    'pages/7_AI_Assistant.py'
]

for page in pages:
    if os.path.exists(page):
        print(f"✅ {page}")
        test_results.append(True)
    else:
        print(f"❌ {page} NOT FOUND")
        test_results.append(False)

# SUMMARY
print("\n" + "="*70)
print("📊 SUMMARY")
print("="*70)

passed = sum(test_results)
total = len(test_results)
pct = (passed/total*100) if total > 0 else 0

print(f"\n✅ Passed: {passed}/{total} ({pct:.0f}%)\n")

if pct == 100:
    print("🎉 ALL TESTS PASSED! System ready.\n")
elif pct >= 80:
    print("✅ MOSTLY WORKING! Minor issues only.\n")
else:
    print("⚠️  Some modules need fixing.\n")

print("="*70)
