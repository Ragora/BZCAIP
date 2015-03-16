"""
	BZCAIP v1.0.0 Release

	Currently experimental AIP generator for BattleZone II Classic Mod.

	This software is licensed under the Draconic Free License
	version 1. Please refer to LICENSE.txt for more information.
"""

import os
import re
import sys
import random
import os.path
from contextlib import contextmanager

from settings import Settings

def processor(arg, dirname, names):
	""" Processor function that is passed in for the visit argument in os.path.walk in
	the application code below. """

	for name in names:
		filename = os.path.join(dirname, name)

		data = "None"
		try:
			with open(filename, "r") as handle:
				data = handle.read()		
		except IOError as e:
			print("WARNING: Unable to load template %s. Verbose Error:\n%s" % (filename, e))
			continue

		arg.append((name, data))

def die(message):
	""" Simple print mechanism that reports an error and closes the application
	immediately. """

	print(message)
	sys.exit(0)

def difficulties(prefix="data"):
	""" Helper function that returns a list of template files. """

	print("Loading difficulties ...")
	difficulties = [ ]
	os.path.walk(os.path.join(prefix, "templ_difficulties/"), processor, difficulties)
	if (len(difficulties) == 0): die("FATAL: No difficulties to use!")
	return difficulties

@contextmanager
def safeopen(filepath, modes):
	""" Safe open controlled execution function.

	Effectively it is just the open() function but it also helps
	reduce code redundancy and warns about programmer errors in
	the application code below.

	Keyword Arguments:
		filepath - The path to the file to open.
		modes - File modes to open with.
	"""
	if ("w" in modes):
		file_exists = True
		try: 
			with open(filepath, "r") as handle: pass
		except IOError: file_exists = False

		#if (file_exists):
		#	print("WARNING: Overwriting file: %s. This is a programmer error." % filepath)
	
	try: handle = open(filepath, modes)
	except IOError as e: die("FATAL: Unable to open %s. Verbose Error:\n%s" % (filepath, e))
	else:
		yield handle
		handle.close()

def worlds(prefix="data"):
	""" Helper function that returns a list of worlds. """

	print ("Loading world types ...")
	with safeopen(os.path.join(prefix, "worlds.txt"), "r") as handle:
		worlds = handle.read().split("\n")
		
	result = [ ]
	for world in worlds:
		result.append(world.split(":"))

	if (len(worlds) == 0): die("FATAL: No world types to use!")
	return result
	
def read(filepath):
	""" Simple read function that returns the entire contents of a given file.
	
	Keyword Arguments:
		filepath - The filepath to attempt to read from.
	"""
	
	with safeopen(filepath, "r") as handle: return handle.read()

def write(filepath, data):
	""" Simple write function shortcut.
	
	Keyword arguments:
		filepath - The filepath to attempt to write to.
		data - The data to write.
	"""
	with safeopen(filepath, "w") as handle: handle.write(data)
	
def writeline(destination, data, location):
	""" Writes a given string to the destination bytearray, overwriting
	the line it happens to be on entirely. """
	
	current_location = location
	current_index = 0
	
	destination_array = bytearray(destination)
	while (True):
		if (current_location == len(destination) or destination[current_location] == "\n"):
			break
								
		if (current_index < len(data)):
			destination_array[current_location] = data[current_index]
			current_index += 1
		else:
			destination_array[current_location] = " "
								
		current_location += 1
	
	return str(destination_array)
							
def warning(output):
	sys.stderr.write("WARNING: ")
	sys.stderr.write(output)
	sys.stderr.write("\n")

