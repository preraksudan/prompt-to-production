"""
UC-0A app.py — Core Implementation Framework.
Built using the RICE + agents.md + skills.md + CRAFT workflow.
"""
import argparse
import os
import csv

ALLOWED_CATEGORIES = [
    "Pothole", "Flooding", "Streetlight", "Waste", "Noise", 
    "Road Damage", "Heritage Damage", "Heat Hazard", "Drain Blockage", "Other"
]

SEVERITY_KEYWORDS = [
    "injury", "child", "school", "hospital", "ambulance", "fire", "hazard", "fell", "collapse"
]

def classify_complaint(description: str) -> dict:
    """
    Skill 1: classify_complaint
    Processes a single string text row under rigid schema constraints.
    """
    desc_lower = description.lower().strip()
    
    # Error Handling & Refusal Condition check
    if not desc_lower:
        return {
            "category": "Other",
            "priority": "Low",
            "reason": "The complaint description is completely blank.",
            "flag": "NEEDS_REVIEW"
        }
        
    # 1. Evaluate Category Strategy
    category = "Other"
    flag = ""
    
    if "pothole" in desc_lower:
        category = "Pothole"
    elif "flood" in desc_lower or "water" in desc_lower:
        category = "Flooding"
    elif "light" in desc_lower or "lamp" in desc_lower:
        category = "Streetlight"
    elif "waste" in desc_lower or "garbage" in desc_lower or "trash" in desc_lower:
        category = "Waste"
    elif "noise" in desc_lower or "loud" in desc_lower:
        category = "Noise"
    elif "road" in desc_lower or "crack" in desc_lower:
        category = "Road Damage"
    elif "heritage" in desc_lower or "monument" in desc_lower:
        category = "Heritage Damage"
    elif "heat" in desc_lower or "hot" in desc_lower:
        category = "Heat Hazard"
    elif "drain" in desc_lower or "sewer" in desc_lower:
        category = "Drain Blockage"
        
    # Check for ambiguity
    matched_indicators = [kw for kw in ["pothole", "flood", "light", "waste", "noise"] if kw in desc_lower]
    if len(matched_indicators) > 1 or category == "Other":
        flag = "NEEDS_REVIEW"

    # 2. Evaluate Priority Strategy
    priority = "Standard"
    triggered_keywords = [kw for kw in SEVERITY_KEYWORDS if kw in desc_lower]
    if triggered_keywords:
        priority = "Urgent"
    elif "low" in desc_lower or "minor" in desc_lower:
        priority = "Low"

    # 3. Create Rationale Reason citing specific words
    if triggered_keywords:
        reason = f"Classified as Urgent due to the presence of the critical phrase '{triggered_keywords[0]}'."
    else:
        # Pull a clean string window out for compliance citing
        words = description.split()
        snippet = " ".join(words[:4]) if len(words) >= 4 else description
        reason = f"Processed based on text containing words like '{snippet}'."

    return {
        "category": category,
        "priority": priority,
        "reason": reason,
        "flag": flag
    }

def batch_classify(input_path: str, output_path: str):
    """
    Skill 2: batch_classify
    Reads source files, transforms columns, and writes clean CSV data bundles.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at: {input_path}")

    results = []
    
    with open(input_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames if reader.fieldnames else []
        
        # Ensure 'description' column presence
        desc_col = 'description' if 'description' in fieldnames else (fieldnames[0] if fieldnames else None)
        
        for row in reader:
            text_to_process = row.get(desc_col, "") if desc_col else ""
            classification = classify_complaint(text_to_process)
            
            # Map elements into target row pipeline structure
            row['category'] = classification['category']
            row['priority_flag'] = classification['priority']  # map priority target
            row['reason'] = classification['reason']
            row['flag'] = classification['flag']
            results.append(row)

    # Determine final structural output columns
    output_fields = list(results[0].keys()) if results else ['description', 'category', 'priority_flag', 'reason', 'flag']
    
    with open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(results)

def main():
    parser = argparse.ArgumentParser(description="UC-0A Citizen Complaint Classifier Processing Tool")
    parser.add_argument('--input', required=True, help="Path to input test CSV file")
    parser.add_argument('--output', required=True, help="Path where output result file should be saved")
    args = parser.parse_args()

    try:
        print(f"Reading configuration from path: {args.input}")
        batch_classify(args.input, args.output)
        print(f"Execution successful! Output committed to: {args.output}")
    except Exception as error:
        print(f"Runtime execution failure encountered: {error}")

if __name__ == "__main__":
    main()
