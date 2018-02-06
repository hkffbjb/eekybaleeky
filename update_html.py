"""
~~~~~~~~~~~~~~ Update to make newer versions go on top & say (New) ~~~~~~~~~~~~~~
~~~~~~~~~~~~~~ Could also push things to php and use that to make  ~~~~~~~~~~~~~~
~~~~~~~~~~~~~~ pages up. This could work well with search.         ~~~~~~~~~~~~~~
"""

def update_html(monster,url,star,filename):
	new_html = "                            <li>\n                                <a href=\"" + url + "\">" + monster + "</a>\n                            </li>"
	found_abc = False
	found_star = False
	abc_cont_found = False
	extra = 0
	new_code = ""
	new_section = "                    <li>\n                        <h2 id=\"" + monster[0] + "\">\n                            " + monster[0] + "\n                        </h2>\n"
	new_section += "                        <ul>\n" + new_html + "\n                            <li class=\"hline\"></li>\n                        </ul>"
	f = open(filename,"r")
	contents = f.read()
	lines = contents.split("\n")
	new_lines = lines
	for i,line in enumerate(lines):
		if "<h2 " in line:
			data = line.split('"')
			if data[1] == monster[0]:
				found_abc = True
				contents = []
				contents_found = False
				k = i
				while not contents_found:
					if "</ul>" in lines[k]:
						contents_found = True
					else:
						contents.append(lines[k])
						k += 1
				contents = contents[3:]
				if len(contents) > 1:
					passed = False
					l = 0
					while not passed:
						line_no = i+l+4
						if "</a>" in contents[l]:
							in_this_line = contents[l].split(">")
							monster_here = in_this_line[1][:-3]
							sorting_list = [monster, monster_here]
							sorting_list.sort()
							if sorting_list[0] == sorting_list[1]:
								passed = True
							elif monster == sorting_list[0]:
								passed = True
								new_lines.insert(line_no-2,new_html)
								extra += 1
						elif '<li class="hline"></li>' in contents[l]:
							passed = True
							new_lines.insert(line_no-1,new_html)
							extra += 1
						l += 1
				else:
					new_lines.insert(k-1+extra,new_html)
					extra += 1
			if data[1] == star:
				found_star = True
				contents = []
				contents_found = False
				k = i
				while not contents_found:
					if "</ul>" in lines[k]:
						contents_found = True
					else:
						contents.append(lines[k])
						k += 1
				contents = contents[4:]
				if len(contents) > 1:
					passed = False
					l = 0
					while not passed:
						line_no = i+l+4
						if "</a>" in contents[l]:
							in_this_line = contents[l].split(">")
							monster_here = in_this_line[1][:-3]
							sorting_list = [monster, monster_here]
							sorting_list.sort()
							if sorting_list[0] == sorting_list[1]:
								passed = True
							elif monster == sorting_list[0]:
								passed = True
								new_lines.insert(line_no-1,new_html)
						elif '<li class="hline"></li>' in contents[l]:
							passed = True
							new_lines.insert(line_no,new_html)
						l += 1
				else:
					new_lines.insert(k-1+extra,new_html)

	if not found_abc:
		for i,line in enumerate(lines):
			if 'id="alphabet"' in line:
				abc_cont_found = True
				passed = False
				k=i
				while not passed:
					k+=1
					if "<h2 " in lines[k]:
						data = lines[k].split('"')
						if ord(data[1]) > ord(monster[0]):
							passed = True
							new_lines.insert(k-1,new_section)



	for i,line in enumerate(new_lines):
		if i < len(new_lines)-1:
			new_code += new_lines[i] + "\n"
		else:
			new_code += new_lines[i]
	f.close()
	f = open(filename,"w")
	f.write(new_code)
	f.close()