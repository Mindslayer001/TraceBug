# 🔍 TraceBug - fix bugs before they bite.

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/github/license/yourusername/ast-llm-analyzer)

![Python](https://img.shields.io/badge/python-3.11-blue)

![Node](https://img.shields.io/badge/node-20.x-brightgreen)

![Frontend](https://img.shields.io/badge/frontend-Vite+React-blueviolet)
![Backend](https://img.shields.io/badge/backend-FastAPI-orange)

> AI-powered risk analyzer using Python AST + LLMs. Intelligently finds, annotates, and corrects risky code by analyzing AST and feeding it to an LLM for judgment.

---

## 🚀 Overview

> TraceBug is an AI-powered static analyzer for Python that detects and fixes risky patterns using AST and LLMs—currently focused on unit-level code, with future plans to support integration-level analysis..

This project automatically:
- Parses Python code using AST
- Identifies patterns with potential risks
- Sends these AST structures to an LLM (like GPT)
- Receives structured risk-level feedback and corrections
- Serves results through a web UI

🔒 Security-focused.  
> Built with secure defaults and extensible risk rules, TraceBug can evolve into an LLM-powered **DevSecOps tool**.

🧠 LLM-enhanced.  
🎨 Developer-friendly UX.

---

## 🧠 Features

- ✅ Python AST parsing
- ✅ Risk-level classification (High / Medium / Low)
- ✅ LLM integration for code understanding
- ✅ Suggests safer alternatives & corrections
- ✅ React frontend for code input and review
- ✅ FastAPI backend API with modular structure
- ✅ Handles edge cases like race conditions, TOCTOU bugs, file I/O risks, etc.

---

## 🏗️ Project Structure

```

.  
├── backend  
│ ├── app  
│ │ ├── core # Configurations  
│ │ ├── routes # CodePayload and health API  
│ │ ├── utils # AST parsing and risk analysis logic  
│ │ └── main.py # FastAPI entrypoint  
│ ├── poetry.lock / pyproject.toml  
├── frontend  
│ ├── components # React UI (Code sender, viewer)  
│ ├── App.tsx # Root app  
│ └── vite.config.ts # Vite + TypeScript setup

```

---

## ⚙️ Setup Instructions

### 📦 Backend (Python 3.11 + FastAPI)

```bash
cd backend
poetry install
poetry shell
uvicorn app.main:app --reload
```

> LLM API keys should be configured in `app/core/config.py` or via `.env`



### 💻 Frontend (React + TypeScript + Vite)

```bash
cd frontend
npm install
npm run dev
```

> React app runs at `http://localhost:5173`

---

## 🧪 Example Usage

1. Paste Python code in the IDE

2. Submit

3. View LLM-generated feedback:

	- Risk level (High / Medium / Low)

    - Vulnerability description
    
    - Suggested corrections
    

---

## 🧠 How It Works

1. **AST Parsing**
    
    - Code is parsed using `ast.parse()`
    
    - Transformed into an intermediate representation
    
2. **Risk Detection**
    
    - Patterns (e.g., `os.remove`, `try...except:`, `threading`, `open()` misuse) are matched
        
    - AST and code snippet sent to LLM with a prompt
        
3. **LLM Judgment**
    
    - Receives structured JSON:
        
        ```json
        {
          "line": 42,
          "risk": "High",
          "explanation": "...",
          "fix": "use 'with open(...) as f'"
        }
        ```
        
4. **Frontend Display**
    
    - Highlights vulnerable lines

    

---

## 🧪 Tests

_TBD: Add Pytest support for AST logic and React unit tests for components._

---

## 🛡️ License

MIT License. © 2025 Mani Sankar Chintagunti

---

## 🤝 Contributing

We welcome contributions, especially in:

- 🧪 Adding more risk rule patterns

- 🌐 Enhancing multilingual code support

- 🧠 Prompt engineering & LLM fine-tuning


---

## 📬 Contact

If you want to collaborate, reach out via [buildwithmani.dev@gmail.com](mailto:buildwithmani.dev@gmail.com) or open an issue.

