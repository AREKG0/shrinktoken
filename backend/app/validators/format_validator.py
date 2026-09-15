import re
from typing import Dict, Any, Optional, List

class FormatValidator:
    """
    FormatValidator for Phase 6.75.
    Extracts structural output format requirements (output_type, cardinality, restrictions)
    and verifies that compressed text does not alter or corrupt format constraints (e.g. ADV-023).
    """

    FORMAT_PATTERNS = [
        (r'\b(single|one)\s+(floating point number|float|decimal number)\b', {"output_type": "floating_point_number", "cardinality": 1}),
        (r'\b(floating point number|float|decimal number)\b', {"output_type": "floating_point_number", "cardinality": 1}),
        (r'\b(single|one)\s+(integer|int|whole number)\b', {"output_type": "integer", "cardinality": 1}),
        (r'\b(integer|int|whole number)\b', {"output_type": "integer", "cardinality": 1}),
        (r'\b(single|one)\s+number\b', {"output_type": "number", "cardinality": 1}),
        (r'\b(single|one)\s+sentence\b', {"output_type": "sentence", "cardinality": 1}),
        (r'\b(single|one)\s+paragraph\b', {"output_type": "paragraph", "cardinality": 1}),
        (r'\b(multi-paragraph|multiple paragraphs)\b', {"output_type": "paragraph", "cardinality": "multiple"}),
        (r'\b(json|valid json|json object|json array)\b', {"output_type": "json"}),
        (r'\b(xml|valid xml)\b', {"output_type": "xml"}),
        (r'\b(csv|csv format)\b', {"output_type": "csv"}),
        (r'\b(markdown table|table format)\b', {"output_type": "markdown_table"}),
        (r'\b(boolean|bool|true/false|true or false)\b', {"output_type": "boolean", "cardinality": 1})
    ]

    RESTRICTIVE_PATTERNS = [
        r'\bonly\b',
        r'\bexactly\b',
        r'\bsingle\b',
        r'\bfinal answer only\b',
        r'\bno additional text\b',
        r'\bno explanation\b',
        r'\bwithout explanation\b'
    ]

    CONFLICTING_CONVERSIONS = {
        "floating_point_number": ["paragraph", "multi-paragraph", "explanation", "table", "json"],
        "integer": ["paragraph", "multi-paragraph", "explanation", "table"],
        "number": ["paragraph", "multi-paragraph", "explanation"],
        "boolean": ["paragraph", "multi-paragraph", "explanation"],
        "sentence": ["multi-paragraph", "long explanation"],
        "paragraph": ["floating_point_number", "integer"]
    }

    def extract_format_spec(self, text: str) -> Dict[str, Any]:
        if not text:
            return {}

        clean = text.lower()
        spec = {
            "output_type": None,
            "cardinality": None,
            "restrictive": False,
            "additional_text_prohibited": False,
            "raw_matches": []
        }

        for pattern, meta in self.FORMAT_PATTERNS:
            if re.search(pattern, clean):
                if not spec["output_type"]:
                    spec["output_type"] = meta.get("output_type")
                    spec["cardinality"] = meta.get("cardinality")
                spec["raw_matches"].append(meta.get("output_type"))

        for r_pat in self.RESTRICTIVE_PATTERNS:
            if re.search(r_pat, clean):
                spec["restrictive"] = True
                if "no additional" in r_pat or "no explanation" in r_pat or "final answer only" in r_pat:
                    spec["additional_text_prohibited"] = True

        return spec

    def validate(self, original_text: str, compressed_text: str) -> bool:
        orig_spec = self.extract_format_spec(original_text)
        if not orig_spec.get("output_type") and not orig_spec.get("restrictive"):
            return True

        comp_spec = self.extract_format_spec(compressed_text)
        orig_type = orig_spec.get("output_type")
        comp_type = comp_spec.get("output_type")

        # 1. Check direct output_type loss when original has restrictive requirements
        if orig_type and orig_spec.get("restrictive"):
            if orig_type != comp_type:
                return False

        # 2. Check conflicting output_type conversion (e.g. floating_point_number -> multi-paragraph)
        if orig_type and comp_type:
            conflicts = self.CONFLICTING_CONVERSIONS.get(orig_type, [])
            if comp_type in conflicts:
                return False

        # 3. Check cardinality shift (e.g. single -> multiple)
        orig_card = orig_spec.get("cardinality")
        comp_card = comp_spec.get("cardinality")
        if orig_card and comp_card and orig_card != comp_card:
            return False

        # 4. Check explicitly prohibited keywords if original required "no explanation" or "only"
        if orig_spec.get("additional_text_prohibited") or orig_spec.get("restrictive"):
            comp_clean = compressed_text.lower()
            if "multi-paragraph" in comp_clean or "long explanation" in comp_clean or "detailed explanation" in comp_clean:
                return False

        return True
