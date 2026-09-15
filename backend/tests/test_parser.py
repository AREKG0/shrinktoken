from backend.app.models.prompt import SegmentType
from backend.app.services.prompt_parser import PromptParser

def test_prompt_parser_role():
    parser = PromptParser()
    result = parser.parse("Act as a Python tutor. Help me write a script.")
    assert len(result.segments) >= 2
    assert result.segments[0].segment_type == SegmentType.role
    assert result.segments[1].segment_type == SegmentType.task

def test_prompt_parser_constraint():
    parser = PromptParser()
    result = parser.parse("Do not mention politics. Explain history.")
    assert result.segments[0].segment_type == SegmentType.constraint
    assert result.segments[1].segment_type == SegmentType.task

def test_prompt_parser_code_block():
    parser = PromptParser()
    result = parser.parse("Explain this code:\n```python\nprint('hello')\n```")
    assert any(s.segment_type == SegmentType.structured_content for s in result.segments)
