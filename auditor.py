import os
import pathlib
from openai import OpenAI
import json


def load_dotenv():
    env_path = pathlib.Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if not line or line.strip().startswith("#"):
                continue
            key, sep, value = line.partition("=")
            if sep:
                os.environ.setdefault(key.strip(), value.strip())


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set. Add it to .env or your environment.")

client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)
def analyze_code(code, optimization_type, language="Python"):
    

    if optimization_type == "Readability & Clean Code":
        focus = "Variable Naming, Docstrings, and formatting."
    elif optimization_type == "Performance (Time Complexity)":
        focus = "Big O efficiency. Detect nested loops."
    elif optimization_type == "Memory Efficiency (Space)":
        focus = "Reduce memory usage."
    elif optimization_type == "Security Hardening":
        focus = "Vulnerabilities and injection risks."
    else:
        return {"error": "Unknown type"}

    
    prompt = f"""
    Act as a Lead Software Architect.
    
    STEP 1: LANGUAGE VALIDATION (CRITICAL)
    You are analyzing code that is claimed to be: **{language}**.
    - If the code is clearly in a different language (e.g., Java syntax with 'public static void' but user selected Python), STOP.
    - Return {{ "error": "Language Mismatch: You pasted [Actual Language] code but selected {language}." }}

    STEP 2: ANALYSIS (Only if Valid)
    Analyze the code for: **{optimization_type}**.
    
    Instructions:
Instructions:
    1. Identify specific blocks of code to refactor.
    2. Create a JSON plan with a list of "operations".
    3. CRITICAL: For "target_code", copy the text EXACTLY from the input (preserve spaces/comments) so my script can find it.
    4. CRITICAL: For "optimized_code", YOU MUST PRESERVE THE EXACT INDENTATION of the target block! If the original code is indented by 4 spaces, your optimized code MUST also be indented by 4 spaces. Python will crash if you drop the indentation.    
    
    SCORING RULES (CRITICAL):
    - Rate the ORIGINAL code strictly (e.g., if O(n^2), give 30-50).
    - Rate the REFACTORED code generously (e.g., if O(n), give 90-100).
    - The "refactored" score MUST be higher than "original".

    Return JSON with:
    - "operations": List of objects {{ "type": "replace_block", "target_code": "...", "optimized_code": "..." }}
    - "explanation": Summary of changes.
    - "scores": {{ "original": int, "refactored": int }}

    CODE TO ANALYZE:
    {code}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}