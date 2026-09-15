from abc import ABC, abstractmethod
from backend.app.models.prompt import CompressionConfig
from backend.app.models.optimization import CompressionResult

class BaseCompressor(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @property
    @abstractmethod
    def is_available(self) -> bool:
        pass
        
    @abstractmethod
    def compress(self, text: str, config: CompressionConfig) -> CompressionResult:
        pass
