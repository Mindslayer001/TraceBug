from dotenv import load_dotenv
load_dotenv()
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

if not client.api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")


# -------------- GPT Query Function --------------
# This function sends a prompt to the GPT model and returns the response.
# It uses the Groq client to interact with the GPT-4 model.
# The prompt includes a system message to set the context for the model as an expert Python code reviewer and AI debugger.
# The temperature is set to 0.3 for more deterministic responses.
def query_gpt(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert Python code reviewer, AI debugger, and the senior-most Quality Assurance Engineer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# -------------- Main Debugging Logic --------------
def debug_code(risks):
    result = []
    for lineno, snippet in risks:
        prompt = f"""
                Line {lineno} in the code contains this risky snippet:
```python
{snippet}
```
Please:

    Clearly explain any runtime risks, logic flaws, or security vulnerabilities this snippet may cause.

    Provide a corrected, production-safe version of the code by inserting it above the original snippet as Python comments, so the faulty code remains visible for comparison.

    At the top of the response, add a severity Issue Level with one of: Low, Medium, or High, based on the risk, exploitability, or potential for production failure.

    Highlight any edge cases, assumptions, or test scenarios that should be considered when using or refactoring this snippet.

    Keep the explanation concise and beginner-friendly where possible, but technically accurate.

    This is not one of those "AI generated code" prompts, so please do not mention that.

    This is not a code generation prompt, so please do not generate any code that is not directly related to the snippet.

    Strictly focus on generating a markdown-formatted response that addresses all the points mentioned.

EExample Input

Line 42 contains this snippet:

eval(user_input)

Example Response
'''
# Issue Level: High 

# Risk Explanation:
Using `eval()` on untrusted user input is highly dangerous. It allows execution of arbitrary Python code, which may lead to security breaches, data loss, or remote code execution. Even seemingly benign input can exploit system access or leak sensitive data.
```python
-> Edge Cases & Test Scenarios:
    - Input is a valid literal (e.g., '123', '[1, 2, 3]') → should succeed.
    - Input is invalid (e.g., 'os.system("rm -rf /")') → should raise an error or be blocked.
    - Input is a malicious payload disguised as data → verify safe parsing.
    - Always test with strict input validation if literal_eval is not feasible.
-> Best Alternatives
    - Safe alternative using literal_eval to avoid executing arbitrary code
'''

# Corrected Code:
# from ast import literal_eval
# user_data = literal_eval(user_input) 
eval(user_input)
```
                """
        print(f"\n🔍 Analyzing line {lineno}...")
        response = query_gpt(prompt)
        result.append(f"Line {lineno}:\n{response}\n")
        print(response)
    if result:
        return result
    return "No risks found in the provided code snippet."