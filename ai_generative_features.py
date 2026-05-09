"""
🔥 PHASE 7: GENERATIVE AI FEATURES
AI Look Generator, Beauty Chatbot, Makeup Artist, Occasion Auto-Looks.
Uses: Gemini API, OpenAI API, LangChain, Diffusion Models.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import cv2
import json

class AIBeautyLookGenerator:
    """
    Generate complete makeup looks from natural language descriptions.
    "Soft glam bridal look for brown skin" → Full makeup recommendation.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize AI model for look generation."""
        self.api_key = api_key
        self.makeup_color_palette = {
            'warm_undertone': {
                'lipstick': ['coral', 'peach', 'warm_pink', 'terracotta', 'bronze'],
                'eyeshadow': ['bronze', 'gold', 'warm_brown', 'copper', 'champagne'],
                'blush': ['peach', 'warm_pink', 'terracotta']
            },
            'cool_undertone': {
                'lipstick': ['cool_pink', 'mauve', 'berry', 'plum', 'cool_red'],
                'eyeshadow': ['silver', 'cool_brown', 'plum', 'taupe', 'cool_pink'],
                'blush': ['cool_pink', 'berry', 'plum']
            },
            'neutral_undertone': {
                'lipstick': ['nude', 'rose', 'pink', 'coral', 'wine'],
                'eyeshadow': ['bronze', 'brown', 'taupe', 'champagne', 'silver'],
                'blush': ['rose', 'peach', 'pink']
            }
        }
        
        # Preset looks
        self.preset_looks = self._create_preset_looks()
    
    def generate_look(self, description: str, skin_tone: str, undertone: str) -> Dict:
        """
        Generate complete makeup look from description.
        
        Example input:
            description: "Soft glam bridal look"
            skin_tone: "medium"
            undertone: "warm"
        
        Returns:
            - Lipstick recommendation (color, finish, intensity)
            - Eyeshadow recommendation (colors, placement, technique)
            - Blush recommendation (color, placement, intensity)
            - Eyeliner recommendation
            - Overall look description
            - step-by-step application guide
        """
        
        # Step 1: Parse description with AI (or keyword matching)
        look_type = self._classify_look(description)
        intensity = self._classify_intensity(description)
        
        # Step 2: Generate tailored recommendations
        recommendations = self._generate_recommendations(
            look_type, intensity, skin_tone, undertone
        )
        
        # Step 3: Create application guide
        guide = self._create_application_guide(recommendations, look_type)
        
        return {
            'look_name': description,
            'look_type': look_type,
            'intensity': intensity,
            'recommendations': recommendations,
            'application_guide': guide,
            'preview_image': None  # Can be generated with diffusion model
        }
    
    def _classify_look(self, description: str) -> str:
        """Classify look type from natural language."""
        keywords = {
            'glam': ['glam', 'glamorous', 'dramatic', 'bold', 'evening'],
            'natural': ['natural', 'subtle', 'everyday', 'minimal', 'fresh'],
            'bridal': ['bridal', 'wedding', 'bride'],
            'party': ['party', 'night', 'clubbing', 'rave'],
            'professional': ['office', 'work', 'professional', 'business'],
            'artistic': ['artistic', 'creative', 'editorial', 'runway'],
            'smokey': ['smokey', 'smoke', 'dark', 'mysterious'],
            'colorful': ['colorful', 'vibrant', 'bold', 'neon']
        }
        
        desc_lower = description.lower()
        for look_type, keys in keywords.items():
            if any(k in desc_lower for k in keys):
                return look_type
        
        return 'natural'
    
    def _classify_intensity(self, description: str) -> float:
        """Classify makeup intensity (0.0-1.0) from description."""
        desc_lower = description.lower()
        
        if any(w in desc_lower for w in ['light', 'subtle', 'minimal', 'natural']):
            return 0.4
        elif any(w in desc_lower for w in ['bold', 'dramatic', 'heavy', 'glam']):
            return 0.9
        else:
            return 0.6
    
    def _generate_recommendations(self, look_type: str, intensity: float, skin_tone: str, undertone: str) -> Dict:
        """Generate specific color and technique recommendations."""
        
        palette = self.makeup_color_palette[f"{undertone}_undertone"]
        
        recommendations = {
            'lipstick': {
                'color': np.random.choice(palette['lipstick']),
                'finish': self._recommend_finish(look_type),
                'intensity': intensity
            },
            'eyeshadow': {
                'colors': self._recommend_eyeshadow_palette(look_type, palette),
                'placement': self._recommend_placement(look_type),
                'intensity': intensity,
                'technique': self._recommend_technique(look_type)
            },
            'blush': {
                'color': np.random.choice(palette['blush']),
                'placement': 'apples of cheeks' if intensity < 0.7 else 'high cheekbones',
                'intensity': intensity * 0.7
            },
            'eyeliner': {
                'enabled': intensity > 0.4,
                'style': self._recommend_eyeliner(look_type),
                'color': 'black' if intensity > 0.7 else 'brown',
                'intensity': intensity * 0.8
            },
            'overall': {
                'skin_prep': 'hydrating primer' if skin_tone in ['fair', 'light'] else 'silicone primer',
                'setting': 'powder setting spray' if intensity > 0.7 else 'light mist spray'
            }
        }
        
        return recommendations
    
    def _recommend_finish(self, look_type: str) -> str:
        """Recommend makeup finish based on look type."""
        finishes = {
            'glam': 'glossy',
            'natural': 'matte',
            'bridal': 'satin',
            'party': 'metallic',
            'professional': 'matte',
            'artistic': 'metallic',
            'smokey': 'matte',
            'colorful': 'shimmer'
        }
        return finishes.get(look_type, 'satin')
    
    def _recommend_eyeshadow_palette(self, look_type: str, palette: Dict) -> List[str]:
        """Recommend eyeshadow color palette."""
        palettes = {
            'glam': [palette['eyeshadow'][0], palette['eyeshadow'][1], 'black'],
            'natural': [palette['eyeshadow'][3], palette['eyeshadow'][4]],
            'bridal': [palette['eyeshadow'][4], palette['eyeshadow'][0]],
            'smokey': ['black', 'dark_gray', palette['eyeshadow'][2]],
            'colorful': [palette['eyeshadow'][0], palette['eyeshadow'][1], palette['eyeshadow'][2]]
        }
        return palettes.get(look_type, palette['eyeshadow'][:2])
    
    def _recommend_placement(self, look_type: str) -> str:
        """Recommend eyeshadow placement."""
        return 'halo' if look_type == 'glam' else 'gradient' if look_type == 'bridal' else 'standard'
    
    def _recommend_technique(self, look_type: str) -> str:
        """Recommend application technique."""
        techniques = {
            'glam': 'blending with wet brush',
            'natural': 'tapping with fingertips',
            'bridal': 'precise gradient blending',
            'smokey': 'diffused blending',
            'artistic': 'layering and blending'
        }
        return techniques.get(look_type, 'standard blending')
    
    def _recommend_eyeliner(self, look_type: str) -> str:
        """Recommend eyeliner style."""
        styles = {
            'glam': 'winged liner',
            'natural': 'tight lining',
            'bridal': 'subtle kitten liner',
            'party': 'graphic liner',
            'smokey': 'smudged liner'
        }
        return styles.get(look_type, 'classic liner')
    
    def _create_application_guide(self, recommendations: Dict, look_type: str) -> List[str]:
        """Create step-by-step application guide."""
        guide = [
            "1. 🎨 PREP: Apply primer and foundation",
            "2. 👁️ EYES: Apply eyeshadow base",
            f"3. 🎯 EYESHADOW: {recommendations['eyeshadow']['technique'].title()}",
            f"4. ✏️ EYELINER: Apply {recommendations['eyeliner']['style']}",
            f"5. 🎀 BLUSH: Apply to {recommendations['blush']['placement']}",
            f"6. 💄 LIPSTICK: Apply {recommendations['lipstick']['color']} in {recommendations['lipstick']['finish']}",
            "7. ✨ SETTING: Use setting spray for longevity"
        ]
        return guide
    
    def _create_preset_looks(self) -> Dict:
        """Create preset looks for quick access."""
        return {
            'everyday_natural': {
                'description': 'Fresh, minimal makeup for daily wear',
                'lipstick': {'color': 'nude', 'intensity': 0.4, 'finish': 'matte'},
                'eyeshadow': {'colors': ['bronze', 'champagne'], 'intensity': 0.3},
                'blush': {'color': 'peach', 'intensity': 0.3}
            },
            'date_night': {
                'description': 'Warm, flirty look for casual dates',
                'lipstick': {'color': 'warm_pink', 'intensity': 0.7, 'finish': 'satin'},
                'eyeshadow': {'colors': ['gold', 'bronze'], 'intensity': 0.6},
                'blush': {'color': 'peach', 'intensity': 0.5}
            },
            'dramatic_evening': {
                'description': 'Bold, glamorous evening makeup',
                'lipstick': {'color': 'wine', 'intensity': 0.9, 'finish': 'glossy'},
                'eyeshadow': {'colors': ['black', 'gold', 'champagne'], 'intensity': 0.9},
                'blush': {'color': 'berry', 'intensity': 0.6}
            }
        }


class AIBeautyChatbot:
    """
    AI-powered beauty chatbot for skincare Q&A, routine planning, ingredient checking.
    Integrates: Gemini API, OpenAI API, LangChain for RAG.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize chatbot with knowledge base."""
        self.api_key = api_key
        self.knowledge_base = self._create_knowledge_base()
        self.conversation_history = []
    
    def _create_knowledge_base(self) -> Dict:
        """Create knowledge base for Q&A."""
        return {
            'ingredients': {
                'retinol': {
                    'benefits': ['reduces wrinkles', 'improves texture', 'brightens skin'],
                    'concentration': '0.25%-1%',
                    'best_for': ['aging skin', 'acne scars', 'dull skin'],
                    'warning': 'Can cause irritation; start low and slow'
                },
                'hyaluronic_acid': {
                    'benefits': ['hydrates', 'plumps skin', 'holds moisture'],
                    'concentration': '0.5%-2%',
                    'best_for': ['dry skin', 'dehydrated skin'],
                    'warning': 'Apply to damp skin for best absorption'
                },
                'vitamin_c': {
                    'benefits': ['brightens', 'antioxidant', 'collagen boosting'],
                    'concentration': '10%-20%',
                    'best_for': ['dull skin', 'dark spots', 'aging'],
                    'warning': 'Unstable; use stabilized forms'
                },
                'niacinamide': {
                    'benefits': ['regulates oil', 'reduces pores', 'calms skin'],
                    'concentration': '4%-5%',
                    'best_for': ['oily skin', 'acne-prone', 'rosacea'],
                    'warning': 'Generally safe for all skin types'
                },
                'salicylic_acid': {
                    'benefits': ['exfoliates', 'unclogs pores', 'reduces acne'],
                    'concentration': '0.5%-2%',
                    'best_for': ['acne', 'oily skin', 'congestion'],
                    'warning': 'Can cause dryness; use with moisturizer'
                }
            },
            'routines': {
                'morning': [
                    'Cleanser',
                    'Toner',
                    'Serum (Vitamin C / Niacinamide)',
                    'Moisturizer',
                    'SPF 50+ Sunscreen'
                ],
                'evening': [
                    'Cleanser',
                    'Toner',
                    'Serum (Retinol / Hyaluronic Acid)',
                    'Moisturizer',
                    'Eye Cream'
                ]
            },
            'conditions': {
                'acne': {
                    'cause': 'Bacteria, clogged pores, inflammation',
                    'treatment': ['Salicylic acid', 'Benzoyl peroxide', 'Niacinamide', 'Retinol'],
                    'avoid': ['Heavy oils', 'Occlusive sunscreens', 'Touching face']
                },
                'dry_skin': {
                    'cause': 'Lack of moisture, damaged barrier',
                    'treatment': ['Hyaluronic acid', 'Ceramides', 'Oils', 'Rich moisturizers'],
                    'avoid': ['Over-exfoliation', 'Hot water', 'Harsh cleansers']
                },
                'dark_circles': {
                    'cause': 'Poor sleep, genetics, thin skin',
                    'treatment': ['Caffeine serum', 'Retinol', 'Vitamin K', 'Cold compress'],
                    'avoid': ['Screen time before bed', 'Salt intake', 'Lack of sleep']
                }
            }
        }
    
    def answer_question(self, question: str) -> str:
        """Answer beauty-related questions."""
        # Add to history
        self.conversation_history.append({'user': question})
        
        # Simple keyword-based responses (can be enhanced with LLM)
        question_lower = question.lower()
        
        if 'acne' in question_lower:
            response = self._answer_acne_question(question)
        elif 'ingredient' in question_lower:
            response = self._answer_ingredient_question(question)
        elif 'routine' in question_lower:
            response = self._answer_routine_question(question)
        elif 'dark circle' in question_lower or 'dark spot' in question_lower:
            response = self._answer_dark_concern_question(question)
        else:
            response = "🤔 I'm not sure, but I can help! Ask me about ingredients, routines, acne, or skincare concerns."
        
        # Add to history
        self.conversation_history.append({'assistant': response})
        
        return response
    
    def _answer_acne_question(self, question: str) -> str:
        """Answer acne-related questions."""
        kb = self.knowledge_base['conditions']['acne']
        return f"""
