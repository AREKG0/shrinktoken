import re
from typing import Dict, Any, List
from backend.app.validators.constraint_validator import ConstraintValidator
from backend.app.services.instruction_extractor import InstructionExtractor

class SegmentCompressor:
    """
    Phase 6.5 SegmentCompressor.
    Extracts minimal required constraint spans (negations, numeric targets, formats, style phrases)
    rather than full sentences, allowing background connective prose to be safely compressed.
    """
    
    def __init__(self):
        self.validator = ConstraintValidator()
        self.extractor = InstructionExtractor()

    def extract_minimal_constraint_spans(self, text: str) -> List[str]:
        spans = []
        # 1. Extracted hard instructions from InstructionExtractor
        instructions = self.extractor.extract(text)
        for inst in instructions:
            spans.append(inst.raw_text)

        # 2. Key constraint phrases
        key_phrases = re.findall(r'\b(do not|don\'t|never|cannot|exactly \d+|at least \d+|at most \d+|between \d+ and \d+|in simple language|markdown table|valid json|no jargon)\b', text, re.I)
        spans.extend(key_phrases)
        
        return list(set(s.strip() for s in spans if s and len(s.strip()) > 3))

    def compress_selectively(self, text: str, compressor_fn, get_token_count_fn, min_expendable_words: int = 15) -> str:
        spans = self.extract_minimal_constraint_spans(text)
        if not spans:
            return compressor_fn(text)

        # Split prompt into sentences
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
        
        protected_sents = []
        expendable_sents = []
        
        for s in sentences:
            if any(span.lower() in s.lower() for span in spans):
                protected_sents.append(s)
            else:
                expendable_sents.append(s)

        if not expendable_sents or get_token_count_fn(" ".join(expendable_sents)) < min_expendable_words:
            return text

        expendable_text = " ".join(expendable_sents)
        try:
            compressed_exp = compressor_fn(expendable_text)
        except Exception:
            compressed_exp = expendable_text

        # Reconstruct: protected sentences preserved verbatim
        reconstructed = []
        for s in sentences:
            if s in protected_sents:
                reconstructed.append(s)
            elif compressed_exp:
                reconstructed.append(compressed_exp)
                compressed_exp = ""  # append once

        candidate = " ".join(reconstructed)
        
        # Validate reconstructed candidate
        val = self.validator.validate(text, candidate)
        if val.status == "PASS":
            return candidate
            
        return text
