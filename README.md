---
noteId: "ed6c6e80095211f09720858bf73c56d1"
tags: []

---

# Carbon Crunch 🌿

> A powerful code quality analyzer that evaluates your React, JavaScript, and Python code against best practices and provides actionable recommendations for improvement.

[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-enabled-success)](https://github.com/features/actions)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB)](https://reactjs.org/)
[![LangChain](https://img.shields.io/badge/LangChain-enabled-blue)](https://www.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="https://github.com/username/carbon-crunch/raw/main/docs/assets/carbon-crunch-logo.png" alt="Carbon Crunch Logo" width="200"/>
</p>
![Uploading Screenshot 2025-03-25 at 1.48.22 PM (2).png…]()

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [GitHub Actions Setup](#github-actions-setup)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Web Interface](#web-interface)
  - [Command Line](#command-line)
  - [GitHub Integration](#github-integration)
- [Example Analysis](#example-analysis)
- [Contributing](#contributing)
- [License](#license)

---

## 🔍 Overview

Carbon Crunch is a comprehensive code quality analyzer that helps developers write cleaner, more maintainable code. It uses advanced language models to evaluate code against industry best practices and provides detailed feedback with actionable recommendations for improvement.

The tool can analyze:
- Python (`.py`) files
- JavaScript (`.js`) files
- React/JSX (`.jsx`) files

---

## ✨ Features

- **Comprehensive Code Analysis**: Evaluates code based on six key criteria (naming, modularity, documentation, formatting, reusability, and best practices)
- **Detailed Scoring**: Provides both an overall score and a breakdown by category
- **Actionable Recommendations**: Offers specific, clear recommendations for improving your code
- **Multiple Interfaces**: Access via web UI, API, or command line
- **GitHub Integration**: Automatically analyze code in PRs and commits
- **Fast and Accurate**: Powered by LangChain and state-of-the-art language models

---

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Node.js 14+ (for frontend)
- OpenAI API Key
- Git (for GitHub integration)

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/carbon-crunch.git
   cd carbon-crunch
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. **Start the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at http://localhost:8000.

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd carbon-crunch-frontend
   ```

2. **Install dependencies**:
   ```bash
 
   npm init -y

 
   npm install react react-dom
   npm install -D vite @vitejs/plugin-react
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```
   The web interface will be available at http://localhost:5173.

### GitHub Actions Setup

To enable automatic code quality checks on your GitHub repository:

1. **Copy the GitHub workflow file** to your repository:
   ```bash
   mkdir -p .github/workflows
   cp path-to-carbon-crunch/.github/workflows/code-quality.yml .github/workflows/
   ```

2. **Add your OpenAI API key** as a GitHub secret:
   - Go to your repository on GitHub
   - Navigate to Settings > Secrets and variables > Actions
   - Click "New repository secret"
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key

3. **Push your changes** to GitHub to activate the workflow.

---

## 📊 Usage

### API Endpoints

Once the FastAPI server is running, you can access:

- **API Documentation**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/openapi.json

#### Example: Analyzing a File via API

```bash
curl -X 'POST' \
  'http://localhost:8000/analyze/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/file.py' \
  -F 'model=gpt-3.5-turbo'
```

### Web Interface

The web interface provides a user-friendly way to analyze code:

1. Navigate to http://localhost:5173
2. Upload a file or paste your code
3. Choose the OpenAI model to use for analysis
4. View the detailed analysis results

### Command Line

You can also analyze files directly from the command line:

```bash
python code-analyzer.py /path/to/your/file.py --model gpt-3.5-turbo --save
```

Options:
- `--model`: Specify which OpenAI model to use (default: gpt-4)
- `--save`: Save the analysis to a JSON file

### GitHub Integration

Once set up, the GitHub Actions workflow will:

1. Run automatically on pull requests and pushes to main/master
2. Analyze all modified code files
3. Post the analysis results as a comment on the PR or commit
4. Upload detailed analysis as workflow artifacts

---

## 🔄 Example Analysis

Here's an example of the analysis results for a Python file:

```json
{
  "overall_score": 70,
  "breakdown": {
    "naming": 7,
    "modularity": 13,
    "comments": 15,
    "formatting": 10,
    "reusability": 10,
    "best_practices": 15
  },
  "recommendations": [
    "Improve naming conventions by using snake_case for all variables and functions.",
    "Break down the 'process_data_file' function into smaller, more focused functions.",
    "Add docstrings to all functions, especially 'badFunc' and 'messy_function'.",
    "Ensure consistent code formatting by using 4 spaces for indentation.",
    "Refactor 'calculate_areas' function to avoid repeating code for different shapes."
  ]
}
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

Please make sure your code passes all tests and follows the project's coding standards.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by Your Team
</p>
