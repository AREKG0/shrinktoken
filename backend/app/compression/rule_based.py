from backend.app.compression.base import BaseCompressor

class RuleBasedCompressor(BaseCompressor):
    """Rule-based compressor. Implementation planned for Phase N."""
    
    @property
    def name(self) -> str:
        return "RuleBased"
        
    @property
    def is_available(self) -> bool:
        return False
        
    def compress(self, text: str, config):
        raise NotImplementedError("Planned for Phase N")
