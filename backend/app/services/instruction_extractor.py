import re
from typing import List
from backend.app.models.prompt import ExtractedConstraint, ConstraintType, SegmentType
from backend.app.services.prompt_parser import PromptParser

class InstructionExtractor:
    """Extracts hard constraints and critical instructions from prompts."""
    
    def __init__(self, parser: PromptParser = None):
        self.parser = parser or PromptParser()
        
    def extract(self, text: str) -> List[ExtractedConstraint]:
        if not text:
            return []
            
        parsed = self.parser.parse(text)
        constraints = []
        
        for segment in parsed.segments:
            is_explicit_constraint = segment.segment_type == SegmentType.constraint
            
            # Modal and style keywords checking
            modals_check = re.search(r'\b(must|should|never|only|exactly|do not|cannot|unless|except|use|format|output|write)\b', segment.text.lower())
            
            if is_explicit_constraint or modals_check:
                extracted = self._parse_constraint(segment.text)
                constraints.append(extracted)
                
        return constraints
        
    def _parse_constraint(self, text: str) -> ExtractedConstraint:
        clean = text.lower().strip()
        
        # 1. Prohibitions / Negations
        negation_match = re.search(r'\b(do not|don\'t|never|cannot|must not|should not|shouldn\'t|avoid|prohibited)\s+([\w\s]{2,20})\b', clean)
        if negation_match:
            action = negation_match.group(2).strip()
            return ExtractedConstraint(
                raw_text=text,
                constraint_type=ConstraintType.prohibition,
                details={
                    "action": action,
                    "polarity": "negative",
                    "trigger_word": negation_match.group(1)
                }
            )
            
        # 2. Quantity constraints (prefix)
        quantity_match = re.search(r'\b(exactly|at least|at most|limit of|maximum of|minimum of)\s+(\d+)\s+([\w\s]{2,20})\b', clean)
        if quantity_match:
            try:
                val = int(quantity_match.group(2))
                return ExtractedConstraint(
                    raw_text=text,
                    constraint_type=ConstraintType.quantity,
                    details={
                        "operator": quantity_match.group(1),
                        "value": val,
                        "target": quantity_match.group(3).strip()
                    }
                )
            except ValueError:
                pass
                
        # 3. Quantity constraints (suffix)
        quantity_suffix = re.search(r'\b(\d+)\s+([\w\s]{2,20})\s+(or less|or more|minimum|maximum)\b', clean)
        if quantity_suffix:
            try:
                val = int(quantity_suffix.group(1))
                return ExtractedConstraint(
                    raw_text=text,
                    constraint_type=ConstraintType.quantity,
                    details={
                        "operator": quantity_suffix.group(3),
                        "value": val,
                        "target": quantity_suffix.group(2).strip()
                    }
                )
            except ValueError:
                pass
                
        # 4. Style Constraints
        style_match = re.search(r'\b(use|format as|output in|write in|style is)\s+([\w\s]{2,20})\b', clean)
        if style_match:
            return ExtractedConstraint(
                raw_text=text,
                constraint_type=ConstraintType.style,
                details={
                    "requirement": style_match.group(2).strip()
                }
            )
            
        # 5. Default fallback to unknown / high risk
        return ExtractedConstraint(
            raw_text=text,
            constraint_type=ConstraintType.unknown,
            details={},
            high_risk=True
        )
