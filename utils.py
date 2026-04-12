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


def process_code(code_input, language, optimization_goal):
    """
    Sends the code to the AI and parses the JSON response.
    """
    from prompts import get_system_prompt, get_refactoring_prompt
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set. Add it to .env or your environment.")
    
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )
    
    
    system_prompt = get_system_prompt()
    user_prompt = get_refactoring_prompt(language, optimization_goal, code_input)
    
    try:
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}, 
            temperature=0.2 
        )
        

        result_json = json.loads(response.choices[0].message.content)
        return result_json

    except Exception as e:
        return {"error": str(e)}