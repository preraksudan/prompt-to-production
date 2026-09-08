# skills.md
# INSTRUCTIONS: Generate a draft by prompting AI, then manually refine this file.
# Delete these comments before committing.

skills:
  - name: "load_dataset"
  description: "Reads the target CSV spreadsheet data, validates all column definitions, and logs complete null counts alongside their text notes before return steps."
  input:
    type: "string"
    format: "Local file path target directory directing to the source ward budget CSV table layout."
  output:
    type: "list"
    format: "A structural list of rows mapped out as item dictionaries."
  error_handling: "If the input file path layout is invalid or vital column labels like actual_spend are completely missing, throws an explicit ValueError."

- name: "compute_growth"
  description: "Filters records by the target ward and category parameters to run sequential period calculations displaying exact math formulas."
  input:
    type: "dictionary"
    format: "{'data': list, 'ward': string, 'category': string, 'growth_type': string}"
  output:
    type: "list"
    format: "A compiled sequence of per-period entries showing values, null alerts, and specific formulas."
  error_handling: "If growth_type is omitted or matches values other than MoM, aborts the application immediately."
