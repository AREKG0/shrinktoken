"""
Compressibility Analyzer for ShrinkToken Pro.
Determines whether a prompt is worth compressing before invoking expensive LLMLingua inference.
Evaluates token count, structured content ratio (code/JSON/URLs), constraint density,
and minimum estimated token savings.
"""
import re
from typing import Dict, Any

class CompressibilityAnalyzer:
    def __init__(self, min_token_savings: int = 3, min_compressible_length: int = 20):
        self.min_token_savings = min_token_savings
        self.min_compressible_length = min_compressible_length

    def analyze(self, text: str, category: str = "general") -> Dict[str, Any]:
        if not text:
            return {
                "compressible": False,
                "estimated_benefit": 0.0,
                "risk_level": "LOW",
                "recommended_strategy": "passthrough",
                "reason": "Empty input"
            }

        # 1. Estimate Token Count (simple whitespace words fallback)
        word_count = len(text.split())
        
        # 2. Check length threshold
        if word_count < self.min_compressible_length:
            return {
                "compressible": False,
                "estimated_benefit": 0.0,
                "risk_level": "LOW",
                "recommended_strategy": "passthrough",
                "reason": f"Prompt length ({word_count} words) below minimum compressible threshold ({self.min_compressible_length})"
            }

        # 3. Analyze Structured Content Ratio (code blocks, JSON, URLs, paths)
        code_blocks = re.findall(r'```[\s\S]*?```', text)
        json_objs = re.findall(r'\{[\s\S]*?"[\w_]+"\s*:\s*[\s\S]*?\}', text)
        urls = re.findall(r'https?://[^\s]+', text)
        paths = re.findall(r'[a-zA-Z]:\\[\w\.\-\\]+|/(?:etc|tmp|var|usr|home)/[\w\.\-/]+', text)

        structured_char_count = sum(len(cb) for cb in code_blocks) + \
                                sum(len(jo) for jo in json_objs) + \
                                sum(len(u) for u in urls) + \
                                sum(len(p) for p in paths)
        
        total_char_count = max(1, len(text))
        structured_ratio = structured_char_count / total_char_count

        # Categories that are naturally protected or have 0% historical benefit
        if category in ["json", "urls_paths", "code", "negation", "numeric_constraints", "output_formats", "ranges", "roles"]:
            if structured_ratio > 0.6 or word_count < 25:
                return {
                    "compressible": False,
                    "estimated_benefit": 0.0,
                    "risk_level": "LOW",
                    "recommended_strategy": "passthrough",
                    "reason": f"Category '{category}' has high structured ratio ({structured_ratio:.1%}) or high risk of constraint loss"
                }

        # 4. Count Hard Constraints & Negations
        negations = re.findall(r'\b(do not|don\'t|never|cannot|can\'t|must not|should not|refrain from|avoid)\b', text, re.I)
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        
        constraint_density = (len(negations) + len(numbers)) / max(1, word_count)

        # High-risk dense multi-constraint short prompts
        if constraint_density > 0.25 and word_count < 35:
            return {
                "compressible": False,
                "estimated_benefit": 0.0,
                "risk_level": "HIGH",
                "recommended_strategy": "passthrough",
                "reason": "High constraint density in short prompt; compression risks constraint loss"
            }

        # 5. Estimate Potential Benefit based on Category & Prose Length
        if category in ["general", "multi_constraint", "rag", "reasoning", "agents"]:
            estimated_reduction_pct = 0.20 if category == "general" else 0.15
            est_tokens_saved = word_count * estimated_reduction_pct
            
            if est_tokens_saved < self.min_token_savings:
                return {
                    "compressible": False,
                    "estimated_benefit": round(est_tokens_saved, 1),
                    "risk_level": "LOW",
                    "recommended_strategy": "passthrough",
                    "reason": f"Estimated savings ({est_tokens_saved:.1f} tokens) below minimum threshold ({self.min_token_savings} tokens)"
                }
                
            risk = "HIGH" if category == "multi_constraint" else ("MEDIUM" if category in ["rag", "reasoning"] else "LOW")
            strategy = f"{category}_selective_compression"
            
            return {
                "compressible": True,
                "estimated_benefit": round(est_tokens_saved, 1),
                "risk_level": risk,
                "recommended_strategy": strategy,
                "reason": f"Category '{category}' has compressible prose (estimated {est_tokens_saved:.1f} token savings)"
            }

        # Default fallback for unclassified categories
        return {
            "compressible": True,
            "estimated_benefit": round(word_count * 0.10, 1),
            "risk_level": "MEDIUM",
            "recommended_strategy": "balanced_selective",
            "reason": "Standard candidate for selective compression"
        }
