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
    larger_text = 0
    barcode_rows = []
    data = json.loads(data)
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    current_row = 1
    title_format = workbook.add_format(
        {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
        }
    )

    order_format = workbook.add_format(
        {
            "border": 1,
            "align": "center",
            "valign": "vcenter",
        }
    )

    worksheet.merge_range(
        f"A{current_row}:C{current_row + 2}",
        title,
        title_format
    )

    current_row += 3
    for delivery in data.keys():
        worksheet.merge_range(
            f"A{current_row}:C{current_row}",
            delivery,
            title_format
        )
        current_row += 1
        for order in data[delivery]["order_ids"]:
            worksheet.merge_range(
                f"A{current_row}:C{current_row}",
                f"{order['id']}\t{order['marketplace']}",
                order_format
            )
            current_row += 1
            for product in order["products"]:
                larger_text = larger_pix_amount(larger_text, len(product["id"]))
                worksheet.merge_range(
                    f"A{current_row}:B{current_row}",
                    product["id"],
                    order_format
                )
                # Write to a file-like object:
                rv = BytesIO()
                Code128(str(product["internal_barcode"]), writer=ImageWriter()).write(rv)
                rv.seek(0)
                buffer_array = np.frombuffer(rv.read(), np.uint8)
                h, w = cv2.imdecode(buffer_array, 0).shape
                larger_img_height = larger_pix_amount(h, larger_img_height)
                larger_img_width = larger_pix_amount(w, larger_img_width)
                worksheet.insert_image(
                    col = 2,
                    row= current_row,
                    filename = "a",
                    options = {
                        "image_data": rv,
                        "x_scale": 0.4,
                        "y_scale": 0.4,
                    }
                )
                barcode_rows.append(current_row)
                current_row += 1


    worksheet.set_column(
        first_col = 2,
        last_col = 2,
        width = ((larger_img_width/4)+10)
    )
    worksheet.set_column(
        first_col=1,
        last_col=1,
        width=larger_text
    )

    for x in barcode_rows:
        worksheet.set_row(
            row = x-1,
            height = ((larger_img_height/4)+10)
        )

    workbook.close()

    return output.getvalue()

