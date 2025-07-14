# TraceBug: AI-Powered Code Risk Analyzer

![Build](https://img.shields.io/badge/build-passing-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.11-blue) ![Node](https://img.shields.io/badge/node-20.x-brightgreen) ![Frontend](https://img.shields.io/badge/frontend-Vite+React-blueviolet) ![Backend](https://img.shields.io/badge/backend-FastAPI-orange)

**TraceBug** is an intelligent static analysis tool that detects and fixes risky code patterns in Python. It combines traditional Abstract Syntax Tree (AST) analysis with the advanced reasoning capabilities of Large Language Models (LLMs) to provide deep, context-aware code reviews.

## 🚀 Overview

This tool automates the code review process by:

1. **Pre-analysis with AST:** First, it parses the input Python code into an Abstract Syntax Tree (AST). It then traverses this tree to find a wide range of predefined potential risks, from security vulnerabilities to runtime errors and bad practices.
2. **Targeted LLM Judgment:** If specific risks are identified, the relevant code snippets are sent to a Large Language Model (Groq Llama 3). A detailed prompt asks the LLM to act as a senior engineer, providing a severity level, a clear explanation of the vulnerability, and a production-safe code correction.
3. **General LLM Fallback:** If the initial AST scan finds no specific issues, the entire code's AST is sent to the LLM for a more general, holistic review.
4. **Interactive Frontend:** Results are displayed in a clean, developer-friendly web UI, with markdown rendering, syntax highlighting, and copy-to-clipboard functionality.

TraceBug is built to be a security-focused, extensible, and user-friendly DevSecOps tool.

## ✨ Features

- **Comprehensive AST-based Risk Detection:**
	  - **Security:** Detects `eval()` usage, command injection (`shell=True`), dangerous imports (`os`, `pickle`), hardcoded secrets, and potential SQL injection.
	  - **Runtime Errors:** Finds division-by-zero risks, variable unpacking mismatches, and usage of undefined variables.
	  - **Bad Practices:** Identifies broad or empty `except` clauses, built-in name shadowing, infinite loops, deep nesting, and more.
- **LLM Integration:** Utilizes the Groq API (Llama 3 model) for intelligent code analysis and generation of human-like feedback.
- **AI-Generated Explanations & Fixes:** Provides clear, actionable feedback including severity levels (High/Medium/Low), risk explanations, and corrected code snippets.
- **Interactive Web UI:** A modern frontend built with React, TypeScript, and Vite, featuring a code editor, file uploads, and a formatted results view.
- **Modular Backend:** A robust backend powered by FastAPI, ensuring high performance and easy extensibility.

## 🏗️ Project Structure

```

.  
├── backend/  
│ ├── app/  
│ │ ├── core/ # FastAPI configuration and settings  
│ │ ├── routes/ # API endpoints (code analysis, health checks)  
│ │ ├── utils/ # Core logic: AST parsing (riskAnalyzer.py) & LLM interaction (grok.py)  
│ │ └── main.py # FastAPI application entrypoint  
│ ├── pyproject.toml # Python dependencies  
│ └── .env_example # Environment variable template  
└── frontend/  
├── src/  
│ ├── components/ # React components (Code Editor, Results Display, etc.)  
│ ├── App.tsx # Main application component  
│ └── main.tsx # Application entrypoint  
├── package.json # Node.js dependencies  
└── vite.config.ts # Vite configuration

```

## ⚙️ Setup and Installation

### Prerequisites

- **Node.js** (v20.x or later)
- **Python** (v3.12 or later)
- **Poetry** for Python package management

---

### 📦 Backend (FastAPI)

1. **Navigate to the backend directory:**

    ```bash
        cd backend
    ```

2. **Create and configure the environment file:**
    - Copy the example `.env` file:

    ```bash
        cp .env_example .env
    ```

    - Open the `.env` file and add your Groq API key and the allowed CORS origin for the frontend:

    ```bash
        TOGETHER_API_KEY="your-together-api-key"
        CORS_ORIGINS="http://localhost:5173"
    ```

3. **Install dependencies using Poetry:**

    ```bash
        poetry install
    ```

4. **Activate the virtual environment and run the server:**

    ```bash
        poetry shell
        uvicorn app.main:app --reload
    ```

The backend API will be running at `http://127.0.0.1:8000`.

---

### 💻 Frontend (React + Vite)

1. **Navigate to the frontend directory:**

    ```bash
        cd frontend
    ```

2. **Create the environment file:**
    - Create a new file named `.env` in the `frontend/` directory.
    - Add the following line to specify the backend API URL:

    ```env
        VITE_API_URL=http://127.0.0.1:8000
    ```

3. **Install dependencies using npm:**

    ```bash
        npm install
    ```

4. **Run the development server:**

    ```bash
        npm run dev
    ```

The frontend application will be available at `http://localhost:5173`.

## 🚀 Usage

1. Ensure both the backend and frontend servers are running.
2. Open your web browser and navigate to `http://localhost:5173`.
3. Paste your Python code into the editor on the left or use the "Upload File" button.
4. Click the "Analyze Code" button.
5. View the detailed, AI-generated analysis in the results panel on the right.

## 🧪 Tests

TBD: Pytest support for AST logic and React Testing Library tests for UI components are planned for future releases.

## 🤝 Contributing

We welcome contributions! If you're interested in improving TraceBug, please consider:

- Adding new risk detection patterns to `riskAnalyzer.py`.
- Enhancing the prompts in `grok.py` for better LLM responses.
- Improving the frontend UI/UX.
- Adding support for more programming languages.

Feel free to open an issue or submit a pull request.

## 📬 Contact

For collaboration or inquiries, please reach out via email at [buildwithmani.dev@gmail.com](mailto:buildwithmani.dev@gmail.com) or connect on [GitHub](https://github.com/Mindslayer001).

## 🛡️ License

This project is licensed under the MIT License. See the LICENSE file for details.

---

© 2025 MindSlayer001