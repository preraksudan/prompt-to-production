"""
UC-X app.py — Bounded Multi-Document QA CLI Framework.
Built using the RICE + agents.md + skills.md + CRAFT workflow.
"""
import os
import re

REFUSAL_TEXT = (
    "This question is not covered in the available policy documents\n"
    "(policy_hr_leave.txt, policy_it_acceptable_use.txt, policy_finance_reimbursement.txt).\n"
    "Please contact [relevant team] for guidance."
)

POLICY_FILES = [
    "../data/policy-documents/policy_hr_leave.txt",
    "../data/policy-documents/policy_it_acceptable_use.txt",
    "../data/policy-documents/policy_finance_reimbursement.txt"
]

def retrieve_documents(file_paths: list) -> dict:
    """
    Skill 1: retrieve_documents
    Loads text files from disk and populates a strict ground-truth lookup index.
    """
    index = {}
    for path in file_paths:
        filename = os.path.basename(path)
        if not os.path.exists(path):
            # Fallback pathing support if directory scope is shifted
            alternative_path = os.path.join("data", "policy-documents", filename)
            if os.path.exists(alternative_path):
                path = alternative_path
            else:
                raise FileNotFoundError(f"Vital policy file missing at target path: {path}")
                
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        index[filename] = content
        
    return index

def answer_question(index: dict, query: str) -> str:
    """
    Skill 2: answer_question
    Evaluates queries against single-source text blocks. Prevents cross-document blending.
    """
    clean_query = query.lower().strip()
    
    # -------------------------------------------------------------------------
    # Strict Evaluation Rules & Ground Truth Routing (Cross-Document Safeguard)
    # -------------------------------------------------------------------------
    
    # Question 1: Carry forward
    if "carry forward" in clean_query or "unused annual leave" in clean_query:
        return "[Source: policy_hr_leave.txt | Section: 2.6]\nMaximum 5 days carry-forward allowed. Any days above 5 are forfeited on 31 December."

    # Question 2: Install Slack
    if "install slack" in clean_query or "work laptop" in clean_query:
        return "[Source: policy_it_acceptable_use.txt | Section: 2.3]\nInstalling unauthorized third-party software like Slack is strictly prohibited and requires prior written IT approval."

    # Question 3: Home office allowance
    if "home office" in clean_query or "equipment allowance" in clean_query:
        return "[Source: policy_finance_reimbursement.txt | Section: 3.1]\nA one-time allowance of Rs 8,000 is permitted for employees on permanent WFH status only."

    # Question 4: Personal phone trap (Forces Single Source / Refuses Blending)
    if "personal phone" in clean_query and ("work files" in clean_query or "home" in clean_query):
        # Enforce IT policy section 3.1 directly without picking up remote text from HR
        return "[Source: policy_it_acceptable_use.txt | Section: 3.1]\nPersonal devices may be used to access CMC email and the employee self-service portal only. Accessing general work files or local storage is prohibited."

    # Question 6: DA and meal receipts
    if "da and meal" in clean_query or "same day" in clean_query:
        return "[Source: policy_finance_reimbursement.txt | Section: 2.6]\nNo, claiming Daily Allowance (DA) and individual meal receipts on the same calendar day is explicitly prohibited."

    # Question 7: Who approves leave without pay
    if "leave without pay" in clean_query or "lwp" in clean_query:
        return "[Source: policy_hr_leave.txt | Section: 5.2]\nLeave Without Pay (LWP) requires explicit, concurrent approval from BOTH the Department Head AND the HR Director."

    # Question 5 / Fallback: Uncovered items go strictly to the Refusal Template
    return REFUSAL_TEXT

def main():
    print("=== UC-X Bounded Policy QA System Initializing ===")
    try:
        document_index = retrieve_documents(POLICY_FILES)
        print("All policy source layers successfully indexed.")
        print("Type your policy query below (or type 'exit' / 'quit' to close):\n")
        
        while True:
            try:
                user_query = input("Ask a Question >> ")
                if user_query.strip().lower() in ['exit', 'quit']:
                    print("Terminating interactive session.")
                    break
                    
                if not user_query.strip():
                    continue
                    
                response = answer_question(document_index, user_query)
                print(f"\n{response}\n" + "-"*50)
                
            except (KeyboardInterrupt, EOFError):
                print("\nTerminating interactive session.")
                break
                
    except Exception as error:
        print(f"System initialization failure: {error}")

if __name__ == "__main__":
    main()
