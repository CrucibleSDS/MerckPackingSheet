from pathlib import Path
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader(Path(__file__).parent)
env = Environment(loader=file_loader)
template = env.get_template('template.tex')

data = {
	'headers': ["Item", "CAS No.", "Weight", "Mass \\%", "Emergency Telephone"],
	'signal_word': "Danger",
	'rows': [
		["Rubber Ducky", "000000-00", "400 kg", "80\\%", "+1(630) 000-0000"],
		["Dino", "000001-00", "100 kg", "20\\%", "+1(630) 000-0000"],
	],
	'pictograms': ["PICT_GHS04_COMPRESSED_GAS", "PICT_GHS07_HARMFUL"]
}

output = template.render(data=data)

with open("output.tex", "w") as f:
	f.write(output)
