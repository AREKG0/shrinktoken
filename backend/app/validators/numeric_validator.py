import re

class NumericValidator:
    """
    Validates preservation of exact numbers, range bounds, units, operator bindings,
    and range directions (e.g., 3.3V to 5.0V vs 5.0V to 3.3V).
    """
    
    WORD_TO_NUM = {
        "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
        "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
        "eleven": "11", "twelve": "12"
    }

    def validate(self, original_text: str, compressed_text: str) -> bool:
        if not original_text:
            return True

        orig_clean = original_text.lower()
        comp_clean = compressed_text.lower()

        # Convert spelled-out numbers to digits
        orig_clean_num = orig_clean
        comp_clean_num = comp_clean
        for word, num in self.WORD_TO_NUM.items():
            orig_clean_num = re.sub(rf'\b{word}\b', num, orig_clean_num)
            comp_clean_num = re.sub(rf'\b{word}\b', num, comp_clean_num)

        # 1. Validate Ranges and Directions
        # Patterns: between X and Y, from X to Y, X-Y, X to Y, from X up to Y, from Y down to X, $X to $Y
        range_pattern = r'\b(between|from)?\s*\$?(\d+(?:\.\d+)?)\s*(?:-|to|and|up to|down to)\s*\$?(\d+(?:\.\d+)?)\b'
        
        orig_ranges = list(re.finditer(range_pattern, orig_clean_num))
        for match in orig_ranges:
            prefix = match.group(1) or ""
            low_str = match.group(2)
            high_str = match.group(3)
            full_match = match.group(0)

            low_val = float(low_str)
            high_val = float(high_str)

            # Look for occurrences in compressed text
            comp_ranges = list(re.finditer(range_pattern, comp_clean_num))
            if not comp_ranges:
                # Range dropped
                return False

            range_found_correct = False
            for c_match in comp_ranges:
                c_low_str = c_match.group(2)
                c_high_str = c_match.group(3)
                c_full = c_match.group(0)

                c_low_val = float(c_low_str)
                c_high_val = float(c_high_str)

                # Check if direction or bounds were reversed
                if c_low_val == high_val and c_high_val == low_val:
                    # Reversed range bounds! (e.g., 5.0V to 3.3V instead of 3.3V to 5.0V)
                    return False
                    
                if "down to" in c_full and "up to" in full_match:
                    # Inverted scaling direction! (e.g. 10 down to 3 instead of 3 up to 10)
                    return False

                if c_low_val == low_val and c_high_val == high_val:
                    range_found_correct = True
                    break

            if not range_found_correct and len(comp_ranges) > 0:
                # Found matching range regex but values/order did not match
                return False

        # 2. Validate Numbers with Units / Scale (e.g., 10MB vs 100MB)
        unit_pattern = r'\b(\d+(?:\.\d+)?)\s*([a-zA-Z%]+)\b'
        orig_units = re.findall(unit_pattern, orig_clean_num)
        for val_str, unit in orig_units:
            if unit in ["a", "an", "the", "and", "or", "in", "to", "of", "is"]:
                continue
            # Search for value+unit in compressed
            matching_comp_units = re.findall(unit_pattern, comp_clean_num)
            # Find if unit exists with wrong value
            unit_found = False
            for c_val, c_unit in matching_comp_units:
                if c_unit == unit:
                    unit_found = True
                    if c_val != val_str:
                        # Value altered for this unit! (e.g., 100MB instead of 10MB)
                        return False
            if not unit_found and orig_units:
                # Unit dropped
                return False

        # 3. Validate Operators with Numbers
        operators = r'\b(exactly|at least|at most|maximum of|minimum of|limit of|max|min|less than|greater than)\b'
        op_pattern = rf'{operators}\s*(\d+(?:\.\d+)?)'

        op_synonyms = {
            "exactly": ["precisely", "strictly", "just"],
            "at least": ["minimum", "min", "no less than"],
            "at most": ["maximum", "max", "no more than"]
        }

        orig_ops = re.findall(op_pattern, orig_clean_num)
        for op, val in orig_ops:
            syns = op_synonyms.get(op.lower(), [])
            occurrences = [m.start() for m in re.finditer(rf'\b{re.escape(val)}\b', comp_clean_num)]
            if not occurrences:
                return False

            op_preserved = False
            for idx in occurrences:
                preceding = comp_clean_num[max(0, idx-25):idx].strip()
                if op in preceding or any(syn in preceding for syn in syns):
                    op_preserved = True
                    break
            if not op_preserved:
                return False

        # 4. Validate Standalone Numbers with Context Noun Binding
        orig_numbers = re.findall(r'\b\d+(?:\.\d+)?\b', orig_clean_num)
        comp_numbers = re.findall(r'\b\d+(?:\.\d+)?\b', comp_clean_num)

        for num in orig_numbers:
            if num not in comp_numbers:
                return False
                
            orig_match = re.search(rf'\b{re.escape(num)}\b', orig_clean_num)
            if orig_match:
                start = orig_match.end()
                following_words = re.findall(r'\b\w+\b', orig_clean_num[start:start+35])
                target_nouns = [w for w in following_words if len(w) >= 3 and w not in ["and", "the", "for", "with", "that", "this"]]
                if target_nouns:
                    target_noun = target_nouns[0]
                    comp_match = re.search(rf'\b{re.escape(num)}\b', comp_clean_num)
                    if comp_match:
                        c_start = comp_match.end()
                        comp_following = comp_clean_num[c_start:c_start+45]
                        if target_noun not in comp_following and target_noun[:4] not in comp_following:
                            return False

        return True
