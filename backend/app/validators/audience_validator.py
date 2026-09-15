import re
from typing import Dict, Any, Optional, List

class AudienceValidator:
    """
    AudienceValidator for Phase 6.75.
    Detects target audience, reader background, and role persona shifts
    between original prompt and compressed prompt.
    """

    AUDIENCE_LEVELS = [
        ("beginner", ["beginner", "novice", "layman", "10-year-old", "child", "student", "non-technical", "no programming knowledge", "no prior experience"]),
        ("intermediate", ["intermediate", "practitioner"]),
        ("expert", ["expert", "senior", "professional", "advanced", "doctorate", "specialist", "veteran"])
    ]

    ROLE_PATTERNS = [
        r'\bact as a\s+([\w\s]{2,25})\b',
        r'\byou are a\s+([\w\s]{2,25})\b',
        r'\brole:\s*([\w\s]{2,25})\b',
        r'\bassume the role of\s+([\w\s]{2,25})\b'
    ]

    def extract_audience(self, text: str) -> Dict[str, Any]:
        if not text:
            return {}

        clean = text.lower()
        level = None
        keywords_found = []

        for lvl_name, kws in self.AUDIENCE_LEVELS:
            for kw in kws:
                if kw in clean:
                    level = lvl_name
                    keywords_found.append(kw)

        role = None
        for r_pat in self.ROLE_PATTERNS:
            m = re.search(r_pat, clean)
            if m:
                role = m.group(1).strip()
                break

        return {
            "level": level,
            "keywords": keywords_found,
            "role": role
        }

    def validate(self, original_text: str, compressed_text: str) -> bool:
        orig_aud = self.extract_audience(original_text)
        if not orig_aud.get("level") and not orig_aud.get("role"):
            return True

        comp_aud = self.extract_audience(compressed_text)
        orig_clean = original_text.lower()
        comp_clean = compressed_text.lower()

        # 1. Level shift check (e.g. beginner -> expert)
        orig_lvl = orig_aud.get("level")
        comp_lvl = comp_aud.get("level")
        if orig_lvl and comp_lvl and orig_lvl != comp_lvl:
            return False

        # 2. Audience keyword preservation check
        for kw in orig_aud.get("keywords", []):
            if kw in orig_clean and kw not in comp_clean:
                # Check if an opposing level keyword replaced it
                if orig_lvl == "beginner" and any(e in comp_clean for e in ["expert", "advanced", "professional"]):
                    return False
                if orig_lvl == "expert" and any(b in comp_clean for b in ["beginner", "novice", "child"]):
                    return False
                # If kw dropped completely
                return False

        # 3. Role persona check
        orig_role = orig_aud.get("role")
        comp_role = comp_aud.get("role")
        if orig_role:
            if not comp_role and orig_role.lower() not in comp_clean:
                return False
            if comp_role and orig_role.lower() != comp_role.lower():
                return False

        return True
