from io import BytesIO
import xlsxwriter
from barcode import Code128
from barcode.writer import ImageWriter

def printable_order(data, title):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    current_row = 1
    worksheet.write(f"A{current_row}", title)
    current_row += 1
    for delivery in data.keys():
        worksheet.write(f"A{current_row}", delivery)
        current_row += 1
        for order in data[delivery]["order_ids"]:
            worksheet.write(f"A{current_row}", order["id"])
            worksheet.write(f"B{current_row}", order["marketplace"])
            current_row += 1
            for product in order["products"]:
                worksheet.write(f"A{current_row}", product["id"])
                # Write to a file-like object:
                rv = BytesIO()
                Code128(str(product["internal_barcode"]), writer=ImageWriter()).write(rv)
                worksheet.insert_image(f"A{current_row}", "a", {"image_data": rv})
                current_row += 1

    workbook.close()

    return output.getvalue()

