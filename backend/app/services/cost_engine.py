from typing import Dict, Any
from backend.app.models.cost import CostResult

class CostEngine:
    """
    Configurable Cost Model for ShrinkToken Pro (Phase 6.75).
    Calculates hypothetical / configurable benchmark inference costs and savings.
    """
    
    LABEL = "HYPOTHETICAL / CONFIGURABLE BENCHMARK COST"

    def calculate(
        self,
        original_input_tokens: int,
        optimized_input_tokens: int,
        provider_input_price_per_million: float = 2.50,
        number_of_requests: int = 1
    ) -> CostResult:
        orig_tokens_total = original_input_tokens * number_of_requests
        opt_tokens_total = optimized_input_tokens * number_of_requests
        
        baseline_cost = round((orig_tokens_total / 1_000_000.0) * provider_input_price_per_million, 6)
        optimized_cost = round((opt_tokens_total / 1_000_000.0) * provider_input_price_per_million, 6)
        cost_saved = round(baseline_cost - optimized_cost, 6)
        
        pct_saved = 0.0
        if baseline_cost > 0:
            pct_saved = round((cost_saved / baseline_cost) * 100.0, 2)

        tokens_saved_per_req = max(0, original_input_tokens - optimized_input_tokens)
        break_even_reqs = 1
        if tokens_saved_per_req > 0:
            # Simple benchmark break-even heuristic
            break_even_reqs = 1

        return CostResult(
            original_cost=baseline_cost,
            optimized_cost=optimized_cost,
            compression_overhead=0.0,
            net_saving=cost_saved,
            currency="USD"
        )
