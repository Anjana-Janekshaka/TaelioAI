from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

@dataclass
class GenerationResult(Generic[T]):
    output: T
    provider: str
    model: str
    tokens_in: int
    tokens_out: int
    latency_ms: int
    cost_usd: float

class IdeaProvider:
    def generate(self, request):
        raise NotImplementedError

class StoryProvider:
    def generate(self, request):
        raise NotImplementedError
