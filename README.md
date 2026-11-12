# customForms



### Google Form Details Extractor

A lightweight Python script that extracts internal field labels, types, and entry IDs from any public Google Form (`viewform` URL) and displays them in a clean, structured command-line table.

---

#### Features
* **Automatic Field Mapping**: Translates Google Form internal type codes (e.g., Short Answer, Paragraph, Multiple Choice, Checkboxes) into human-readable names.
* **Entry ID Discovery**: Grabs the specific `entry.XXXXXXXXX` IDs required for programmatic form submission.
* **Robust Request Handling**: Includes standard headers (`User-Agent`) to prevent blocking by Google.
* **Formatted Output**: Prints a neat tabular summary of all questions and section headers.

---

## Prerequisites

Make sure you have Python installed along with the `requests` library:

```bash
pip install requests
```
```
