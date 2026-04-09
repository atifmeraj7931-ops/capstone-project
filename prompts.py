def get_system_prompt():
    return """
    You are an expert Senior Software Engineer and Lead Code Reviewer. 
    Your goal is to refactor code to be production-ready, efficient, and clean.
    
    You must always output a valid JSON object.
    """

def get_refactoring_prompt(language, goal, user_code):
    return f"""
    Refactor the following {language} code.
    
    
    {goal}
    

    1. Analyze the original code quality and assign a score (0-100).
    2. Refactor the code to improve it based on the specific GOAL.
    3. Assign a new score (0-100) to the refactored code.
    4. Briefly explain the complexity (Time/Space) if relevant.
    
    
    Return ONLY a raw JSON object with no markdown formatting. Use this exact schema:
    {{
        "original_code_score": <int>,
        "refactored_code_score": <int>,
        "refactored_code": "<string representation of the code>",
        "changes_made": [
            "<string explanation of change 1>",
            "<string explanation of change 2>"
        ],
        "complexity_analysis": "<string>"
    }}
    

    {user_code}
    """