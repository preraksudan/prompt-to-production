# skills.md
# INSTRUCTIONS: Generate a draft by prompting AI, then manually refine this file.
# Delete these comments before committing.

- name: "classify_complaint"
  description: "Processes a single raw text complaint row to extract and assign the correct category, priority, quotation reason, and evaluation review flag based on strict operational schemas."
  input:
    type: "string"
    format: "Plain text raw complaint description row from CSV item entry."
  output:
    type: "dictionary"
    format: "{'category': string, 'priority': string, 'reason': string, 'flag': string}"
  error_handling: "If the input text is completely missing or blank, defaults to Other category, Low priority, explicitly populates reason stating missing text description string, and marks flag as NEEDS_REVIEW."

- name: "batch_classify"
  description: "Reads the complete source city test CSV data bundle, loops row by row invoking the individual row evaluation capability, and commits results to a target output file framework."
  input:
    type: "string"
    format: "Local filesystem path string directing to the raw source test CSV file."
  output:
    type: "string"
    format: "Local filesystem path string confirming successful execution and validation layout writing."
  error_handling: "If the targeted source input file does not exist on the filesystem path or structural columns are missing, raises a clear FileNotFoundError or ValueError explicitly halt execution."
