import re
from typing import List
from backend.app.models.prompt import ParsedPrompt, PromptSegment, SegmentType

class PromptParser:
    """Prompt parser. Categorizes sentences into roles, tasks, constraints, etc."""
    
    def parse(self, text: str) -> ParsedPrompt:
        if not text:
            return ParsedPrompt(original_text=text, segments=[])
            
        segments = []
        
        # Step 1: Detect Markdown code blocks and pull them out as structured_content
        code_block_pattern = r'(```[\s\S]*?```)'
        parts = re.split(code_block_pattern, text)
        
        for part in parts:
            if not part.strip():
                continue
            
            # If it's a code block, classify as structured_content
            if part.strip().startswith('```'):
                segments.append(PromptSegment(
                    text=part,
                    segment_type=SegmentType.structured_content,
                    confidence=1.0
                ))
                continue
                
            # Step 2: Split the non-code parts into sentences
            sentences = self._split_into_sentences(part)
            for sentence in sentences:
                if not sentence.strip():
                    continue
                segment_type, confidence = self._classify_sentence(sentence)
                segments.append(PromptSegment(
                    text=sentence,
                    segment_type=segment_type,
                    confidence=confidence
                ))
                
        return ParsedPrompt(original_text=text, segments=segments)
        
    def _split_into_sentences(self, text: str) -> List[str]:
        paragraphs = text.split('\n')
        sentences = []
        for paragraph in paragraphs:
            if not paragraph.strip():
                continue
            split_p = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])', paragraph)
            for s in split_p:
                if s.strip():
                    sentences.append(s.strip())
        return sentences
        
    def _classify_sentence(self, sentence: str) -> tuple[SegmentType, float]:
        clean = sentence.lower().strip()
        
        # Check structured content first
        if clean.startswith('{') or clean.startswith('[') or clean.startswith('<'):
            return SegmentType.structured_content, 0.95
            
        # 1. Constraints
        constraint_regex = r'\b(do not|don\'t|never|cannot|must not|should not|shouldn\'t|avoid|prohibited|except|unless|only|exactly|limit|no)\b'
        if re.search(constraint_regex, clean):
            return SegmentType.constraint, 0.9
            
        # 2. Output requirements
        output_regex = r'\b(format|output|return|respond|json|xml|yaml|markdown|csv|bullet|list|schema|length|paragraphs|words|sentences)\b'
        if re.search(output_regex, clean):
            return SegmentType.output_requirement, 0.8
            
        # 3. Roles
        role_regex = r'\b(act as|you are (a|an|the)?|as (a|an|the)?|answer as (a|an|the)?|persona is|role is|position is)\b'
        if re.search(role_regex, clean):
            return SegmentType.role, 0.95
            
        # 4. Tasks
        task_regex = r'\b(write|explain|summarize|create|generate|analyze|parse|extract|translate|calculate|evaluate|solve|help me|develop|design)\b'
        if re.search(task_regex, clean):
            return SegmentType.task, 0.85
            
        # 5. Examples
        example_regex = r'\b(example|examples|input|output|instance)\b\s*:'
        if re.search(example_regex, clean) or 'for example' in clean:
            return SegmentType.example, 0.9
            
        # Fallback to context or unknown
        if len(clean.split()) > 5:
            return SegmentType.context, 0.6
            
        return SegmentType.unknown, 0.5

