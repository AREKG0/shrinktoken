import re
from typing import Dict, Any, Tuple, List
from backend.app.validators.constraint_validator import ConstraintValidator
from backend.app.core.config import settings

class RAGStrategy:
    """
    Phase 6.75 RAG Strategy.
    Protects 100% of System Instructions, User Query, and Answer Requirements.
    Applies adaptive retention rate testing (0.50, 0.65, 0.80, 0.90 — capped at MAX_MODEL_CALLS=4) to Retrieved Context.
    Validates complete reconstructed prompt to guarantee safe context compression.
    """

    CONTEXT_PATTERNS = [
        r'\bcontext:\s*',
        r'\bretrieved context:\s*',
        r'\bdocument:\s*',
        r'\bexcerpts:\s*',
        r'\bsource text:\s*'
    ]

    QUERY_PATTERNS = [
        r'\bquestion:\s*',
        r'\bquery:\s*',
        r'\buser question:\s*',
        r'\banswer:\s*'
    ]

    def __init__(self, max_model_calls: int = settings.MAX_MODEL_CALLS):
        self.validator = ConstraintValidator()
        self.max_model_calls = max_model_calls

    def segment_rag(self, prompt: str) -> Tuple[str, str, str]:
        instructions = ""
        context = ""
        query = ""

        c_match = None
        for cp in self.CONTEXT_PATTERNS:
            m = re.search(cp, prompt, re.I)
            if m:
                c_match = m
                break

        q_match = None
        for qp in self.QUERY_PATTERNS:
            m = re.search(qp, prompt, re.I)
            if m:
                q_match = m
                break

        if c_match and q_match:
            c_start = c_match.end()
            q_start = q_match.start()

            instructions = prompt[:c_match.start()].strip()
            context = prompt[c_start:q_start].strip()
            query = prompt[q_start:].strip()
        elif c_match:
            c_start = c_match.end()
            instructions = prompt[:c_match.start()].strip()
            context = prompt[c_start:].strip()
        else:
            context = prompt

        return instructions, context, query

    def compress_rag(self, prompt: str, base_compressor, get_token_count_fn) -> Dict[str, Any]:
        instructions, context, query = self.segment_rag(prompt)

        orig_total = get_token_count_fn(prompt)
        orig_instr = get_token_count_fn(instructions + " " + query)
        orig_ctx = get_token_count_fn(context)

        if not context or orig_ctx < settings.MIN_COMPRESSIBLE_LENGTH:
            return {
                "compressed_text": prompt,
                "orig_total_tokens": orig_total,
                "opt_total_tokens": orig_total,
                "orig_instruction_tokens": orig_instr,
                "opt_instruction_tokens": orig_instr,
                "orig_context_tokens": orig_ctx,
                "opt_context_tokens": orig_ctx,
                "context_reduction_percent": 0.0,
                "total_reduction_percent": 0.0,
                "fallback": False,
                "model_calls": 0
            }

        # Strictly cap retention rates to max_model_calls=4
        rates_to_test = [0.50, 0.65, 0.80, 0.90][:self.max_model_calls]
        best_comp_text = prompt
        best_opt_total = orig_total
        best_opt_ctx = orig_ctx
        model_calls = 0
        is_valid_found = False

        from backend.app.models.prompt import CompressionConfig, CompressionMode

        for rate in rates_to_test:
            model_calls += 1
            try:
                cfg = CompressionConfig(mode=CompressionMode.balanced, target_rate=rate)
                comp_res = base_compressor.compress(context, cfg)
                comp_ctx_str = comp_res.compressed_text
            except Exception:
                comp_ctx_str = context

            # Reconstruct prompt
            reconstructed = []
            if instructions:
                reconstructed.append(instructions)
            if comp_ctx_str:
                reconstructed.append(f"Context: {comp_ctx_str}")
            if query:
                reconstructed.append(query)

            cand_prompt = "\n\n".join(reconstructed) if reconstructed else prompt
            
            # Validate reconstructed prompt
            val = self.validator.validate(prompt, cand_prompt)
            if val.status == "PASS":
                best_comp_text = cand_prompt
                best_opt_total = get_token_count_fn(cand_prompt)
                best_opt_ctx = get_token_count_fn(comp_ctx_str)
                is_valid_found = True
                break  # Pick strongest safe rate

        total_saved = max(0, orig_total - best_opt_total)
        total_red_pct = round((total_saved / max(1, orig_total)) * 100.0, 2)
        ctx_saved = max(0, orig_ctx - best_opt_ctx)
        ctx_red_pct = round((ctx_saved / max(1, orig_ctx)) * 100.0, 2)

        return {
            "compressed_text": best_comp_text if is_valid_found else prompt,
            "orig_total_tokens": orig_total,
            "opt_total_tokens": best_opt_total if is_valid_found else orig_total,
            "orig_instruction_tokens": orig_instr,
            "opt_instruction_tokens": orig_instr,
            "orig_context_tokens": orig_ctx,
            "opt_context_tokens": best_opt_ctx if is_valid_found else orig_ctx,
            "context_reduction_percent": ctx_red_pct if is_valid_found else 0.0,
            "total_reduction_percent": total_red_pct if is_valid_found else 0.0,
            "fallback": not is_valid_found,
            "model_calls": model_calls
        }
