import subprocess
import os
import sys
import io

                                                      
def run_test_case(original_code, refactored_code, test_input, language):
    """
    Runs code in Python, JS, Java, or C++ using system tools.
    """

                              
    def prepare_code(code, input_call, lang):
        if lang == "Python":
            return code + f"\nprint({input_call})"
        elif lang == "JavaScript":
            return code + f"\nconsole.log({input_call});"
        elif lang == "Java":
            return f"""
            public class Main {{
                {code}
                public static void main(String[] args) {{
                    System.out.println({input_call});
                }}
            }}
            """
        elif lang == "C++":
            return f"""
            #include <iostream>
            #include <vector>
            #include <string>
            #include <algorithm>
            using namespace std;
            {code}
            int main() {{
                cout << {input_call} << endl;
                return 0;
            }}
            """
        return code

                                  
    def execute(code, lang):
        try:
            if lang == "Python":
                captured = io.StringIO()
                sys.stdout = captured
                exec(code, {}, {})
                sys.stdout = sys.__stdout__
                return captured.getvalue().strip()

            elif lang == "JavaScript":
                with open("temp.js", "w") as f: f.write(code)
                result = subprocess.run(["node", "temp.js"], capture_output=True, text=True, shell=True)
                return result.stdout.strip()

            elif lang == "Java":
                with open("Main.java", "w") as f: f.write(code)
                subprocess.run(["javac", "Main.java"], capture_output=True, shell=True)
                run_res = subprocess.run(["java", "Main"], capture_output=True, text=True, shell=True)
                return run_res.stdout.strip()

            elif lang == "C++":
                with open("temp.cpp", "w") as f: f.write(code)
                subprocess.run(["g++", "temp.cpp", "-o", "temp.exe"], capture_output=True, shell=True)
                run_res = subprocess.run(["temp.exe"], capture_output=True, text=True, shell=True)
                return run_res.stdout.strip()

        except Exception as e:
            return f"Error: {str(e)}"

                           
    ready_original = prepare_code(original_code, test_input, language)
    ready_refactored = prepare_code(refactored_code, test_input, language)
    
    out_1 = execute(ready_original, language)
    out_2 = execute(ready_refactored, language)
    
    return {
        "match": out_1 == out_2,
        "original_output": out_1,
        "refactored_output": out_2
    }