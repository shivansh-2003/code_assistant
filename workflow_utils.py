# workflow_utils.py
"""
Utility functions for the GitHub Actions workflow.
This includes handling of OpenAI API keys and other configuration.
"""

import os
import json
import subprocess
import argparse
from typing import Dict, Any, List, Optional

def setup_openai_credentials(api_key: Optional[str] = None) -> None:
    """
    Set up OpenAI API credentials for GitHub Actions workflow.
    
    This function handles setting up the OpenAI API key from either:
    - A provided API key parameter
    - The OPENAI_API_KEY environment variable
    - A .env file in the repository
    
    Args:
        api_key (str, optional): OpenAI API key to use. Defaults to None.
    
    Raises:
        ValueError: If no API key could be found through any method
    """
    # First try the provided API key
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        return
    
    # Then check for an environment variable (GitHub secret)
    if "OPENAI_API_KEY" in os.environ and os.environ["OPENAI_API_KEY"]:
        return
    
    # Finally, check for a .env file
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("OPENAI_API_KEY="):
                    key = line.strip().split("=", 1)[1]
                    # Remove quotes if present
                    key = key.strip("'\"")
                    if key:
                        os.environ["OPENAI_API_KEY"] = key
                        return
    
    # If we get here, no API key was found
    raise ValueError(
        "No OpenAI API key found. Please set the OPENAI_API_KEY environment variable, "
        "provide it as a parameter, or include it in a .env file."
    )

def format_analysis_comment(results_file: str) -> str:
    """
    Format code analysis results into a GitHub comment.
    
    Args:
        results_file (str): Path to the JSON results file
    
    Returns:
        str: Formatted comment text in Markdown
    """
    try:
        with open(results_file, "r") as f:
            results = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        return f"Error reading analysis results: {str(e)}"
    
    # Extract file name
    file_name = os.path.basename(results_file).replace("_analysis.json", "")
    
    # Build the comment
    comment = f"## Code Quality Analysis: {file_name}\n\n"
    comment += f"**Overall Score**: {results.get('overall_score', 'N/A')}/100\n\n"
    
    # Add breakdown section
    breakdown = results.get("breakdown", {})
    if breakdown:
        comment += "### Score Breakdown\n\n"
        for category, score in breakdown.items():
            max_score = {"naming": 10, "modularity": 20, "comments": 20, 
                          "formatting": 15, "reusability": 15, "best_practices": 20}.get(category, "?")
            comment += f"- **{category.capitalize()}**: {score}/{max_score}\n"
        comment += "\n"
    
    # Add recommendations
    recommendations = results.get("recommendations", [])
    if recommendations:
        comment += "### Recommendations\n\n"
        for i, rec in enumerate(recommendations, 1):
            comment += f"{i}. {rec}\n"
    
    return comment

def analyze_changed_files(files: List[str], model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
    """
    Analyze a list of changed files and generate a summary.
    
    Args:
        files (List[str]): List of file paths to analyze
        model (str, optional): OpenAI model to use. Defaults to "gpt-3.5-turbo".
    
    Returns:
        Dict[str, Any]: Summary of analysis results
    """
    summary = {
        "files_analyzed": 0,
        "average_score": 0,
        "results": {},
        "comment_text": "# Code Quality Analysis Results 🔍\n\n"
    }
    
    total_score = 0
    
    for file_path in files:
        if not os.path.exists(file_path):
            continue
            
        # Run the analyzer
        output_file = f"{os.path.basename(file_path)}_{model}_analysis.json"
        try:
            subprocess.run(
                ["python", "code-analyzer.py", file_path, "--model", model, "--save"],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Find the generated output file
            import glob
            result_files = glob.glob(f"{os.path.basename(file_path)}_*_analysis.json")
            if not result_files:
                continue
                
            # Use the most recently created file
            result_file = max(result_files, key=os.path.getctime)
            
            # Read the results
            with open(result_file, "r") as f:
                results = json.load(f)
                
            # Add to summary
            summary["files_analyzed"] += 1
            score = results.get("overall_score", 0)
            total_score += score
            summary["results"][file_path] = results
            
            # Format for comment
            file_comment = format_analysis_comment(result_file)
            summary["comment_text"] += f"{file_comment}\n\n---\n\n"
            
        except Exception as e:
            summary["comment_text"] += f"Error analyzing {file_path}: {str(e)}\n\n"
    
    # Calculate average score
    if summary["files_analyzed"] > 0:
        summary["average_score"] = total_score / summary["files_analyzed"]
        
    # Add summary footer
    summary["comment_text"] += f"\n\n_Analysis performed on {summary['files_analyzed']} files with an average score of {summary['average_score']:.1f}/100._\n"
    summary["comment_text"] += "\n_Generated by Carbon Crunch Code Analyzer_"
    
    return summary

def main():
    """Main function for command line usage."""
    parser = argparse.ArgumentParser(description="Analyze changed files in GitHub Actions")
    parser.add_argument("--files", nargs="+", help="List of files to analyze")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="OpenAI model to use")
    parser.add_argument("--output", default="analysis_summary.json", help="Output file for summary")
    
    args = parser.parse_args()
    
    # Setup OpenAI credentials
    setup_openai_credentials()
    
    # Analyze files
    summary = analyze_changed_files(args.files, args.model)
    
    # Save summary
    with open(args.output, "w") as f:
        json.dump(summary, f, indent=2)
    
    # Also create a Markdown summary
    with open(args.output.replace(".json", ".md"), "w") as f:
        f.write(summary["comment_text"])
    
    # Print summary for GitHub Actions
    print(f"::set-output name=files_analyzed::{summary['files_analyzed']}")
    print(f"::set-output name=average_score::{summary['average_score']:.1f}")
    
    # GitHub Actions can't handle multiline outputs well, so we'll save the comment to a file
    # and read it in the workflow

if __name__ == "__main__":
    main()
