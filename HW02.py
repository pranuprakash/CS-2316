import csv
from pprint import pprint
import requests
import json
from bs4 import BeautifulSoup
import re

### DO NOT MODIFY THE FOLLOWING METHOD ###
def date_cleaner(string):
	mapping = {"January":"01", "February":"02", "March":"03",
				   "April":"04",   "May":"05",      "June":"06",
				   "July":"07",    "August":"08",   "September":"09",
				   "October":"10", "November":"11", "December":"12"}
	MM = mapping[string.split()[0]]
	DD = string.split(",")[0].split()[1]
	DD = "0" + DD if len(DD) == 1 else DD
	YYYY = string.split(",")[1].strip()
	date_str = f"{MM}/{DD}/{YYYY}"
	return date_str
##########################################

def shrek_script(file_name, output_file):
	newlist = []
	count = 1
	length_count = 0

	with open(f"{file_name}.txt", "r") as f:
		text = f.readlines()

	for i in text:
		# print(i.strip())
		# print(len(i.strip().split()))
		
		length_count += len(i.strip().split())
		if "Shrek" in i.strip():
			newlist.append([count, len(i.strip().split()), length_count, True, i.strip()])
			# with open(f"{output_file}.csv", "a") as a:
			# 	a.write(str([count, len(i.strip().split()), length_count, True, i.strip()]))
			# 	a.write("\n")
		else:
			newlist.append([count, len(i.strip().split()), length_count, False, i.strip()])
			# with open(f"{output_file}.csv", "a") as a:
			# 	a.write(str([count, len(i.strip().split()), length_count, False, i.strip()]))
			# 	a.write("\n")
		count += 1
	
	# for i in text:
	# 	length_count += len(i.strip().split())
	# 	if "Shrek" in i.strip():
	# 		newlist.append([count, len(i.strip().split()), length_count, True, i.strip()])

	# 	else:
	# 		newlist.append([count, len(i.strip().split()), length_count, False, i.strip()])
	# 	count += 1

	with open(f"{output_file}.csv", "w") as w:
		writer_object = csv.writer(w)
		writer_object.writerows(newlist)

	return newlist

def csv_parser(filename):
	with open(filename, "r", encoding = "utf8") as r:
		header = r.readline()
		reader = csv.reader(r, delimiter=",")
		reader_list = list(reader)

	# print(header)
	# return(reader_list[2])

	final_list = []
	final_list.append(["ID", "IsMovie", "IsShow", "Title", "Director/s", "CastList", "CastSize", "Rating", "DateAdded", "IsHorror", "Synopsis"])

	for i in reader_list:
		# pprint(i)
		# break
		new_string = ""

		id = i[0]
		is_movie = True if i[1] == "Movie" else False
		is_show = True if i[1] == "TV Show" else False
		title = i[2]
		director = "NIA" if i[3] == "" else i[3]

		if i[4] == "":
			cast_list_end = []

		else:
		
			cast_list_start = [j.strip() for j in i[4].split(",")]

			new_cast_list = []
			for a in cast_list_start:
				new_name = ""
				first_last = a.split()
				if len(first_last) > 1:
					new_name = first_last[0][0] + ". " + first_last[-1]

				else:
					new_name = first_last[0]

				new_cast_list.append(new_name)
			
			cast_list_end = new_cast_list # amended list 
			
		# cast_list_end = [] if i[4] == "" else [j.strip() for j in i[4].split(",")]

		cast_size = 0 if i[4] == "" else len(cast_list_end)
		rating = i[8]
		date_added = "NIA" if i[6] == "" else date_cleaner(i[6]) # index 6
		is_horror = "Horror" if "Horror" in i[10] else "Not Horror"

		new_string = " ".join(i[-1].split()[0:10])

		synopsis = new_string + "..." # index (-1)

		final_list.append([id, is_movie, is_show, title, director, cast_list_end, cast_size, rating, date_added, is_horror, synopsis])

	return final_list

