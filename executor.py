import subprocess
import tempfile
import os
import sys
import re

def execute_code(code, language, stdin=""):
    """
    Executes Python, JavaScript, Java, and C++ locally using system compilers.
    """
    try:
        # Create an isolated temporary directory for the files
        with tempfile.TemporaryDirectory() as tmpdir:
            
            # --- 1. PYTHON ---
            if language == "Python":
                filepath = os.path.join(tmpdir, "script.py")
                with open(filepath, "w", encoding="utf-8") as f: f.write(code)
                cmd = [sys.executable, filepath]
                
            # --- 2. JAVASCRIPT ---
            elif language == "JavaScript":
                filepath = os.path.join(tmpdir, "script.js")
                with open(filepath, "w", encoding="utf-8") as f: f.write(code)
                cmd = ["node", filepath]
                
            # --- 3. C++ ---
            elif language == "C++":
                filepath = os.path.join(tmpdir, "main.cpp")
                exe_path = os.path.join(tmpdir, "main.exe" if os.name == 'nt' else "main.out")
                with open(filepath, "w", encoding="utf-8") as f: f.write(code)
                
                # C++ Requires Compilation First
                comp = subprocess.run(["g++", filepath, "-o", exe_path], capture_output=True, text=True)
                if comp.returncode != 0:
                    return f"C++ Compilation Error:\n{comp.stderr}"
                cmd = [exe_path]

            # --- 4. JAVA ---
            elif language == "Java":
                # Java is strict: The file name MUST match the 'public class' name.
                match = re.search(r'public\s+class\s+(\w+)', code)
                class_name = match.group(1) if match else "Main"
                filepath = os.path.join(tmpdir, f"{class_name}.java")
                
                with open(filepath, "w", encoding="utf-8") as f: f.write(code)
                
                # Java Requires Compilation First
                comp = subprocess.run(["javac", filepath], capture_output=True, text=True)
                if comp.returncode != 0:
                    return f"Java Compilation Error:\n{comp.stderr}"
                cmd = ["java", "-cp", tmpdir, class_name]

            else:
                return f"Language {language} is not currently supported in the sandbox."

            # --- EXECUTION PHASE ---
            try:
                # Run the command with a 5-second timeout limit
                res = subprocess.run(cmd, input=stdin, capture_output=True, text=True, timeout=5)
                output = res.stdout + res.stderr
                return output.strip() if output.strip() else "Execution finished with no output."
                
            except FileNotFoundError:
                tool = cmd[0]
                return f"Environment Error: '{tool}' is not installed on your computer or not added to your system PATH."
            except subprocess.TimeoutExpired:
                return "Error: Execution timed out (Possible infinite loop detected and killed)."

    except Exception as e:
        return f"Sandbox System Error: {str(e)}"