from backend.app.services.protection_engine import ProtectionEngine

def test_protection_engine_code_block():
    engine = ProtectionEngine()
    text = "Run this code:\n```python\nprint('hello')\n```\nAnd then run it."
    masked, mapping = engine.mask(text)
    assert "__ST_PROTECT_CODE_0__" in masked
    assert "print('hello')" not in masked
    
    restored = engine.unmask(masked, mapping)
    assert restored == text
    assert engine.validate_placeholders(masked, mapping) is True

def test_protection_engine_json():
    engine = ProtectionEngine()
    text = 'Here is the data: {"name": "Raviraj", "age": 25} and that is all.'
    masked, mapping = engine.mask(text)
    assert "__ST_PROTECT_JSON_0__" in masked
    assert "Raviraj" not in masked
    
    restored = engine.unmask(masked, mapping)
    assert restored == text
    assert engine.validate_placeholders(masked, mapping) is True

def test_protection_engine_url():
    engine = ProtectionEngine()
    text = "Visit https://google.com or http://example.com/test for details."
    masked, mapping = engine.mask(text)
    assert "__ST_PROTECT_URL_0__" in masked
    assert "__ST_PROTECT_URL_1__" in masked
    assert "google.com" not in masked
    
    restored = engine.unmask(masked, mapping)
    assert restored == text
    assert engine.validate_placeholders(masked, mapping) is True

def test_protection_engine_invalid_placeholder_count():
    engine = ProtectionEngine()
    text = "Visit https://google.com"
    masked, mapping = engine.mask(text)
    
    # Simulate a deleted placeholder
    corrupted_masked = masked.replace("__ST_PROTECT_URL_0__", "")
    assert engine.validate_placeholders(corrupted_masked, mapping) is False
    
    # Simulate a duplicated placeholder
    duplicated_masked = masked + " __ST_PROTECT_URL_0__"
    assert engine.validate_placeholders(duplicated_masked, mapping) is False
