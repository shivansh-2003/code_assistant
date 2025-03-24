# Code Quality Analyzer API

A FastAPI application that provides an API for analyzing code quality across multiple programming languages (.py, .js, .jsx).

## Features

- Upload files for analysis
- Analyze code from server-side file paths
- Get detailed code quality analysis with scores and recommendations
- Support for multiple languages (Python, JavaScript, React/JSX)
- Choice of OpenAI models for analysis

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Start the server

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

### API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints

#### 1. Analyze code from uploaded file

```
POST /analyze/
```

**Parameters:**
- `file`: The code file to analyze (.py, .js, or .jsx)
- `model`: (optional) The OpenAI model to use (default: gpt-3.5-turbo)

**Example using curl:**

```bash
curl -X 'POST' \
  'http://localhost:8000/analyze/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/file.py' \
  -F 'model=gpt-3.5-turbo'
```

#### 2. Analyze code from server-side path

```
POST /analyze/path/
```

**Parameters:**
- `file_path`: The path to the code file to analyze (.py, .js, or .jsx)
- `model`: (optional) The OpenAI model to use (default: gpt-3.5-turbo)

**Example using curl:**

```bash
curl -X 'POST' \
  'http://localhost:8000/analyze/path/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'file_path=/path/to/your/file.py&model=gpt-3.5-turbo'
```

## Sample Response

```json
{
  "overall_score": 85,
  "breakdown": {
    "naming": 8,
    "modularity": 18,
    "comments": 17,
    "formatting": 14,
    "reusability": 13,
    "best_practices": 15
  },
  "recommendations": [
    "Add docstrings to all functions for better documentation",
    "Follow consistent naming conventions for variables",
    "Break down large functions into smaller, more focused ones",
    "Implement error handling for more robust code"
  ]
}
```

## Testing

You can test the API with the sample files provided in the repository:
- `test_code_analyzer.py` - Python test file
- `test_code_analyzer.js` - JavaScript test file
- `test_code_analyzer.jsx` - React/JSX test file

## License

MIT 