class Application:
	""" Application class merely designed for organization. """

	stagepoint_expression = re.compile("ForceStagePoint ?= ?[0-9]+", re.IGNORECASE)
	condition_expression = re.compile("planConditionPath[0-9]* *= *\"([A-z]|[0-9])+\"", re.IGNORECASE)
	buildloc_expression = re.compile("buildLoc[0-9]", re.IGNORECASE)

	# Sane Defaults for BZ2 Object counts	
	object_types = [("Supp", 3), ("Hang", 3), ("Cafe", 3), ("Comm", 3), ("HQCP", 3), ("MBld", 3), ("Silo", 6), ("Barr", 6)]
	
	def main(self):
		""" Main program "entry point" of sorts. """

		print("BZCAIP AIP Generator v1.0.0 Release")
		print("Copyright (c) 2014 Robert MacGregor")

		if (len(sys.argv) < 3): die("Usage: %s <RACE> <SOURCE FOLDER> [DESTINATION FOLDER]" % sys.argv[0])
		self.race = sys.argv[1]
		if (len(self.race) != 1): die("ERROR: Race names must be one letter in length.")
		
		# Read the destination folder
		if (len(sys.argv) == 4):
			self.write_destination = sys.argv[3]
		else:
			self.write_destination = self.race
			
		# Read the source folder
		self.data_source = sys.argv[2]
		
		# Load config
		print("Loading config.cfg ...")
		config = Settings("config.cfg")
		
		if (not config.is_good()):
			warning("Failed to load config.cfg, assuming BZ2 defaults.")
		else:
			self.object_types = [ ]
			object_type_conf = config.get_index("ObjectTypes", str).split(";")
			for object_type_name in object_type_conf:
				object_type_count_var = object_type_name + "Count"
				self.object_types.append((object_type_name, config.get_index(object_type_count_var, int)))

		self.difficulties = difficulties(self.data_source)
		self.worlds = worlds(self.data_source)

		# Create the main output dir
		destination_dir = os.path.join(self.write_destination)
		try: os.makedirs(self.write_destination)
		except OSError: pass
		# Create the subdirs
		#os.chdir(destination_dir)
		for world in self.worlds:
			if (world[0] == ""): world = [None, "Moon (default)"] # Hack
			try: os.makedirs(os.path.join(self.write_destination, world[1]))
			except OSError: pass

		self.generate_race()
		self.generate_play()
		self.generate_thug()

		print("COMPLETE: The result has been written to %s" % self.write_destination)

	def generate_race(self):
		""" Race generation step function call. """

		print("Generating race data ------------------------------")
		for template in self.difficulties:
			basename, basedata = template

			pathbase = os.path.join(self.write_destination, "Moon (default)/")
			filebase = os.path.join(pathbase, basename.replace("RACE", self.race))
			filebase = filebase.replace("NUMBER", "0")
			filename = filebase.replace("WORLD", "")
			
			print("Creating Race Definition: %s" % filename)
			filedata = str(basedata).replace("\"sb", "\"%sb" % self.race)
			filedata = filedata.replace("\"sv", "\"%sv" % self.race)
			filedata = filedata.replace("REPLACE\"", "\"")
			write(filename, filedata)

			for world in self.worlds:
				# Don't overwrite definitions
				if (world[0] == ""): continue

				filebase = "%s/%s" % (world[1], basename.replace("RACE", self.race))
				filebase = os.path.join(self.write_destination, filebase)
				filebase = filebase.replace("NUMBER", "0")
				filename = filebase.replace("WORLD", world[0])

				print("Creating Race World Info: %s " % filename)
				filedata = str(basedata).replace("REPLACE\"", "%s\"" % world)
				filedata = filedata.replace("\"sb", "\"%sb" % self.race)
				filedata = filedata.replace("\"sv", "\"%sv" % self.race)
				filedata = self.generate_objectdata(basename, filedata)
				write(filename, filedata)

	def generate_play(self):
		""" Play generation step function call. """

		#print("Generating team data ------------------------------")
		for world in self.worlds:
			world_filepath = world[1]
			if (world_filepath == ""): world_filepath = "Moon (default)"

			for template in self.difficulties:
				basename, basedata = template

				filebase = "%s/%s" % (world_filepath, basename.replace("RACE", self.race))
				filebase = filebase.replace("WORLD", world[0])
				filebase = os.path.join(self.write_destination, filebase)
				
				for i in range(1, 5):
					filepath = filebase.replace("NUMBER", str(i))
					print("Creating play information: %s" % filepath)

					filedata =  str(basedata).replace("\"0", "\"%i" % i)
					filedata = filedata.replace("\"sb", "\"%sb" % self.race)
					filedata = filedata.replace("\"sv", "\"%sv" % self.race)
					
					# Write Stage Point Information
					# TODO: Verify that it operates correctly.
					lastindex = 0
					
					# Iterate over all of the stagepoint information
					match_iter = self.stagepoint_expression.finditer(filedata)
					for match in match_iter:
						result_stagepoint = int(match.group(0).split("=")[1]) + 3 * i
						
						start_point = match.start()
						end_point = match.end()
						
						# In Bytes
						desired_length = end_point - start_point
						result_string = "ForceStagePoint=%u" % result_stagepoint
							
						# Write the result to our filedata
						filedata = writeline(filedata, result_string, start_point)

					# NOTE: Was probably supposed to be done in the previous step?
					filedata = filedata.replace("REPLACE\"", "%s\"" % world[0])
					
					filedata = self.generate_objectdata(basename, filedata)
					write(filepath, filedata)

	def generate_thug(self):
		""" Thug generation step function call. """

		thug_data = read(os.path.join(self.data_source, "templ_THUG.aip"))
		for world in self.worlds:
			world_filepath = world[1]
			if (world_filepath == ""): world_filepath = "Moon (default)"
			
			file_data = str(thug_data)

			file_name = "%s/bzcthug_%s%s.aip" % (world_filepath, self.race, world[0])
			file_name = os.path.join(self.write_destination, file_name)
			print("Generating THUG: %s" % file_name)

			file_data = file_data.replace("\"sb", "\"%sb" % self.race)
			file_data = file_data.replace("\"sv", "\"%sv" % self.race)
			file_data = file_data.replace("REPLACE\"", "%s\"" % world[0])
			
			file_data = self.generate_objectdata(file_name, file_data)
			write(file_name, file_data)
			
	def generate_objectdata(self, templatename, filedata):
		""" Writes out the BZ2 object data to filedata. """
		
		for object_definition in self.object_types:
			object_name, object_count = object_definition
			object_possibilities = range(1, object_count + 1)
			
			# TODO: Move this to program init so that it's a little bit
			# more efficient
			condition_expr = re.compile("planConditionPath[0-9]* *= *\"[0-9]*%s[0-9]*\"" % object_name, re.IGNORECASE)
			
			condition_match_iter = condition_expr.finditer(filedata)
			for condition_match in condition_match_iter:
				if (len(object_possibilities) == 0):
					warning("Too many occurances of %s in template %s to randomize ID's for! It is likely that your config.cfg is wrong." % (object_name, templatename))
					break
					
				condition_match_text = condition_match.group(0)
				
				# Now locate the data we want to change
				condition_match_split = condition_match_text.split("=")
				condition_value = condition_match_split[1].strip("\" ")
				condition_value_split = condition_value.split(object_name)
				
				team_id = condition_value_split[0]
				
				# What was that condition #?
				condition_number = condition_match_split[0].strip("planconditionpathPLANCONDITIONPATH ")
				# Pick a number
				random_num = object_possibilities.pop(random.randint(0, len(object_possibilities) - 1))
				
				# Construct the new value, we'll need it later
				result_value = "%s%s%u" % (team_id, object_name, random_num)
				result_string = "planConditionPath%s=\"%s\"" % (condition_number, result_value)

				# Write the new planConditionPath to our filedata
				filedata = writeline(filedata, result_string, condition_match.start())
				
				# Now grab the next buildLoc#
				buildloc_location = filedata.find("buildLoc1", condition_match.start())
				if (buildloc_location != -1):
					result_string = "buildLoc1 = \"%s\"" % result_value
					filedata = writeline(filedata, result_string, buildloc_location)
				else:
					print("BAD")
			
				
		return filedata

if __name__ == "__main__":
	Application().main()
