import math
import csv

def jaccard_coefficient(path1, path2):
	doc1 = open(path1,"r",encoding='utf-8', errors='ignore').read()
	doc2 = open(path2,"r",encoding='utf-8', errors='ignore').read()

	punctuations = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
	for char in punctuations:
		doc1 = doc1.replace(char, "")
		doc2 = doc2.replace(char, "")

	doc1_words = doc1.split(" ")
	doc2_words = doc2.split(" ")

	union = list(set(doc1) | set(doc2))
	intersection = list(set(doc1) & set(doc2))

	jc = len(intersection)/float(len(union))

	return jc


def cosine_similarity(path1, path2):
	doc1 = open(path1,"r",encoding='utf-8', errors='ignore').read()
	doc2 = open(path2,"r",encoding='utf-8', errors='ignore').read()

	punctuations = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
	for char in punctuations:
		doc1 = doc1.replace(char, "")
		doc2 = doc2.replace(char, "")

	doc1 = doc1.replace("\n", " ")
	doc2 = doc2.replace("\n", " ")
		
	doc1_words = doc1.split(" ")
	doc2_words = doc2.split(" ")

	union = list(set(doc1_words) | set(doc2_words))
	
	mod_value1 = 0
	mod_value2 = 0
	dot_product = 0
	for i in union:
		tf1 = 1 + math.log10(doc1_words.count(i))
		tf2 = 1 + math.log10(doc2_words.count(i))

		idf = 0
		if (tf1 > 1) and (tf2 > 1):
			pass
		elif (tf1 > 1) or (tf2 > 1):
			idf = math.log10(2)

		dot_product += (tf1*idf)*(tf2*idf)
		mod_value1 += (tf1*idf)**2
		mod_value2 += (tf2*idf)**2

	mod_value1 = mod_value1**(1/2)
	mod_value2 = mod_value2**(1/2)

	cs = dot_product/(mod_value1*mod_value2)

	return cs

