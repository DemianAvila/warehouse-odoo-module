import logging
from io import BytesIO
import xlsxwriter
from barcode import Code128
from barcode.writer import ImageWriter
import json
import cv2
import numpy as np

def larger_pix_amount(first, comp):
    if first>comp:
        return first
    else:
        return comp

def printable_order(data, title):
    larger_img_width = 0
    larger_img_height = 0
    barcode_rows = []
    data = json.loads(data)
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    current_row = 1
    worksheet.write(f"A{current_row}", title)

    current_row += 1
    for delivery in data.keys():
        worksheet.merge_range(
            f"A{current_row}:C{current_row+2}",
            delivery,
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
            })
        current_row += 3
        for order in data[delivery]["order_ids"]:
            worksheet.merge_range(
                f"A{current_row}:C{current_row}",
                f"{order['id']}\t{order['marketplace']}",
                {
                    "bold": 1,
                    "border": 1,
                    "align": "center",
                    "valign": "vcenter",
                }
            )
            current_row += 1
            for product in order["products"]:
                worksheet.merge_range(
                    f"A{current_row}:B{current_row}",
                    product["id"],
                    {
                        "border": 1,
                        "align": "center",
                        "valign": "vcenter",
                    }
                )
                # Write to a file-like object:
                rv = BytesIO()
                Code128(str(product["internal_barcode"]), writer=ImageWriter()).write(rv)
                logging.info("==============================")
                logging.info(rv.read())
                logging.info("==============================")
                h, w, _ = cv2.imdecode(np.frombuffer(rv.read(), np.uint8), 0).shape
                larger_img_height = larger_pix_amount(h, larger_img_height)
                larger_img_width = larger_pix_amount(w, larger_img_width)
                worksheet.insert_image(
                    f"C{current_row}",
                    "a",
                    {
                        "image_data": rv
                    },
                    {
                        "x_scale": 0.25,
                        "y_scale": 0.25,
                        "x_offset": 5,
                        "y_offset": 5,
                        "border": 1
                    }
                )
                barcode_rows.append(current_row)
                current_row += 1

    worksheet.set_column('B:B', larger_img_width+10)
    worksheet.set_row((x for x in barcode_rows), larger_img_height+10)

    workbook.close()

    return output.getvalue()

