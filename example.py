import os
from pathlib import Path

from templater import Templater, PaperType

t = Templater()

cover = t.generate_pdf({
    'graphicspath': f"{(Path(__file__).parent / 'img').absolute()}{os.sep}",
    'paper': PaperType.A4_PAPER.value,
    'cover_title': "Cover Sheet — U.S. Origin Shipments",
    'sensitivity': "Proprietary",
    'product_name': "Test Product",
    'destination_country': "United States",
    'columns': 'L|l|l|l|l|l',
    'headers': [
        "Product Name",
        "CAS No.",
        "Product Brand",
        "Product Number",
        f"{'Mass'} \\%"
    ],
    'signal_word': None,
    'rows': [
        ["Rubber Ducky", "000000-00", "400 kg", "80\\%", "+1(630) 000-0000"],
        ["Dino", "000001-00", "100 kg", "20\\%", "+1(630) 000-0000"],
    ],
    'pictograms': ["PICT_GHS04_COMPRESSED_GAS", "PICT_GHS07_HARMFUL"],
    'hazard_statement_overview': ["EMIT_FLAMMABLE_GASES", "HAZARDOUS_TO_AQUATIC_ENVIRONMENT"],
    'signature_Date': "September 38, 2023",
})

with open("example-output.pdf", "wb") as f:
    f.write(cover.getbuffer())
