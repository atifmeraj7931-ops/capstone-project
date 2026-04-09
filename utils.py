from openai import OpenAI
import json

def process_code(code_input, language, optimization_goal):
    """
    Sends the code to the AI and parses the JSON response.
    """
    from prompts import get_system_prompt, get_refactoring_prompt
    
    
    my_api_key = "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" 
    
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=my_api_key
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