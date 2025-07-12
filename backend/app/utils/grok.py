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
            {"role": "system", "content": "You are an expert Python code reviewer and AI debugger and Senior most Quality Assurance Engineer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# -------------- Main Debugging Logic --------------
def debug_code(risks):
    for lineno, snippet in risks:
        prompt = f"""
Line {lineno} in the code contains this risky snippet:
```python
{snippet}
```

Please:
1. Explain potential runtime risks or logic errors.
2. Suggest a safe fix.
3. Mention edge cases if any.
"""
        print(f"\n🔍 Analyzing line {lineno}...")
        response = query_gpt(prompt)
        print(response)
        return response
    return "No risks found."