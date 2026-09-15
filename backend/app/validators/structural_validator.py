import re

class StructuralValidator:
    """
    Validates structural preservation of code blocks, JSON objects, URLs, file paths,
    agent tool names, schema fields, and explicit output format requirements.
    """
    
    def validate(self, original_text: str, compressed_text: str) -> bool:
        if not original_text:
            return True

        orig_clean = original_text.lower()
        comp_clean = compressed_text.lower()

        # 1. File Path Preservation (Windows & Linux paths)
        # Windows: C:\path\file.ext, Linux: /etc/path/file.ext
        win_path_re = r'[a-zA-Z]:\\[\w\.\-\\]+'
        linux_path_re = r'/(?:etc|tmp|var|usr|home|bin)/[\w\.\-/]+'
        
        orig_paths = re.findall(win_path_re, original_text) + re.findall(linux_path_re, original_text)
        for path in orig_paths:
            if path not in compressed_text:
                # File path missing or altered! (e.g. C:\Windows\System32\cmd.exe instead of C:\Users\...)
                return False

        # 2. Agent Tool Function Name Preservation
        # e.g., get_weather(location), delete_database()
        tool_re = r'\b([a-zA-Z_]\w*\([^\)]*\))'
        orig_tools = re.findall(tool_re, original_text)
        for tool in orig_tools:
            tool_name = tool.split('(')[0]
            if tool_name not in compressed_text:
                # Tool name altered or dropped!
                return False

        # 3. URL Preservation
        url_re = r'https?://[^\s/$.?#].[^\s]*'
        orig_urls = re.findall(url_re, original_text)
        for url in orig_urls:
            if url not in compressed_text:
                return False

        # 4. Code & JSON Blocks
        code_block_re = r'```[\s\S]*?```'
        orig_code_blocks = re.findall(code_block_re, original_text)
        comp_code_blocks = re.findall(code_block_re, compressed_text)
        if len(orig_code_blocks) > len(comp_code_blocks):
            return False

        # Inline JSON object preservation: {"key": value}
        json_obj_re = r'\{[\s\S]*?"[\w_]+"\s*:\s*[\s\S]*?\}'
        orig_json_objs = re.findall(json_obj_re, original_text)
        if orig_json_objs:
            comp_json_objs = re.findall(json_obj_re, compressed_text)
            if len(orig_json_objs) > len(comp_json_objs):
                # JSON object dropped!
                return False

        # 5. Output Format Requirement Preservation
        # e.g. "Return output strictly as valid JSON", "Format response as a Markdown table"
        if "valid json" in orig_clean or "strictly as json" in orig_clean or "json object" in orig_clean:
            if "freeform prose" in comp_clean or "plain text" in comp_clean:
                # Contradictory format!
                return False
                
        if "markdown table" in orig_clean:
            if "bullet list" in comp_clean and "markdown table" not in comp_clean:
                # Structural output requirement ignored!
                return False

        # 6. JSON Schema Fields Requirement
        # e.g. "Return JSON with fields name, age, and email."
        schema_re = r'\bfields\s+([\w\s,]+)\b'
        orig_schema_match = re.search(schema_re, orig_clean)
        if orig_schema_match:
            fields_str = orig_schema_match.group(1)
            required_fields = [f.strip() for f in re.split(r'[,and\s]+', fields_str) if len(f.strip()) >= 2]
            for field in required_fields:
                if field not in comp_clean:
                    # Required schema field dropped! (e.g. 'age' field missing)
                    return False

        return True
