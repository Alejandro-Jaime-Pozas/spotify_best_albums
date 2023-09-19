import openpyxl

def add_album_data_excel(list_data):

    # Create a new Excel workbook
    workbook = openpyxl.Workbook()

    # Select the default active sheet
    sheet = workbook.active

    # Set column headers
    sheet['A1'] = 'id'
    sheet['B1'] = 'spotify_name'
    sheet['C1'] = 'acclaimed_music_name'
    sheet['D1'] = 'similarity_score'
    sheet['E1'] = 'album_found_on_spotify'
    sheet['F1'] = 'year'

    # Write data to the worksheet
    for row_index, row_data in enumerate(list_data, start=2):
        sheet.cell(row=row_index, column=1, value=row_data['top_album_id'])
        sheet.cell(row=row_index, column=2, value=row_data['top_album_spotify_name'])
        sheet.cell(row=row_index, column=3, value=row_data['acclaimed_music_album_name'])
        sheet.cell(row=row_index, column=4, value=row_data['top_album_score'])
        sheet.cell(row=row_index, column=5, value=row_data['album_found'])
        sheet.cell(row=row_index, column=6, value=row_data['year'])

    # Save the Excel file
    workbook.save('spotify_album_data.xlsx')
    # Close the workbook
    workbook.close()

    print("Excel file 'spotify_album_data' created successfully.")