while (1):
	print("Entering '1' will train from the data.")
	print("Entering '2' will take a English document as input and translate it to French document.")
	print("Entering '3' will take a French document as input and translate it to English document.")
	print("Entering '4' will take a set of English documents as input and translate it to corresponding French documents.")
	print("Entering '5' will take a set of French documents as input and translate it to corresponding English documents.")

	decision = int(input())
	if decision == 1:
		train()
	elif decision == 2:
		csv = open("frenchToEnlgish.csv","r",encoding='utf-8', errors='ignore').read()
		lines = csv.splitlines()

		english_to_french = {}
		for i in lines:
			temp = i.split(",")
			english_to_french[temp[1]] = temp[2]

		file_path_name = input("Please enter the English text filename that has to be translated to French with path and extension included : ")
		file_path_name_acc = input("Please enter the French text filename that is an accurate translation with path and extension included : ")
		file_path = open(file_path_name,"r",encoding='utf-8', errors='ignore').read()
		file_path = file_path.lower()

		punctuations = '''!|()-[]{};:"\,<>./?@#$%^&*_~'''
		for char in punctuations:
				file_path = file_path.replace(char, "")

		file_sentences = file_path.splitlines()
		with open("english_to_french.txt", 'a') as out:
			for i in file_sentences:
				for j in i.split(" "):
					out.write(english_to_french[j] + " ")
				out.write("\n")

		print("Jaccard Coeffiecient : " + str(jaccard_coefficient(file_path_name_acc, "english_to_french.txt")))
		print("Cosine Similarity : " + str(cosine_similarity(file_path_name_acc, "english_to_french.txt")))

	elif decision == 3:
		csv = open("frenchToEnlgish.csv","r",encoding='utf-8', errors='ignore').read()
		lines = csv.splitlines()

		french_to_english = {}
		for i in lines:
			temp = i.split(",")
			french_to_english[temp[2]] = temp[1]

		file_path_name = input("Please enter the French text filename that has to be translated to English with path and extension included : ")
		file_path_name_acc = input("Please enter the French text filename that is an accurate translation with path and extension included : ")
		file_path = open(file_path_name,"r",encoding='utf-8', errors='ignore').read()
		file_path = file_path.lower()

		punctuations = '''!|()-[]{};:"\,<>./?@#$%^&*_~'''
		for char in punctuations:
				file_path = file_path.replace(char, "")

		file_sentences = file_path.splitlines()
		with open("french_to_english.txt", 'a') as out:
			for i in file_sentences:
				for j in i.split(" "):
					out.write(french_to_english[j] + " ")
				out.write("\n")

		print("Jaccard Coeffiecient : " + str(jaccard_coefficient(file_path_name_acc, "french_to_english.txt")))
		print("Cosine Similarity : " + str(cosine_similarity(file_path_name_acc, "french_to_english.txt")))

	elif decision == 4:
		csv = open("frenchToEnlgish.csv","r",encoding='utf-8', errors='ignore').read()
		lines = csv.splitlines()

		english_to_french = {}
		for i in lines:
			temp = i.split(",")
			english_to_french[temp[1]] = temp[2]

		no = int(input("Enter the number of English text files to be translated to French : "))
		jc_avg = 0
		cs_avg = 0
		for n in range(0,no):
			file_path_name = input("Please enter the " + str(n+1) + " English text filename that has to be translated to French with path and extension included : ")
			file_path_name_acc = input("Please enter the French text filename that is an accurate translation with path and extension included : ")
			file_path = open(file_path_name,"r",encoding='utf-8', errors='ignore').read()
			file_path = file_path.lower()

			punctuations = '''!|()-[]{};:"\,<>./?@#$%^&*_~'''
			for char in punctuations:
					file_path = file_path.replace(char, "")

			file_sentences = file_path.splitlines()
			with open("english_to_french" + str(n+1) + ".txt", 'a') as out:
				for i in file_sentences:
					for j in i.split(" "):
						out.write(english_to_french[j] + " ")
					out.write("\n")
			jc = jaccard_coefficient(file_path_name_acc, "english_to_french" + str(n+1) + ".txt")
			cs = cosine_similarity(file_path_name_acc, "english_to_french" + str(n+1) + ".txt")

			jc_avg += jc
			cs_avg += cs

			print("Jaccard Coeffiecient : " + str(jc))
			print("Cosine Similarity : " + str(cs))

		print("Average Jaccard Coefficient : " + str(jc_avg/no))
		print("Average Cosine Similarity : " + str(cs_avg/no))


	elif decision == 5:
		csv = open("frenchToEnlgish.csv","r",encoding='utf-8', errors='ignore').read()
		lines = csv.splitlines()

		french_to_english = {}
		for i in lines:
			temp = i.split(",")
			french_to_english[temp[2]] = temp[1]

		no = int(input("Enter the number of French text files to be translated to English : "))
		jc_avg = 0
		cs_avg = 0
		for n in range(0,no):
			file_path_name = input("Please enter the " + str(n+1) + " French text filename that has to be translated to English with path and extension included : ")
			file_path_name_acc = input("Please enter the English text filename that is an accurate translation with path and extension included : ")
			file_path = open(file_path_name,"r",encoding='utf-8', errors='ignore').read()
			file_path = file_path.lower()

			punctuations = '''!|()-[]{};:"\,<>./?@#$%^&*_~'''
			for char in punctuations:
					file_path = file_path.replace(char, "")

			file_sentences = file_path.splitlines()
			with open("french_to_english" + str(n+1) + ".txt", 'a') as out:
				for i in file_sentences:
					for j in i.split(" "):
						out.write(french_to_english[j] + " ")
					out.write("\n")

			jc = jaccard_coefficient(file_path_name_acc, "french_to_english" + str(n+1) + ".txt")
			cs = cosine_similarity(file_path_name_acc, "french_to_english" + str(n+1) + ".txt")

			jc_avg += jc
			cs_avg += cs

			print("Jaccard Coeffiecient : " + str(jc))
			print("Cosine Similarity : " + str(cs))

		print("Average Jaccard Coefficient : " + str(jc_avg/no))
		print("Average Cosine Similarity : " + str(cs_avg/no))
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

