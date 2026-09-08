# skills.md
# INSTRUCTIONS: Generate a draft by prompting AI, then manually refine this file.
# Delete these comments before committing.

skills:
- name: "retrieve_policy"
  description: "Loads the target plain text policy file from the local file path and parses the content into structured, indexable numbered sections."
  input:
    type: "string"
    format: "Path directing to the raw policy text document file."
  output:
    type: "dictionary"
    format: "A keyed structure mapping section identifiers to raw text strings."
  error_handling: "If the requested policy file does not exist at the target path location, it throws a strict FileNotFoundError to immediately alert the processing framework."

- name: "summarize_policy"
  description: "Evaluates the parsed sections structure to generate a dense summary that enforces cross-referencing and absolute operational fidelity."
  input:
    type: "dictionary"
    format: "A keyed dictionary layout representing individual policy clauses and content blocks."
  output:
    type: "string"
    format: "A strict plain text summary containing exact clause definitions and compliance verifications."
  error_handling: "If vital inventory clauses are omitted or missing completely from the dictionary input, it defaults to quoting the target text verbatim and flagging a failure mode alert."

