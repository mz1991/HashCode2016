import csv

def read_csv(file,separator):
	return csv.DictReader(f,delimiter=separator)

def open_file(path,operation=""):
	# for the operation type see: http://stackoverflow.com/questions/1466000/python-open-built-in-function-difference-between-modes-a-a-w-w-and-r
	if operation!="":
		return open(path,operation)
	else:
		return open(path)
	
def close_file(file):
	file.close()

def dict_reader_to_list(dict_reader):
	return list(dict_reader)

def read_line(path):
	f = open_file(path)
	lines = [line.rstrip('\n') for line in f]
	close_file(f)
	return lines
	
def generate_list_of_numbers(min, max):
	# [min,max)
	return list(range(min,max))

def write_list_to_file(file,lines):
	# use the separator w+ to create the file if it does not exist
	for l in lines:
		file.write(l+'\n')

def split_list(lines,split_char):
	return [x.split(split_char) for x in lines]