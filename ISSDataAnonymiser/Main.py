from openpyxl import load_workbook

wb = load_workbook("wcd.xlsx")
ws = wb.active

name_map = {}
email_map = {}
counter = 1
ecounter = 1

# Adjust column letters if needed
first_col = "A"
last_col = "B"
email_col = "C"

# ----------- NAME ANONYMIZATION -----------
for row in range(2, ws.max_row + 1):  # skip header row
    first = ws[f"{first_col}{row}"].value
    last = ws[f"{last_col}{row}"].value

    if first and last:
        full_name = f"{first.strip()} {last.strip()}"

        if full_name not in name_map:
            name_map[full_name] = f"Person_{counter:03}"
            counter += 1

        anon_value = name_map[full_name]

        # Replace BOTH columns with same anonymized value
        ws[f"{first_col}{row}"] = anon_value
        ws[f"{last_col}{row}"] = anon_value


# ----------- EMAIL ANONYMIZATION -----------
for row in range(2, ws.max_row + 1):  # start at 2 (same as above)
    email = ws[f"{email_col}{row}"].value

    if email:
        email_clean = email.strip()

        if email_clean not in email_map:
            email_map[email_clean] = f"email_{ecounter:03}"
            ecounter += 1

        eanon_value = email_map[email_clean]

        # Replace email column only
        ws[f"{email_col}{row}"] = eanon_value


wb.save("writing_center_data_anonymized.xlsx")
