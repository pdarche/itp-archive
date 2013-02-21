import csv

import sqlite3
conn = sqlite3.connect('../ItpArchive/db-test/itparchive.db')

c = conn.cursor()

csvwriter = csv.writer(open('thesis_from_db.csv', "w"))

csvwriter.writerow(["refid", "unittitle", "unitdate", "container_type", "container_label", "extent", "extent_desc", "note_title", "note_text", "persname_1", "persname_2", "persname_3", "persname_4"])

theses = c.execute('SELECT * FROM theses, people, documentations  WHERE theses.id = people.thesis_id AND theses.id = documentations.thesis_id')

for thesis in theses:
	thesis_id = "ref" + str((int(thesis[0]) * 2) + 1008)
	unittitle = thesis[1]
	unitdate = thesis[2]
	container_type = "Box"
	container_label = "ITP Archive Thesis Database" #(Year-refId) needs to be standardized
	extent = "1.0 object" 
	extent_desc = "One thesis pdf"
	note_title = "Document Link"
	note_text = "http://s3.amazonaws.com/itp_archive/documentation/%s/%s" % (thesis[0], thesis[20])
	persname_1 = "%s %s" % (thesis[7], thesis[8])
	persname_2 = ""
	persname_3 = ""
	persname_4 = ""
	newrow = [ thesis_id, unittitle, unitdate, container_type, container_label, extent, extent_desc, note_title, note_text, persname_1, persname_2, persname_3, persname_4 ]
	csvwriter.writerow(newrow)
	


	













