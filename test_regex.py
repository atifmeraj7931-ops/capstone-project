import re

# This is a real Unit Test!
java_code = "public class MyDemoTest { public static void main() {} }"
match = re.search(r'public\s+class\s+(\w+)', java_code)

assert match.group(1) == "MyDemoTest", "Regex failed to find the class name!"
print("Unit Test Passed: Java Class Name Extracted Perfectly.")