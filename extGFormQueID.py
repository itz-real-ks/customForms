import json
import re
import requests

# Map Google Form internal type codes to human-readable names
QUESTION_TYPES = {
    0: "Short Answer",
    1: "Paragraph",
    2: "Multiple Choice",
    3: "Dropdown",
    4: "Checkboxes",
    5: "Linear Scale",
    7: "Grid / Matrix",
    9: "Date",
    10: "Time",
    11: "File Upload",
    99: "Section Header / Page Break",
}


# Main func => entry_id
def extract_form_details(url: str):
    # Add a User-Agent header to avoid being blocked by Google
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[-] Error fetching the URL: {e}")
        return

    # Extract the hidden JSON structure using Regex
    match = re.search(r"FB_PUBLIC_LOAD_DATA_ = (.*?);", response.text)
    if not match:
        print(
            "[-] Could not find form data. Make sure the URL is a public 'viewform' link."
        )
        return

    try:
        data_str = match.group(1)
        data = json.loads(data_str)
        form_fields = data[1][1]
    except (json.JSONDecodeError, IndexError, TypeError) as e:
        print(f"[-] Error parsing form payload: {e}")
        return

    # Parse fields and collect rows for the table
    table_rows = []
    for field in form_fields:
        try:
            # Field label/question title
            label = field[1] if field[1] else "Untitled Section / Description"

            # Field type code
            type_code = field[3] if len(field) > 3 else None
            field_type = QUESTION_TYPES.get(type_code, f"Other / Unknown ({type_code})")

            # Entry ID is usually nested in field[4][0][0]
            entry_id = "N/A"
            if len(field) > 4 and field[4] and field[4][0] and field[4][0][0]:
                entry_id = f"entry.{field[4][0][0]}"

            # Skip items that don't take user inputs (like section headers) if entry_id is N/A
            if entry_id != "N/A" or type_code == 99:
                table_rows.append(
                    {"label": label, "entry_id": entry_id, "type": field_type}
                )
        except (IndexError, TypeError):
            continue

    # Print Clean Tabular Format
    print("\n" + "=" * 90)
    print(
        f"{'Question / Field Label':<45} | {'Entry ID':<18} | {'Expected Input Type':<20}"
    )
    print("=" * 90)

    for row in table_rows:
        # Truncate long labels for clean alignment
        display_label = (
            (row["label"][:42] + "...") if len(row["label"]) > 45 else row["label"]
        )
        print(f"{display_label:<45} | {row['entry_id']:<18} | {row['type']:<20}")

    print("=" * 90 + "\n")


if __name__ == "__main__":
    # Replace with your public Google Form viewform URL
    # form_url : str = "https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform"
    form_url: str = input("Enter your full google forms link: ")
    extract_form_details(form_url)