def json_parser(filename):
	adict = json.load(open(filename))

	# pprint(adict["s2"])

	final_list = []

	for key, val in adict.items():
		final_dict = {}
		# print(final_dict)

		# cast_list = [] if val["cast"] == "" else [i for i in val["cast"].split(",")]

		if val["cast"] == None: # csv "" for json ??
			cast_list_end = []

		else:
		
			cast_list_start = [j.strip() for j in val["cast"].split(",")]

			new_cast_list = []
			for a in cast_list_start:
				new_name = ""
				first_last = a.split()
				if len(first_last) > 1:
					new_name = first_last[0][0] + ". " + first_last[-1]

				else:
					new_name = first_last[0]

				new_cast_list.append(new_name)
			
			cast_list_end = new_cast_list # amended list 

		cast_size = 0 if val["cast"] == None else len(cast_list_end)
		date_added = "NIA" if val["date_added"] == None else date_cleaner(val["date_added"])
		director = "NIA" if val["director"] == None else val["director"]
		is_horror = "Horror" if "Horror" in val["listed_in"] else "Not Horror"
		is_movie = True if val["type"] == "Movie" else False
		is_show = True if val["type"] == "TV Show" else False
		rating = val["rating"]
		title = val["title"]

		final_string = " ".join(val["description"].split()[0:10])
		final_string += "..."

		synopsis = final_string

		final_dict = {"CastList": cast_list_end, "CastSize": cast_size, "DateAdded": date_added, "Director/s": director , "ID": key, "IsHorror": is_horror, "IsMovie": is_movie, "IsShow": is_show, "Rating": rating, "Synopsis": synopsis, "Title": title}

		final_list.append(final_dict)

	return final_list

def horror(csv_data, json_data, filename):
	# pprint(json_data)
	final_dict = {}
	movie_dict = {("0" + str(i)) if i < 10 else (str(i)):{"num_horror":0, "total":0} for i in range(1,13)} 
	show_dict = {("0" + str(j)) if j < 10 else (str(j)):{"num_horror":0, "total":0} for j in range(1,13)}
	show_dict["NIA"] = {"num_horror": 0, "total": 0}
	
	movie_dict["overall"] = {"num_horror":0, "total":0}
	show_dict["overall"] = {"num_horror":0, "total":0}

	# pprint(movie_dict)
	# pprint(show_dict)

	for data in json_data:
		# date_added = re.findall("\d\d|NIA", data["DateAdded"])
		# print(date_added[0])
		# break

		if data['IsMovie'] == True:
			if data['IsHorror'] == "Horror":
				date_added = re.findall("\d\d", data['DateAdded'])[0]
				movie_dict[date_added]['num_horror'] += 1
				movie_dict[date_added]['total'] += 1
				movie_dict['overall']['num_horror'] += 1
				movie_dict['overall']['total'] += 1

			else:
				date_added = re.findall("\d\d", data['DateAdded'])[0]
				movie_dict[date_added]['total'] += 1
				movie_dict['overall']['total'] += 1
		else:
			if data['IsHorror'] == "Horror":
				date_added = re.findall("\d\d|NIA", data['DateAdded'])[0]
				show_dict[date_added]['num_horror'] += 1
				show_dict[date_added]['total'] += 1
				show_dict['overall']['num_horror'] += 1
				show_dict['overall']['total'] += 1

			else:
				date_added = re.findall("\d\d|NIA", data['DateAdded'])[0]
				show_dict[date_added]['total'] += 1
				show_dict['overall']['total'] += 1	

	for csv in csv_data[1:]:

		if csv[1] == True:
			if csv[-2] == "Horror":
				date_added = re.findall("\d\d", csv[-3])[0]
				movie_dict[date_added]["num_horror"] += 1
				movie_dict[date_added]["total"] += 1
				movie_dict["overall"]["num_horror"] += 1
				movie_dict["overall"]["total"] += 1

			else:
				date_added = re.findall("\d\d", csv[-3])[0]
				movie_dict[date_added]["total"] += 1
				movie_dict["overall"]["total"] += 1
		else:
			if csv[-2] == "Horror":
				date_added = re.findall("\d\d|NIA", csv[-3])[0]
				show_dict[date_added]["num_horror"] += 1
				show_dict[date_added]["total"] += 1
				show_dict["overall"]["num_horror"] += 1
				show_dict["overall"]["total"] += 1

			else:
				date_added = re.findall("\d\d|NIA", csv[-3])[0]
				show_dict[date_added]["total"] += 1
				show_dict["overall"]["total"] += 1				

	final_dict["Movie"] = movie_dict
	final_dict["Show"] = show_dict

	with open(filename, "w") as w:
		json.dump(final_dict, w)

	return final_dict

	#\d\d|NIA