🔴 **About Acne**
**Causes:** {kb['cause']}
**Recommended Treatments:** {', '.join(kb['treatment'])}
**Avoid:** {', '.join(kb['avoid'])}

💡 Pro tip: Use salicylic acid (BHA) for exfoliation and niacinamide to calm inflammation.
        """
    
    def _answer_ingredient_question(self, question: str) -> str:
        """Answer ingredient-related questions."""
        # Check which ingredient is asked about
        for ingredient, info in self.knowledge_base['ingredients'].items():
            if ingredient.replace('_', ' ') in question.lower():
                return f"""
✨ **{ingredient.replace('_', ' ').title()}**
**Benefits:** {', '.join(info['benefits'])}
**Concentration:** {info['concentration']}
**Best For:** {', '.join(info['best_for'])}
**⚠️ Warning:** {info['warning']}
                """
        
        return "I don't have info on that ingredient, but I know about: Retinol, Hyaluronic Acid, Vitamin C, Niacinamide, Salicylic Acid."
    
    def _answer_routine_question(self, question: str) -> str:
        """Answer routine-related questions."""
        kb = self.knowledge_base['routines']
        
        routine_type = 'evening' if 'night' in question.lower() or 'evening' in question.lower() else 'morning'
        routine = kb[routine_type]
        
        return f"""
