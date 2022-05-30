import os
import re
import json
import time
import glob
import requests
from os import system
from tkinter import Tk, filedialog

def single_film(film, vtype="movie", year=""):
	api_file = open("data/API_Key.txt", "r")
	api_key = api_file.readline().strip()
	param = {"t": film, "type": vtype, "r": "json", "apikey": api_key, "y":year}
	file = requests.get("http://www.omdbapi.com/", params=param)
	api_file.close()
	return file.json()

def multiple_films(detail_list):
	if detail_list != []:
		for name, year in detail_list:
			jfile = single_film(film=name, year=year)
			write_json(jfile)
			display(jfile, name)

def display(json, film_name):
	try:
		if json["Response"] == 'True' and json["Type"] == 'movie':
			print("\n\t {} ({})\n".format(json["Title"], json["Year"]))
			print(" IMDB Rating:\t{} from {} Votes.\n Language:\t{}\n Runtime:\t{}\n Genre:\t\t{}\n".format(json["imdbRating"], json["imdbVotes"], json["Language"], json["Runtime"], json["Genre"]))
			print(" Director:\t{}\n Writer:\t{}\n Actors:\t{} \n Awards:\t{}\n BoxOffice:\t{}\n".format(json["Director"], json["Writer"], json["Actors"], json["Awards"], json["BoxOffice"]))
			print(" Plot:\n {}\n".format(json["Plot"]))
		elif json["Response"] == 'True' and json["Type"] == 'series':
			print("\t {} ({})\n".format(json["Title"], json["Year"]))
			print(" IMDB Rating:\t{} from {} Votes.\n Language:\t{}\n Runtime:\t{}\n Genre:\t\t{}\n Total Seasons:\t{}\n".format(json["imdbRating"], json["imdbVotes"], json["Language"], json["Runtime"], json["Genre"], json["totalSeasons"]))
			print(" Director:\t{}\n Writer:\t{}\n Actors:\t{} \n Awards:\t{}\n".format(json["Director"], json["Writer"], json["Actors"], json["Awards"]))
			print(" Plot:\n {}\n".format(json["Plot"]))
		else:
			print(" Information - '" + film_name + "' Movie/Series not found.")
	except Exception as e:
		pass

def extract_details(path):
	clean_list = []
	with open(path,"r") as detail_file:
		for i in detail_file:
			temp1 = re.sub("[-.,\(\):_]"," ", i).replace("  "," ")
			temp2 = re.search("^([a-zA-Z0-9 ]*) ([0-9]{4})", temp1)
			try:
				clean_list.append((temp2[1].lower(), temp2[2]))
			except:
				clean_list.append((temp1.lower(), ""))
		return clean_list

def write_json(file):
	fname = "data/Movie_details.json"
	try:
		if file["Response"] == 'True':
			if not os.path.isfile(fname):
				with open(fname,"w") as write_file:
					write_file.write("[\n")
					write_file.write(json.dumps(file, indent=2))
					write_file.write(",\n")
			else:
				if offline_read(file["Title"], file["Year"]):
					with open(fname,"a") as write_file:
						write_file.write(json.dumps(file, indent=2))
						write_file.write(",\n")
	except:
		pass
		
def offline_read(film_name, year):
	fname = "data/Movie_details.json"
	if os.path.isfile(fname):
		with open(fname, "r") as read_file:
			jfile = json.loads((read_file.read()[:-2]+"\n]"))
			for i in jfile:
				if i["Title"] == film_name and i["Year"] == year:
					return False
		return True

def menu():
	print("\n\n\t\t      --------------------------")
	print("\t\t\t MOVIE DETAILS FINDER ")
	print("\t\t      --------------------------")
	print("\n 1. Find Single Movie/Series Details\n 2. Find Multiple Movies Details\n 3. Generate a text file from Movies located at Local drive\n 4. Exit")

def user_selection_single():
	film_name = input("\n Movie/Series Title: ")
	try:
		film_year = int(input(" Movie/Series Year: "))
	except:
		film_year = ""
	film_type = input(" Movie/Series Type ([default: Movie][s/S for Series]): ")
	print("\n Results:")
	try:
		if film_type == 's' or film_type == 'S':
			display(single_film(film = film_name, vtype= "Series", year = film_year), film_name)
		else:
			display(single_film(film = film_name, year = film_year), film_name)
	except:
		print("\n Please check your internet connection & Try again!")
	question1 = input(" Do you want to find details about another movie? (y/n): ")
	if question1 == "y":
		user_selection_single()
	else:
		pass

def user_selection_multiple(user_input="manual", file_path=""):
	if user_input == "manual":
		print("\n Please select the file containing movie names (.TXT).")
		root = Tk().withdraw()
		path_text = filedialog.askopenfilename(initialdir="/", filetypes=[("Text File (.txt)", ".TXT")], title='Select the Text File...')
		try:
			multiple_films(extract_details(path_text))
		except:
			print("\n Please check your internet connection & Try again!")
		question2 = input(" Do you want to try again? (y/n): ")
		if question2 == "y":
			user_selection_multiple()
	else:
		try:
			multiple_films(extract_details(file_path))
		except:
			print("\n Please check your internet connection & Try again!")

def user_selection_textfile():
	print("\n Please select the directory containing Movies...")
	root = Tk().withdraw()
	dir_path = filedialog.askdirectory(initialdir="/", title='Select the Directory...')
	save_file = "{}.txt".format(os.path.basename(dir_path))
	film_names_list = [os.path.basename(t) for t in glob.glob(dir_path + "/*")]
	save_file_path = os.path.dirname(os.path.realpath(save_file))
	print("\n Selected Directory Path: {}".format(dir_path))
	print(" Generated Text file Path: {}\\{}\n\n Movie List: \n".format(save_file_path, save_file))
	with open(save_file, "w") as file:
	    for film in film_names_list:
	        file.write(film+"\n")
	        print(" "+film)
	question3 = input("\n Do you want to find details about these movies? (y/n): ")
	if question3 == "y":
		user_selection_multiple(user_input="auto", file_path=save_file)
		os.system("pause")
	else:
		pass
	
def user_choice():
	menu()
	user_selection = input("\n Please select an option: ")
	if user_selection == "1":
		print("\n\t Single Movie Details")
		user_selection_single()
	elif user_selection == "2":
		print("\n\t Multiple Movie Details")
		user_selection_multiple()
	elif user_selection == "3":
		print("\n\t Text File Generater")
		user_selection_textfile()
	elif user_selection == "4":
		pass
	else:
		print("\nInvalied Input! Please try again...")
		time.sleep(2)
		system('cls')
		user_choice()

def main():
	user_choice()

main()

