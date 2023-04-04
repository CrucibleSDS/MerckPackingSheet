import enum
import logging
import os
import subprocess
from enum import Enum
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from jinja2 import Environment, FileSystemLoader
from PyPDF2 import PdfMerger


class Templater:
    def __init__(self):
        self.file_loader = FileSystemLoader(Path(__file__).parent)
        self.env = Environment(loader=self.file_loader)
        self.template = self.env.get_template('template.tex')
        self.logger = logging.getLogger("Templater")

    def generate_pdf(self, data: dict[str, any]) -> BytesIO:
        data['graphicspath'] = f"{(Path(__file__).parent / 'img').absolute()}{os.sep}"
        with TemporaryDirectory() as td:
            with open(Path(td, 'output.tex'), 'w') as f:
                f.write(self.template.render(data=data))
            args = [
                'latexmk',
                '-cd',
                '-jobname=output',
                f'-auxdir={td}',
                f'-outdir={td}',
                '-interaction=batchmode',
                '-halt-on-error',
                '-pdf',
                '-shell-escape',
                'output.tex',
            ]
            subprocess.run(args,
                           cwd=td,
                           timeout=15,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
            with open(Path(td, 'output.log'), 'rb') as f:
                print(f.read().decode('utf-8'))
                # self.logger.debug()
                pass
            with open(Path(td, 'output.pdf'), 'rb') as f:
                pdf = f.read()
        return BytesIO(pdf)


class HazardStatementOverview(Enum):
    ACUTE_TOXICITY = enum.auto()
    ASPIRATIONAL_HAZARD = enum.auto()
    CARCINOGENCITY = enum.auto()
    EMIT_FLAMMABLE_GASES = enum.auto()
    COMBUSTIBLE_DUST = enum.auto()
    CORROSIVE_TO_METALS = enum.auto()
    EXPLOSIVES = enum.auto()
    FLAMMABLE_AEROSOLS = enum.auto()
    FLAMMABLE_LIQUIDS = enum.auto()
    FLAMMABLE_SOLIDS = enum.auto()
    GASES_UNDER_PRESSURE = enum.auto()
    GERM_CELL_MUTAGENCITY = enum.auto()
    HAZARDOUS_TO_AQUATIC_ENVIRONMENT = enum.auto()
    HAZARDOUS_TO_OZONE_LAYER = enum.auto()
    OXIDIZING_GASES = enum.auto()
    OXIDIZING_LIQUIDS = enum.auto()
    OXIDIZING_SOLIDS = enum.auto()
    ORGANIC_PEROXIDES = enum.auto()
    PYROPHORIC_GAS = enum.auto()
    PYROPHORIC_LIQUIDS = enum.auto()
    PYROPHORIC_SOLID = enum.auto()
    REPRODUCTIVE_TOXICITY = enum.auto()
    RESPIRATORY_OR_SKIN_SENSITIZATION = enum.auto()
    SELF_HEATING_CHEMICALS = enum.auto()
    SELF_REACTIVE_CHEMICALS = enum.auto()
    SERIOUS_EYE_DAMAGE_IRRITATION = enum.auto()
    SKIN_CORROSION_IRRITATION = enum.auto()
    SIMPLE_ASPHYXIANT = enum.auto()
    ORGAN_TOXICITY_REPEATED_PROLONGED = enum.auto()
    ORGAN_TOXICITY_SINGLE = enum.auto()
    OTHER = enum.auto()
    NOT_APPLICABLE = enum.auto()


class PaperType(Enum):
    A4_PAPER = 'a4paper'
    A5_PAPER = 'a5paper'
    B5_PAPER = 'b5paper'
    LETTER_PAPER = 'letterpaper'
    LEGAL_PAPER = 'legalpaper'


class SensitivityLabels(Enum):
    PROPRIETARY = 'Proprietary'
    CONFIDENTIAL = 'Confidential'
    SENSITIvE = 'Sensitive'
    PUBLIC = 'Public'


def merge_pdf(pdfs: list[BytesIO]) -> BytesIO:
    bytesio = BytesIO()
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(bytesio)
    merger.close()
    return bytesio


def fix_si(amount):
    prefixes = [
        ('T', 1e12),
        ('G', 1e9),
        ('M', 1e6),
        ('k', 1e3),
        ('', 1),
        ('m', 1e-3),
        ('µ', 1e-6),
        ('n', 1e-9)]
    for prefix, factor in prefixes:
        if amount >= factor:
            return f'{amount / factor:.2f}{prefix}g'
    return f'{amount}g'