def character_info(page):
	base = "https://api.disneyapi.dev/characters?page="
	url = base + str(page)

	request = requests.get(url)
	data = request.json()

	# pprint(data)

	final_list = []

	for i in range(len(data["data"])):
		if len(data["data"][i]["films"]) >= 1:
			name = data["data"][i]["name"]
			id = data["data"][i]["_id"]
			films = data["data"][i]["films"]

			if len(data["data"][i]["tvShows"]) == 0:
				tvShows = "None"
			else:
				tvShows = data["data"][i]["tvShows"]


			final_list.append((name, id, films, tvShows))

		else:
			continue

	
	return sorted(final_list, key=lambda x: len(x[2]), reverse=True)

	# pprint(data["data"][0])

def glee_dict(filename):
	soup = BeautifulSoup(open(filename), "html.parser")

	final_dict = {}
	tag_1 = soup.find("table", {"style": "text-align:center; width:99%;"})
	# print(tag_1)

	table_row = tag_1.find_all("tr")
	# print(table_row)

	count = 1
	# key_glee = f"Season {count}"

	for sub_tag in table_row[2:]:
		# print(sub_tag)
		# break
		sub_dict = {}

		val_list = sub_tag.find_all("td")
		# print(val_list[1])
		# break

		val_premier  = re.findall("[0123456789.]+", val_list[1].text)[0] # index 1
		# print(val_premier)

		val_finale = re.findall("[0123456789.]+", val_list[2].text)[0] # index 2 
		# print(val_finale)
		# break

		sub_dict["Finale Views"] = f"{val_finale} million"
		sub_dict["Premiere Views"] = f"{val_premier} million"

		if float(val_finale) > float(val_premier):
			diff = round(((float(val_finale) / float(val_premier)) - 1) * 100,2)
			sub_dict["Retention"] = f"{diff}% increase"
			sub_dict["Success"] = True
			final_dict[f"Season {count}"] = sub_dict
			# print(final_dict)
			count += 1

		else:
			diff = round((1 - (float(val_finale) / float(val_premier))) * 100,2)
			sub_dict["Retention"] = f"{diff}% decrease"
			sub_dict["Success"] = False
			final_dict[f"Season {count}"] = sub_dict
			# print(final_dict)
			count += 1

	return final_dict


def colorful_film():
	url = 'https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films'
	res = requests.get(url)
	src_code = res.text

	# print(src_code)

	soup = BeautifulSoup(src_code, "html.parser")
	# print(soup)

	table_tag = soup.find_all("table")
	# print(table_tag)

	final_list = []

	for sub_tag in table_tag:
		winner = sub_tag.find_all("tr", {"style": "background:#EEDD82"})

		for i in winner:
			sub_list = []
			check = i.find_all("td")
			# print(check[3])
			# break

			title = re.findall(".", check[0].text)
			clean_title = "".join(title)
			sub_list.append(clean_title)

			year = re.findall("[1234567890]+", check[1].text)[0]
			sub_list.append(int(year))

			wins = re.findall("[1234567890]+", check[2].text)[0]
			sub_list.append(int(wins))

			nominations = re.findall("[1234567890]+", check[3].text)[0]
			sub_list.append(int(nominations))

			# print(sub_list)

			final_list.append(sub_list)

	return sorted(final_list, key=lambda x:x[1])


if __name__ == "__main__":
	# pprint(shrek_script('shrek', 'shrek_clean'))

	# pprint(csv_parser('netflix.csv'))

	# pprint(json_parser('netflix.json'))

	# clean_csv = csv_parser('netflix.csv')
	# clean_json = json_parser('netflix.json')
	# pprint(horror(clean_csv, clean_json, 'double_analysis.json'))

	# print(character_info(49))
	# print(character_info(72))

	# print(glee_dict('glee.html'))

	# print(colorful_film())