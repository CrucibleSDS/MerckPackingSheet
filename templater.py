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
                self.logger.debug(f.read().decode('utf-8'))
                pass
            with open(Path(td, 'output.pdf'), 'rb') as f:
                pdf = f.read()
        return BytesIO(pdf)


class HazardStatementOverview(Enum):
    ACUTE_TOXICITY = enum.auto()
    ASPIRATION_HAZARD = enum.auto()
    CARCINOGENICITY = enum.auto()
    EMIT_FLAMMABLE_GASES = enum.auto()
    COMBUSTIBLE_DUST = enum.auto()
    CORROSIVE_TO_METALS = enum.auto()
    EXPLOSIVES = enum.auto()
    FLAMMABLE_AEROSOLS = enum.auto()
    FLAMMABLE_LIQUIDS = enum.auto()
    FLAMMABLE_SOLIDS = enum.auto()
    GASES_UNDER_PRESSURE = enum.auto()
    GERM_CELL_MUTAGENICITY = enum.auto()
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

    @classmethod
    def get_statement(cls, hcode):
        hcode_map: dict[str, cls] = {
            # ACUTE_TOXICITY
            "H300": [cls.ACUTE_TOXICITY],
            "H301": [cls.ACUTE_TOXICITY],
            "H302": [cls.ACUTE_TOXICITY],
            "H303": [cls.ACUTE_TOXICITY],
            "H310": [cls.ACUTE_TOXICITY],
            "H311": [cls.ACUTE_TOXICITY],
            "H312": [cls.ACUTE_TOXICITY],
            "H313": [cls.ACUTE_TOXICITY],
            "H330": [cls.ACUTE_TOXICITY],
            "H331": [cls.ACUTE_TOXICITY],
            "H332": [cls.ACUTE_TOXICITY],
            "H333": [cls.ACUTE_TOXICITY],
            # ASPIRATION_HAZARD
            "H304": [cls.ASPIRATION_HAZARD],
            "H305": [cls.ASPIRATION_HAZARD],
            # CARCINOGENICITY
            "H350": [cls.CARCINOGENICITY],
            "H351": [cls.CARCINOGENICITY],
            # EMIT_FLAMMABLE_GASES
            "H260": [cls.EMIT_FLAMMABLE_GASES],
            "H261": [cls.EMIT_FLAMMABLE_GASES],
            # COMBUSTIBLE_DUST TODO CANNOT FIND
            # CORROSIVE_TO_METALS
            "H290": [cls.CORROSIVE_TO_METALS],
            # EXPLOSIVES
            "H200": [cls.EXPLOSIVES],
            "H201": [cls.EXPLOSIVES],
            "H202": [cls.EXPLOSIVES],
            "H203": [cls.EXPLOSIVES],
            "H204": [cls.EXPLOSIVES],
            "H205": [cls.EXPLOSIVES],
            "H206": [cls.EXPLOSIVES],
            "H207": [cls.EXPLOSIVES],
            "H208": [cls.EXPLOSIVES],
            "H209": [cls.EXPLOSIVES],
            "H210": [cls.EXPLOSIVES],
            "H211": [cls.EXPLOSIVES],
            # FLAMMABLE_AEROSOLS
            "H222": [cls.FLAMMABLE_AEROSOLS],
            "H223": [cls.FLAMMABLE_AEROSOLS],
            "H229": [cls.FLAMMABLE_AEROSOLS], # TODO CHECK IF "AEROSOLS" FIT HERE
            # FLAMMABLE_LIQUIDS
            "H224": [cls.FLAMMABLE_LIQUIDS],
            "H225": [cls.FLAMMABLE_LIQUIDS],
            "H226": [cls.FLAMMABLE_LIQUIDS],
            "H227": [cls.FLAMMABLE_LIQUIDS],
            # FLAMMABLE_SOLIDS
            "H228": [cls.FLAMMABLE_SOLIDS],
            # GASES_UNDER_PRESSURE
            "H280": [cls.GASES_UNDER_PRESSURE],
            "H281": [cls.GASES_UNDER_PRESSURE],
            "H282": [cls.GASES_UNDER_PRESSURE],
            "H283": [cls.GASES_UNDER_PRESSURE],
            "H284": [cls.GASES_UNDER_PRESSURE],
            # GERM_CELL_MUTAGENICITY
            "H340": [cls.GERM_CELL_MUTAGENICITY],
            "H341": [cls.GERM_CELL_MUTAGENICITY],
            # HAZARDOUS_TO_AQUATIC_ENVIRONMENT
            "H400": [cls.HAZARDOUS_TO_AQUATIC_ENVIRONMENT],
            "H401": [cls.HAZARDOUS_TO_AQUATIC_ENVIRONMENT],
            "H402": [cls.HAZARDOUS_TO_AQUATIC_ENVIRONMENT],
            "H410": [cls.HAZARDOUS_TO_AQUATIC_ENVIRONMENT],
            "H411": [cls.HAZARDOUS_TO_AQUATIC_ENVIRONMENT],
            "H412": [cls.HAZARDOUS_TO_AQUATIC_ENVIRONMENT],
            "H413": [cls.HAZARDOUS_TO_AQUATIC_ENVIRONMENT],
            # HAZARDOUS_TO_OZONE_LAYER
            "H420": [cls.HAZARDOUS_TO_OZONE_LAYER],
            # OXIDIZING_GASES
            "H270": [cls.OXIDIZING_GASES],
            # OXIDIZING_LIQUIDS, OXIDIZING_SOLIDS
            "H271": [cls.OXIDIZING_LIQUIDS, cls.OXIDIZING_SOLIDS],
            "H272": [cls.OXIDIZING_LIQUIDS, cls.OXIDIZING_SOLIDS],
            # ORGANIC_PEROXIDES, SELF_REACTIVE_CHEMICALS
            "H240": [cls.ORGANIC_PEROXIDES, cls.SELF_REACTIVE_CHEMICALS],
            "H241": [cls.ORGANIC_PEROXIDES, cls.SELF_REACTIVE_CHEMICALS],
            "H242": [cls.ORGANIC_PEROXIDES, cls.SELF_REACTIVE_CHEMICALS],
            # PYROPHORIC_GAS
            "H220": [cls.PYROPHORIC_GAS],
            # PYROPHORIC_LIQUIDS, PYROPHORIC_SOLID
            "H250": [cls.PYROPHORIC_LIQUIDS, cls.PYROPHORIC_SOLID],
            # REPRODUCTIVE_TOXICITY
            "H360": [cls.REPRODUCTIVE_TOXICITY],
            "H361": [cls.REPRODUCTIVE_TOXICITY],
            "H362": [cls.REPRODUCTIVE_TOXICITY],
            # RESPIRATORY_OR_SKIN_SENSITIZATION
            "H317": [cls.RESPIRATORY_OR_SKIN_SENSITIZATION],
            # SELF_HEATING_CHEMICALS
            "H251": [cls.SELF_HEATING_CHEMICALS],
            "H252": [cls.SELF_HEATING_CHEMICALS],
            # SERIOUS_EYE_DAMAGE_IRRITATION
            "H314": [cls.SERIOUS_EYE_DAMAGE_IRRITATION, cls.SKIN_CORROSION_IRRITATION],
            "H318": [cls.SERIOUS_EYE_DAMAGE_IRRITATION],
            "H319": [cls.SERIOUS_EYE_DAMAGE_IRRITATION],
            "H320": [cls.SERIOUS_EYE_DAMAGE_IRRITATION],
            # SKIN_CORROSION_IRRITATION
            "H315": [cls.SKIN_CORROSION_IRRITATION],
            "H316": [cls.SKIN_CORROSION_IRRITATION],
            # SIMPLE_ASPHYXIANT TODO CANNOT FIND
            # ORGAN_TOXICITY_REPEATED_PROLONGED
            "H372": [cls.ORGAN_TOXICITY_REPEATED_PROLONGED],
            "H373": [cls.ORGAN_TOXICITY_REPEATED_PROLONGED],
            # ORGAN_TOXICITY_SINGLE
            "H335": [cls.ORGAN_TOXICITY_SINGLE],
            "H336": [cls.ORGAN_TOXICITY_SINGLE],
            "H370": [cls.ORGAN_TOXICITY_SINGLE],
            "H371": [cls.ORGAN_TOXICITY_SINGLE],
        }
        try:
            result = hcode_map[hcode]
        except KeyError:
            result = []
        return result

    @classmethod
    def get_statements(cls, hcodes):
        statements: list[cls] = []
        for hcode in hcodes:
            statements.extend(cls.get_statement(hcode))
        return statements

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
