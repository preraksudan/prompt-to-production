# skills.md
# INSTRUCTIONS: Generate a draft by prompting AI, then manually refine this file.
# Delete these comments before committing.

- name: "retrieve_documents"
  description: "Loads the three core corporate policy files from the local filesystem and indexes their raw contents by document filename and section numbers."
  input:
    type: "list"
    format: "A list containing local file path target directory strings."
  output:
    type: "dictionary"
    format: "An indexed lookup structure keyed by document name and individual section identifiers."
  error_handling: "If any of the target policy manuals do not exist at the designated path locations, raises a clear FileNotFoundError to halt indexing operations."

- name: "answer_question"
  description: "Searches the structured policy index to resolve targeted query strings using single-source extraction or a strict refusal template."
  input:
    type: "dictionary"
    format: "{'index': dictionary, 'query': string}"
  output:
    type: "string"
    format: "A single-source response complete with document name and section citations, or a rigid literal refusal text block."
  error_handling: "If the question cannot be safely answered from a single isolated reference segment, defaults directly to emitting the exact required system refusal structure."
