import templater

data = {
	'headers': ["Item", "CAS No.", "Weight", "Mass \\%", "Emergency Telephone"],
	'signal_word': "Danger",
	'rows': [
		["Rubber Ducky", "000000-00", "400 kg", "80\\%", "+1(630) 000-0000"],
		["Dino", "000001-00", "100 kg", "20\\%", "+1(630) 000-0000"],
	],
	'pictograms': ["PICT_GHS04_COMPRESSED_GAS", "PICT_GHS07_HARMFUL"]
}

templater = templater.Templater()

output = templater.template_front_page(data)

with open("example-output.tex", "w") as f:
	f.write(output)
