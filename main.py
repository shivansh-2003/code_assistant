from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks, HTTPException, Depends, Path
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import tempfile
import os
import uuid
import json
import shutil
from pydantic import BaseModel

# Import the code analyzer function - fixed import for code-analyzer.py
# Note: The import has been changed to match the hyphenated filename
import sys
import importlib.util

# Dynamically import the code_analyzer module from code-analyzer.py
spec = importlib.util.spec_from_file_location("code_analyzer", "code-analyzer.py")
code_analyzer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(code_analyzer)

# Now we can access the analyze_code function
analyze_code = code_analyzer.analyze_code

app = FastAPI(
    title="Code Quality Analyzer API",
    description="API for analyzing code quality across multiple programming languages",
    version="1.0.0"
)

# Directory to store temporary uploaded files
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

# Model for analysis results to document the response structure
class AnalysisResult(BaseModel):
    overall_score: int
    breakdown: dict
    recommendations: list[str]

@app.post("/analyze/", response_model=AnalysisResult, 
         summary="Analyze code quality", 
         description="Upload a code file to analyze its quality based on best practices")
async def analyze_code_endpoint(
    file: UploadFile = File(...),
    model: str = Form("gpt-3.5-turbo")
):
    """
    Analyze code quality from an uploaded file.
    
    - **file**: The code file to analyze (.py, .js, or .jsx)
    - **model**: The OpenAI model to use for analysis (default: gpt-3.5-turbo)
    
    Returns an analysis with overall score, breakdown, and recommendations.
    """
    # Validate file extension
    filename = file.filename
    extension = os.path.splitext(filename)[1].lower()
    
    if extension not in [".py", ".js", ".jsx"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {extension}. Supported types: .py, .js, .jsx"
        )
    
    # Create a unique temporary file path
    temp_file_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}{extension}")
    
    try:
        # Save the uploaded file
        with open(temp_file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
        
        # Analyze the code
        results = analyze_code(temp_file_path, model_name=model)
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/analyze/path/", response_model=AnalysisResult,
         summary="Analyze code at a specific file path",
         description="Analyze code at a given file path (for server-side files)")
async def analyze_path(
    file_path: str = Form(...),
    model: str = Form("gpt-3.5-turbo")
):
    """
    Analyze code quality from a file at a specified path.
    
    - **file_path**: The path to the code file to analyze (.py, .js, or .jsx)
    - **model**: The OpenAI model to use for analysis (default: gpt-3.5-turbo)
    
    Returns an analysis with overall score, breakdown, and recommendations.
    """
    # Validate file exists
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {file_path}"
        )
    
    # Validate file extension
    extension = os.path.splitext(file_path)[1].lower()
    if extension not in [".py", ".js", ".jsx"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {extension}. Supported types: .py, .js, .jsx"
        )
    
    try:
        # Analyze the code
        results = analyze_code(file_path, model_name=model)
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health", summary="Check API health")
async def health_check():
    """Check if the API is running."""
    return {"status": "healthy"}

@app.get("/models", summary="List available models")
async def get_models():
    """Get a list of available models for code analysis."""
    return {
        "models": [
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Faster and more cost-effective"},
            {"id": "gpt-4", "name": "GPT-4", "description": "More accurate but slower and more expensive"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 