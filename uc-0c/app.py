"""
UC-0C app.py — Granular Budget Pipeline Framework.
Built using the RICE + agents.md + skills.md + CRAFT workflow.
"""
import argparse
import os
import csv
import sys

def load_dataset(input_path: str) -> list:
    """
    Skill 1: load_dataset
    Reads CSV records, tracks explicit null count indicators, and registers notes.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at: {input_path}")
        
    rows = []
    null_count = 0
    
    with open(input_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Guard column architecture consistency
        required_cols = ['period', 'ward', 'category', 'budgeted_amount', 'actual_spend', 'notes']
        for col in required_cols:
            if col not in reader.fieldnames:
                raise ValueError(f"Missing essential dataset column: {col}")
                
        for idx, row in enumerate(reader, start=1):
            actual_val = row.get('actual_spend', '').strip()
            if not actual_val:
                null_count += 1
                print(f"[DATA LOG] Row {idx}: Found NULL value in ward '{row['ward']}' | Reason: {row['notes']}")
            rows.append(row)
            
    print(f"[DATA LOG] Dataset loaded. Total rows: {len(rows)}, Deliberate Nulls: {null_count}")
    return rows

def compute_growth(data: list, ward: str, category: str, growth_type: str) -> list:
    """
    Skill 2: compute_growth
    Calculates sequential granular metrics showing math equations without scope bleeding.
    """
    # Filter dataset strictly for the designated coordinates
    filtered_rows = [r for r in data if r['ward'] == ward and r['category'] == category]
    
    # Sort chronologically by the period sequence (YYYY-MM)
    filtered_rows.sort(key=lambda x: x['period'])
    
    output_records = []
    
    for idx, current_row in enumerate(filtered_rows):
        period = current_row['period']
        actual_str = current_row['actual_spend'].strip()
        notes = current_row['notes']
        
        out_row = {
            "period": period,
            "ward": ward,
            "category": category,
            "actual_spend": "NULL" if not actual_str else actual_str,
            "growth": "NOT_COMPUTED",
            "formula": "n/a"
        }
        
        # Enforcement 2: Flag null rows and block evaluation
        if not actual_str:
            out_row["growth"] = f"NULL - {notes}"
            out_row["formula"] = "Blocked due to missing metric input"
            output_records.append(out_row)
            continue
            
        current_val = float(actual_str)
        
        if idx == 0:
            out_row["growth"] = "First Period Baseline"
            out_row["formula"] = "None (No preceding index)"
        else:
            prev_row = filtered_rows[idx - 1]
            prev_str = prev_row['actual_spend'].strip()
            
            if not prev_str:
                out_row["growth"] = "NOT_COMPUTED"
                out_row["formula"] = f"Blocked: Previous period ({prev_row['period']}) value is NULL"
            else:
                prev_val = float(prev_str)
                if prev_val == 0:
                    out_row["growth"] = "Undefined"
                    out_row["formula"] = f"(Current [{current_val}] - Previous) / Previous"
                else:
                    change = current_val - prev_val
                    growth_rate = (change / prev_val) * 100
                    sign = "+" if growth_rate >= 0 else ""
                    out_row["growth"] = f"{sign}{growth_rate:.1f}%"
                    out_row["formula"] = f"(Current [{current_val}] - Previous [{prev_val}]) / Previous [{prev_val}] * 100"
                    
        output_records.append(out_row)
        
    return output_records

def main():
    parser = argparse.ArgumentParser(description="UC-0C Localized Financial Growth Pipeline")
    parser.add_argument('--input', required=True, help="Path to input budget spreadsheet")
    parser.add_argument('--ward', required=False, help="Isolated target ward name filter")
    parser.add_argument('--category', required=False, help="Isolated target category name filter")
    parser.add_argument('--growth-type', required=False, help="MoM or YoY target selection")
    parser.add_argument('--output', required=True, help="Output tracking path destination")
    args = parser.parse_args()

    # Enforcement 1 & Refusal: Guard macro aggregation requests
    if not args.ward or not args.category:
        print("CRITICAL REFUSAL: System will not compute all-ward or cross-category macro aggregations.")
        sys.exit(1)

    # Enforcement 4: Growth type checking constraints
    if not args.growth_type:
        print("CRITICAL REFUSAL: Growth calculation layout parameters not defined. Please explicitly provide --growth-type.")
        sys.exit(1)
        
    if args.growth_type != "MoM":
        print(f"CRITICAL REFUSAL: Unsupported calculation layout method: {args.growth_type}. Only MoM is supported.")
        sys.exit(1)

    try:
        dataset = load_dataset(args.input)
        processed_table = compute_growth(dataset, args.ward, args.category, args.growth_type)
        
        # Commit results to structural output CSV layout
        with open(args.output, mode='w', encoding='utf-8', newline='') as outfile:
            fieldnames = ["period", "ward", "category", "actual_spend", "growth", "formula"]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_table)
            
        print(f"Execution successful! Granular results written directly to: {args.output}")
        
    except Exception as error:
        print(f"Runtime execution failure encountered: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
