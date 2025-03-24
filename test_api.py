#!/usr/bin/env python3
"""
Test script for the Code Quality Analyzer API.
This script demonstrates how to use the API to analyze code files.
"""

import requests
import argparse
import json
import os
from pprint import pprint

def test_file_upload(api_url, file_path, model="gpt-3.5-turbo"):
    """Test the file upload endpoint."""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return
    
    url = f"{api_url}/analyze/"
    
    files = {
        'file': (os.path.basename(file_path), open(file_path, 'rb'), 'text/plain')
    }
    
    data = {
        'model': model
    }
    
    print(f"Uploading {file_path} for analysis using model {model}...")
    
    try:
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        
        result = response.json()
        print("\nAnalysis Result:")
        print("=" * 50)
        print(f"Overall Score: {result['overall_score']}/100")
        
        print("\nBreakdown:")
        for category, score in result['breakdown'].items():
            print(f"  {category.capitalize()}: {score}")
        
        print("\nRecommendations:")
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None
    finally:
        files['file'][1].close()

def test_path_analysis(api_url, file_path, model="gpt-3.5-turbo"):
    """Test the file path endpoint."""
    url = f"{api_url}/analyze/path/"
    
    data = {
        'file_path': os.path.abspath(file_path),
        'model': model
    }
    
    print(f"Requesting analysis of {file_path} using model {model}...")
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        
        result = response.json()
        print("\nAnalysis Result:")
        print("=" * 50)
        print(f"Overall Score: {result['overall_score']}/100")
        
        print("\nBreakdown:")
        for category, score in result['breakdown'].items():
            print(f"  {category.capitalize()}: {score}")
        
        print("\nRecommendations:")
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Test the Code Quality Analyzer API")
    parser.add_argument("file_path", help="Path to the code file to analyze")
    parser.add_argument("--api-url", default="http://localhost:8000", help="Base URL of the API")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="OpenAI model to use")
    parser.add_argument("--method", choices=["upload", "path"], default="upload", help="API method to test")
    
    args = parser.parse_args()
    
    if args.method == "upload":
        test_file_upload(args.api_url, args.file_path, args.model)
    else:
        test_path_analysis(args.api_url, args.file_path, args.model)

if __name__ == "__main__":
    main() 