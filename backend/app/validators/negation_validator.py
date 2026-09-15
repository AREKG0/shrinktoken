import re

class NegationValidator:
    """Validates that negation polarity, action targets, and scope modifiers are strictly preserved."""
    
    def validate(self, original_text: str, compressed_text: str) -> bool:
        if not original_text:
            return True
            
        original_clean = original_text.lower()
        compressed_clean = compressed_text.lower()
        
        # 1. Negation trigger patterns
        negation_pattern = r'\b(do not|don\'t|never|cannot|can\'t|must not|mustn\'t|should not|shouldn\'t|not|no|refrain from|avoid|prohibit)\b'
        
        # Check if original had a negation trigger that was completely inverted in compressed
        # Example: "Don't apologize if..." vs "Apologize profusely if..."
        orig_matches = list(re.finditer(negation_pattern, original_clean))
        if not orig_matches:
            return True
            
        # 2. Extract negation scopes from original text
        for match in orig_matches:
            trigger = match.group(1)
            start_pos = match.end()
            following_text = original_clean[start_pos:].strip()
            words = re.findall(r'\b\w+\b', following_text)[:6]
            if not words:
                continue
                
            key_action = words[0]  # e.g., 'ask', 'apologize', 'summarize'
            stem = key_action[:4] if len(key_action) >= 4 else key_action
            
            # Check if action appears in compressed text
            # Sentence split
            sent_split_re = r'(?<=[.!?])\s+'
            compressed_sentences = [s.strip() for s in re.split(sent_split_re, compressed_clean) if s.strip()]
            if not compressed_sentences:
                compressed_sentences = [compressed_clean]
                
            containing_sentences = [s for s in compressed_sentences if re.search(r'\b' + re.escape(stem) + r'\w*', s)]
            
            if not containing_sentences:
                # If action verb itself disappeared completely → dropped prohibition
                return False
                
            # Each sentence containing this action verb must have the negation trigger directly preceding the action verb (within 3 words)
            action_negated = False
            for s in containing_sentences:
                neg_near_action = rf'{negation_pattern}\s+(?:\w+\s+){{0,3}}{re.escape(stem)}'
                if re.search(neg_near_action, s):
                    action_negated = True
                    break
            if not action_negated:
                # The action appears without its direct negation -> polarity flipped!
                return False
                    
            # 3. Check Scope Modifiers following the negation
            # e.g., "Do not ask me questions about my preferences" -> scope words: "preferences"
            # e.g., "Never mention politics during the interview" -> scope words: "politics", "interview"
            scope_nouns = [w for w in words[1:] if len(w) >= 4 and w not in ["that", "this", "some", "your", "what", "have", "with", "from", "questions"]]
            for scope_w in scope_nouns:
                if scope_w not in compressed_clean:
                    # Trailing scope context noun dropped -> unsafe scope loss!
                    return False
                    
        return True
