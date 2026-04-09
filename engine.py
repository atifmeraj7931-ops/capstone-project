class RefactorEngine:
    def __init__(self, code_str):
        self.original_code = code_str
        self.current_code = code_str

    def apply_updates(self, plan):
        operations = plan.get("operations", [])
        logs = []

        for op in operations:
            if not isinstance(op, dict): continue

    
            if op.get('type') == 'replace_block':
                target = op.get('target_code')
                optimized = op.get('optimized_code')
                
                if target and optimized:
                    if self._replace_block_smart(target, optimized):
                        logs.append("✅ Optimized Logic Block")
                    else:
                        logs.append(f"⚠️ Could not locate block to replace.")


            elif op.get('type') == 'rename':
                old = op.get('old_name')
                new = op.get('new_name')
                if old and new:
                    self.current_code = self.current_code.replace(old, new)
                    logs.append(f"Renamed '{old}' -> '{new}'")

        return self.current_code, logs

    def _replace_block_smart(self, target_str, replacement_str):
        """
        Finds target_str in current_code by matching line-by-line,
        ignoring indentation differences.
        """
        source_lines = self.current_code.splitlines()
        target_lines = target_str.strip().splitlines()
        
        if not target_lines: return False

        clean_target = [line.strip() for line in target_lines if line.strip()]
        

        for i in range(len(source_lines)):

            match_found = True
            matched_lines_count = 0
            

            source_idx = i
            target_idx = 0
            
            while target_idx < len(clean_target):
                if source_idx >= len(source_lines):
                    match_found = False
                    break
                
                src_line_clean = source_lines[source_idx].strip()
                
                
                if not src_line_clean:
                    source_idx += 1
                    continue
                

                if src_line_clean != clean_target[target_idx]:
                    match_found = False
                    break
                
                source_idx += 1
                target_idx += 1
            
            if match_found and target_idx == len(clean_target):
               
                new_source = source_lines[:i]
                
                new_source.append(replacement_str)
                
                new_source.extend(source_lines[source_idx:])
                
                self.current_code = "\n".join(new_source)
                return True

        return False