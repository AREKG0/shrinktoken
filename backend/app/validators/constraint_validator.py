import re
from backend.app.validators.negation_validator import NegationValidator
from backend.app.validators.numeric_validator import NumericValidator
from backend.app.validators.structural_validator import StructuralValidator
from backend.app.validators.format_validator import FormatValidator
from backend.app.validators.audience_validator import AudienceValidator
from backend.app.models.validation import ValidationResult
from backend.app.services.prompt_parser import PromptParser

class ConstraintValidator:
    """
    Unified Validation Engine integrating Negation, Numeric, Structural, Format,
    and Audience sub-validators, plus explicit positive clause and style preservation checks.
    """

    def __init__(self):
        self.negation_v = NegationValidator()
        self.numeric_v = NumericValidator()
        self.structural_v = StructuralValidator()
        self.format_v = FormatValidator()
        self.audience_v = AudienceValidator()
        self.parser = PromptParser()

    def validate(self, original_text: str, compressed_text: str) -> ValidationResult:
        if not original_text:
            return ValidationResult(total_constraints=0, preserved=0, failed=0, status="PASS")
            
        orig_clean = original_text.lower()
        comp_clean = compressed_text.lower()
        failures = []

        # 1. Negation & Scope Validation (including ADV-001)
        if not self.negation_v.validate(original_text, compressed_text):
            failures.append("Negation polarity flipped, target missing, or scope truncated")

        # 2. Numeric & Unit & Range Semantics Validation
        if not self.numeric_v.validate(original_text, compressed_text):
            failures.append("Numeric value, range direction, scale unit, or entity binding violated")

        # 3. Structural & Path & Schema Validation
        if not self.structural_v.validate(original_text, compressed_text):
            failures.append("Path, tool signature, JSON schema field, or output format requirement missing/corrupted")

        # 4. Format & Output Restrictions Validation (including ADV-023)
        if not self.format_v.validate(original_text, compressed_text):
            failures.append("Output format restrictions or cardinality requirements violated")

        # 5. Audience & Persona Role Validation
        if not self.audience_v.validate(original_text, compressed_text):
            failures.append("Target audience role or persona requirement dropped or altered")

        # 6. Positive Clause & Required Action Preservation
        if ", but " in orig_clean:
            after_but = orig_clean.split(", but ")[1].strip()
            verbs = re.findall(r'\b(explain|provide|include|return|output|show|summarize|list|details)\b', after_but)
            for v in verbs:
                if v not in comp_clean:
                    failures.append(f"Positive required clause action '{v}' dropped")
                    break

        # 7. Style & Tone Modifier Preservation
        style_keywords = ["simple language", "concise", "professional tone", "like i am a child", "without jargon", "easy to understand"]
        for style_phrase in style_keywords:
            if style_phrase in orig_clean and style_phrase not in comp_clean:
                failures.append(f"Explicit style requirement '{style_phrase}' dropped")
                break

        # Status decision
        total = len(failures)
        if total > 0:
            return ValidationResult(
                total_constraints=total,
                preserved=0,
                failed=total,
                status="FAIL",
                critical_failures=failures,
                details=failures
            )
            
        return ValidationResult(
            total_constraints=1,
            preserved=1,
            failed=0,
            status="PASS"
        )