✨ **{routine_type.title()} Routine**
{chr(10).join([f'{i+1}. {step}' for i, step in enumerate(routine)])}

💡 Wait 1-2 minutes between products for absorption.
        """
    
    def _answer_dark_concern_question(self, question: str) -> str:
        """Answer dark circles/spots questions."""
        kb = self.knowledge_base['conditions']['dark_circles']
        return f"""
🌙 **About Dark Circles**
**Causes:** {kb['cause']}
**Treatments:** {', '.join(kb['treatment'])}
**Prevent:** {', '.join(kb['avoid'])}

💡 Pro tip: Use caffeine serum in morning and retinol at night for best results.
        """
    
    def suggest_routine(self, skin_type: str, concerns: List[str]) -> List[str]:
        """Suggest personalized routine based on skin type and concerns."""
        routine = []
        
        if skin_type == 'dry':
            routine = [
                'Gentle cream cleanser',
                'Hydrating toner',
                'Hyaluronic acid serum',
                'Rich moisturizer',
                'SPF 50+ sunscreen'
            ]
        elif skin_type == 'oily':
            routine = [
                'Foaming cleanser',
                'Balancing toner',
                'Niacinamide serum',
                'Lightweight moisturizer',
                'Mattifying SPF sunscreen'
            ]
        else:  # Combination/Normal
            routine = [
                'Balanced cleanser',
                'Toning essence',
                'Vitamin C serum',
                'Lightweight moisturizer',
                'SPF 50+ sunscreen'
            ]
        
        # Add concern-specific products
        for concern in concerns:
            if 'acne' in concern.lower():
                routine.insert(2, 'Salicylic acid (2-3x/week)')
            if 'aging' in concern.lower():
                routine.append('Retinol (evening)')
            if 'dark spot' in concern.lower():
                routine.insert(2, 'Vitamin C serum')
        
        return routine


if __name__ == "__main__":
    look_gen = AIBeautyLookGenerator()
    chatbot = AIBeautyChatbot()
    
    print("✅ AI Beauty Features loaded")
    print("\n📌 Look Generator example:")
    look = look_gen.generate_look("soft glam bridal look", "medium", "warm")
    print(f"Look: {look['look_name']}")
    print(f"Guide: {look['application_guide'][0]}")
    
    print("\n💬 Chatbot example:")
    print(chatbot.answer_question("What's the best ingredient for acne?"))
