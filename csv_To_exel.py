import csv, os
import xlsxwriter
csvs = '/Users/MWK/Desktop/bios/multi_bios.csv'
xlsx = '/Users/MWK/Desktop/bios/new_multi_bios.xlsx'
workbook = xlsxwriter.Workbook(xlsx)
worksheet = workbook.add_worksheet()

with open(csvs, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            worksheet.write(line_count, 0, "Titel")
            worksheet.write(line_count, 1, "Start tijd")
            worksheet.write(line_count, 2, "Leeftijd")
            worksheet.write(line_count, 3, "Afbeelding")
            line_count += 1
        print(f'\tDe film {row["Titel"]} begint om {row["Start tijd"]} en heeft als url{row["Afbeelding"]}')
        if "(OV)" in str(row["Titel"]):
            worksheet.write(line_count, 4, "True") 
        else:
            worksheet.write(line_count, 4, "False")

        worksheet.write(line_count, 0, str(row["Titel"]))
        worksheet.write(line_count, 1, str(row["Start tijd"]))
        try:
            worksheet.write(line_count, 2, int(row["Leeftijd"]))
        except ValueError as e:
            worksheet.write(line_count, 2, str(row["Leeftijd"]))

        worksheet.write(line_count, 3, str(row["Afbeelding"]))
        line_count += 1

    print(f'Processed {line_count} lines.')


workbook.close()
