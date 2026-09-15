import pytest
from backend.app.models.prompt import CompressionMode
from backend.app.compression.llmlingua import LLMLinguaCompressor
from backend.app.services.compression_engine import CompressionService

@pytest.fixture
def service():
    compressor = LLMLinguaCompressor()
    # Mocking the actual LLMLingua loading for fast tests unless marked slow
    return CompressionService(compressor)

@pytest.mark.slow
def test_compression_reduces_tokens(service):
    text = "Hello, could you please summarize the main points of this lengthy document? Thank you very much for your help!" * 10
    result = service.optimize(text, mode=CompressionMode.balanced)
    assert result.compressed_tokens < result.original_tokens

@pytest.mark.slow
def test_modes_all_return_valid_compressed_output(service):
    """
    Per the spec: SAFE/BALANCED/AGGRESSIVE are compression targets only, not safety guarantees.
    The adaptive engine finds the maximum compression that passes validation, regardless of mode.
    All modes must return a result with status 'safe' or fall back gracefully to 'failed'.
    """
    text = "Here is a very long prompt with many details. Please make sure to read carefully and summarize the key findings appropriately. " * 5
    for mode in [CompressionMode.safe, CompressionMode.balanced, CompressionMode.aggressive]:
        result = service.optimize(text, mode=mode)
        assert result.status in ['safe', 'failed'], f"Mode {mode} returned unexpected status: {result.status}"
        assert result.compressed_text, f"Mode {mode} returned empty compressed text"


@pytest.mark.slow
def test_empty_input_handled(service):
    result = service.optimize("", mode=CompressionMode.balanced)
    assert result.status in ['safe', 'failed']

def test_short_input_returned_unchanged(service):
    text = "Short prompt"
    result = service.optimize(text, mode=CompressionMode.balanced)
    assert result.original_text == result.compressed_text
    assert result.compressed_tokens == result.original_tokens

def test_compression_result_has_required_fields(service):
    text = "Short"
    result = service.optimize(text, mode=CompressionMode.balanced)
    assert hasattr(result, 'original_text')
    assert hasattr(result, 'compressed_text')
    assert hasattr(result, 'original_tokens')
    assert hasattr(result, 'compressed_tokens')
    assert hasattr(result, 'compression_ratio')
    assert hasattr(result, 'saving_percent')
    assert hasattr(result, 'mode_used')
    assert hasattr(result, 'status')
