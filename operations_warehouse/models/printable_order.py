from io import BytesIO
import xlsxwriter
from barcode import Code128
from barcode.writer import ImageWriter
import json
import logging
def printable_order(data, title):
    logging.info("=====================")
    logging.info("1")
    logging.info(data)
    logging.info("=====================")
    data = json.load(data)
    logging.info("=====================")
    logging.info("2")
    logging.info("=====================")
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

