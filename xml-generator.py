import csv
import sys
import re
import codecs
from xml import dom
from xml.dom.minidom import parse, parseString

dom = parse('../archive-test-files/archive_xml_template.xml')
csvFile = '../archive-test-files/media_objects.csv'

csvData = csv.reader(open(csvFile))

cees = dom.getElementsByTagName('c')
subseries = []
theses = []
rowNum = 0

for c in cees:	
	if c.getAttribute("level") == "subseries": 
		subseries.append(c)

for row in csvData:
    if rowNum == 0:
        tags = row
        # replace spaces w/ underscores in tag names
        for i in range(len(tags)):
            tags[i] = tags[i].replace(' ', '_').decode('utf-8')
    else: 
        # create a new empty dictionary for each thesis/(row) 
        thesis = {}
        # for each column, make the column name the key and the column 
        # content the value of a new thesis dictionary entry 
        for i in range(len(tags)):
            thesis[tags[i]] = row[i].decode('utf-8')

       	theses.append(thesis)

    rowNum +=1 

for thesis in theses:
		#if unititle year equals thesis year:
	for sub in subseries:
		if sub.getElementsByTagName("unittitle")[0].firstChild.nodeValue == thesis["unitdate"]:
			#create c with refid and level <c id="{refid}" level="item">
			c = dom.createElement("c")
			c.attributes["refid"] = thesis["refid"]
			c.attributes["level"] = "item"
			sub.appendChild(c)	
			#create did
			did = dom.createElement("did") 
			c.appendChild(did)
			#create unittitle tag
			unittitle = dom.createElement("unittitle")
			did.appendChild(unittitle)
			unittitle.appendChild(dom.createTextNode(thesis["unittitle"]))
			#create langmaterial tag 	
			langmaterial = dom.createElement("langmaterial")
			did.appendChild(langmaterial)
			language = dom.createElement("language")
			language.attributes["lang"] = "eng"
			langmaterial.appendChild(language)
			#create container tag
			container = dom.createElement("container")
			container.attributes["type"] = thesis["container_type"]
			container.attributes["label"] = thesis["container_label"]
			did.appendChild(container)
			container.appendChild(dom.createTextNode(""))
			#create phydesc tag
			physdesc = dom.createElement("physdesc")
			did.appendChild(physdesc)
			extent = dom.createElement("extent")
			physdesc.appendChild(extent)
			extent.appendChild(dom.createTextNode(thesis["extent"]))
			extent_desct = dom.createElement("extent_desct")
			physdesc.appendChild(extent_desct)
			extent_desct.appendChild(dom.createTextNode(thesis["extent_desc"]))
			#create unitdate tag
			unitdate = dom.createElement("unitdate")
			did.appendChild(unitdate)
			unitdate.appendChild(dom.createTextNode(thesis["unitdate"]))
			#create origination tag
			origination = dom.createElement("origination")
			origination.attributes["label"] = "creator"
			did.appendChild(origination)
			
			#add persnames
			for key, value in thesis.iteritems():				
				m = re.search('persname', key)
				if m != None and len(value) > 0:
					persname = dom.createElement("persname")
					persname.attributes["source"] = "local"
					origination.appendChild(persname)
					persname.appendChild(dom.createTextNode(value))

			# add notes
			if thesis["note_title"] != None and len(thesis["note_title"]) > 0:
				newRef = int(thesis["refid"][3:])
				newRef += 1
				noteRef = "ref" + str(newRef)
				# add note 
				note = dom.createElement("odd")
				note.attributes["id"] = noteRef
				c.appendChild(note)
				#create note title
				head = dom.createElement("head")
				head.appendChild(dom.createTextNode(thesis["note_title"]))
				note.appendChild(head)
				#create note content
				p = dom.createElement("p")
				p.appendChild(dom.createTextNode(thesis["note_text"]))
				note.appendChild(p)

print dom.toxml().encode('utf-8')


# spreadsheet is the cannonical representation of the thesis objects 
# thesis entries will be merged with the spreadsheet on name and date 
# another script will need to be added that iterates through the 
# archive db theses, creates a dict of the archive thesis record, 
# iterate through the subs and inject content into the approproate xml




