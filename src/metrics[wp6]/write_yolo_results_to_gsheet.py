import pygsheets


def write_results_to_google_sheet(results, sheet_id, sheet_name, json_keyfile):
    gc = pygsheets.authorize(service_file=json_keyfile)
    try:
        sh = gc.open_by_key(sheet_id)
    except pygsheets.SpreadsheetNotFound:
        print(f"Error: Google Sheet '{sheet_id}' not found.")
        return

    try:
        worksheet = sh.add_worksheet(sheet_name)
    except Exception as e:
        print(f"Error accessing worksheet: {e}")
        return
    worksheet.clear()

    # Write headers
    headers = ["Class", "Precision", "Recall", "F1-score"]
    worksheet.update_value('A1', headers[0])
    worksheet.update_value('B1', headers[1])
    worksheet.update_value('C1', headers[2])
    worksheet.update_value('D1', headers[3])
    class_names = {
        0: "Adh Dense",
        1: "Adh Filmy",
        2: "Sup Black",
        3: "Sup White",
        4: "Sup Red",
        5: "Sup Subtle",
        6: "Ov. Endometrioma",
        7: "Ov. Chocolate Fluid",
        8: "Deep Endometriosis",
        9: 'Background'
    }
    # Write results row by row
    row = 2  # Start from the second row (first row is headers)
    for class_id, metrics in results.items():
        worksheet.update_value(f'A{row}', class_names[class_id])
        worksheet.update_value(f'B{row}', metrics["Precision"])
        worksheet.update_value(f'C{row}', metrics["Recall"])
        worksheet.update_value(f'D{row}', metrics["F1-score"])
        row += 1

    print(f"Results successfully written to Google Sheet '{sheet_name}'.")
