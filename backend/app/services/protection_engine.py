import re
from typing import Tuple, Dict

class ProtectionEngine:
    """Masks high-risk structured components with placeholders and restores them."""
    
    def mask(self, text: str) -> Tuple[str, Dict[str, str]]:
        if not text:
            return "", {}
            
        mapping = {}
        masked_text = text
        
        # Helper to extract balanced character blocks (curly braces or square brackets)
        def extract_balanced_blocks(s, open_char='{', close_char='}'):
            blocks = []
            start = -1
            count = 0
            for idx, char in enumerate(s):
                if char == open_char:
                    if count == 0:
                        start = idx
                    count += 1
                elif char == close_char:
                    if count > 0:
                        count -= 1
                        if count == 0 and start != -1:
                            blocks.append(s[start:idx+1])
            return blocks
            
        # 1. Code blocks (do first to avoid double masking)
        code_blocks = re.findall(r'(```[\s\S]*?```)', masked_text)
        for i, block in enumerate(code_blocks):
            placeholder = f"__ST_PROTECT_CODE_{i}__"
            mapping[placeholder] = block
            masked_text = masked_text.replace(block, placeholder, 1)
            
        # 2. Markdown tables
        tables = re.findall(r'(\|\s*[^\r\n|]+\s*\|\r?\n\|\s*[-:| ]+\s*\|\r?\n(?:\|\s*[^\r\n|]+\s*\|\r?\n?)+)', masked_text)
        for i, table in enumerate(tables):
            placeholder = f"__ST_PROTECT_TABLE_{i}__"
            mapping[placeholder] = table
            masked_text = masked_text.replace(table, placeholder, 1)
            
        # 3. JSON blocks (balanced outer curly braces)
        json_objs = extract_balanced_blocks(masked_text, '{', '}')
        for i, block in enumerate(json_objs):
            if ':' in block:  # heuristic to verify it's a JSON block
                placeholder = f"__ST_PROTECT_JSON_{i}__"
                mapping[placeholder] = block
                masked_text = masked_text.replace(block, placeholder, 1)
                
        # 4. JSON arrays (balanced outer square brackets)
        json_arrs = extract_balanced_blocks(masked_text, '[', ']')
        for i, block in enumerate(json_arrs):
            if ',' in block or ':' in block:
                placeholder = f"__ST_PROTECT_JSON_ARR_{i}__"
                mapping[placeholder] = block
                masked_text = masked_text.replace(block, placeholder, 1)
                
        # 5. XML blocks
        xml_blocks = re.findall(r'(<([a-zA-Z0-9]+)\b[^>]*>[\s\S]*?<\/\2>)', masked_text)
        for i, match in enumerate(xml_blocks):
            block = match[0]
            placeholder = f"__ST_PROTECT_XML_{i}__"
            mapping[placeholder] = block
            masked_text = masked_text.replace(block, placeholder, 1)
            
        # 6. URLs
        urls = re.findall(r'(https?://[^\s\)\"\'\>]+)', masked_text)
        urls = sorted(list(set(urls)), key=len, reverse=True)
        for i, url in enumerate(urls):
            placeholder = f"__ST_PROTECT_URL_{i}__"
            mapping[placeholder] = url
            masked_text = masked_text.replace(url, placeholder)
            
        # 7. SQL
        sql_keywords = re.findall(r'\b(select|insert|update|delete|create table)\b', masked_text, re.IGNORECASE)
        for i, kw in enumerate(sql_keywords):
            start_idx = masked_text.lower().find(kw.lower())
            if start_idx != -1:
                end_idx = masked_text.find(';', start_idx)
                if end_idx != -1:
                    full_sql = masked_text[start_idx:end_idx+1]
                    placeholder = f"__ST_PROTECT_SQL_{i}__"
                    mapping[placeholder] = full_sql
                    masked_text = masked_text.replace(full_sql, placeholder, 1)
                    
        # 8. File paths
        paths = re.findall(r'\b([a-zA-Z]:\\[\\\w\s.-]+|/[/\w\s.-]+)\b', masked_text)
        paths = sorted(list(set(paths)), key=len, reverse=True)
        for i, path in enumerate(paths):
            if len(path) > 3:
                placeholder = f"__ST_PROTECT_PATH_{i}__"
                mapping[placeholder] = path
                masked_text = masked_text.replace(path, placeholder)
                
        return masked_text, mapping
        
    def unmask(self, text: str, mapping: Dict[str, str]) -> str:
        restored = text
        for placeholder, original in mapping.items():
            restored = restored.replace(placeholder, original)
        return restored
        
    def validate_placeholders(self, text: str, mapping: Dict[str, str]) -> bool:
        for placeholder in mapping.keys():
            if text.count(placeholder) != 1:
                return False
        return True

