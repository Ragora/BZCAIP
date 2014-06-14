"""
	BZCAIP v1.0.0 Release

	Currently experimental AIP generator for BattleZone II Classic Mod.

	This software is licensed under the Draconic Free License
	version 1. Please refer to LICENSE.txt for more information.
"""

import os
import re
import sys
import os.path
from contextlib import contextmanager

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

def difficulties():
	""" Helper function that returns a list of template files. """

	print("Loading difficulties ...")
	difficulties = [ ]
	os.path.walk("data/templ_difficulties/", processor, difficulties)
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

def worlds():
	""" Helper function that returns a list of worlds. """

	print ("Loading world types ...")
	with safeopen("data/worlds.txt", "r") as handle:
		worlds = handle.read().split("\n")

	if (len(worlds) == 0): die("FATAL: No world types to use!")
	return worlds
	
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

class Application:
	""" Application class merely designed for organization. """

	stagepoint_expression = re.compile("ForceStagePoint ?= ?[0-9]+", re.IGNORECASE)
	
	def main(self):
		""" Main program "entry point" of sorts. """

		print("BZCAIP AIP Generator v1.0.0 Release")
		print("Copyright (c) 2013 Robert MacGregor")

		if (len(sys.argv)  < 2): die("Usage: %s <RACE>" % sys.argv[0])
		self.race = sys.argv[1]
		if (len(self.race) != 1): die("ERROR: Race names must be one letter in length.")

		self.difficulties = difficulties()
		self.worlds = worlds()

		# Create the main output dir
		try: os.makedirs(self.race)
		except OSError: pass
		# Create the subdirs
		os.chdir(self.race)
		for world in self.worlds:
			if (world == ""): world = "Moon (default)"
			try: os.makedirs(world)
			except OSError: pass
		# Yea, I know, hacky hack to avoid having to change the logic everywhere else for this
		os.chdir("../")

		self.generate_race()
		self.generate_play()
		self.generate_thug()

		print("COMPLETE: The result has been written to %s" % self.race)

	def generate_race(self):
		""" Race generation step function call. """

		#print("Generating race data ------------------------------")
		for template in self.difficulties:
			basename, basedata = template

			pathbase = "%s/Moon (default)/" % self.race
			filebase = os.path.join(pathbase, basename.replace("RACE", self.race))
			filebase = filebase.replace("NUMBER", "0")
			filename = filebase.replace("WORLD", "")
			
			#print("Creating Race Definition: %s" % filename)
			filedata = str(basedata).replace("\"sb", "\"%sb" % self.race)
			filedata = filedata.replace("\"sv", "\"%sv" % self.race)
			filedata = filedata.replace("REPLACE\"", "\"")
			write(filename, filedata)

			for world in self.worlds:
				# Don't overwrite definitions
				if (world == ""): continue

				filebase = "%s/%s/%s" % (self.race, world, basename.replace("RACE", self.race))
				filebase = filebase.replace("NUMBER", "0")
				filename = filebase.replace("WORLD", world)

				#print("Creating Race World Info: %s " % filename)
				filedata = str(basedata).replace("REPLACE\"", "%s\"" % world)
				filedata = filedata.replace("\"sb", "\"%sb" % self.race)
				filedata = filedata.replace("\"sv", "\"%sv" % self.race)
				write(filename, filedata)

	def generate_play(self):
		""" Play generation step function call. """

		#print("Generating team data ------------------------------")
		for world in self.worlds:
			world_filepath = world
			if (world_filepath == ""): world_filepath = "Moon (default)"

			for template in self.difficulties:
				basename, basedata = template

				filebase = "%s/%s/%s" % (self.race, world_filepath, basename.replace("RACE", self.race))
				filebase = filebase.replace("WORLD", world)
				
				for i in range(1, 5):
					filepath = filebase.replace("NUMBER", str(i))
					#print("Creating play information: %s" % filepath)

					filedata =  str(basedata).replace("\"0", "\"%i" % i)
					filedata = filedata.replace("\"sb", "\"%sb" % self.race)
					filedata = filedata.replace("\"sv", "\"%sv" % self.race)
					
					# Write Stage Point Information
					# TODO: Verify that it operates correctly.
					lastindex = 0
					
					# Iterate over all of the stagepoint information
					match_iter = self.stagepoint_expression.finditer(filedata)
					file_array = bytearray(filedata)
					for match in match_iter:
						result_stagepoint = int(match.group(0).split("=")[1]) + 3 * i
						
						start_point = match.start()
						end_point = match.end()
						
						# In Bytes
						desired_length = end_point - start_point
						result_string = "ForceStagePoint=%u" % result_stagepoint
							
						# Write the result to our filedata
						current_location = start_point
						current_index = 0
						while (True):
							if (filedata[current_location] == "\n"):
								break
								
							if (current_index < len(result_string)):
								file_array[current_location] = result_string[current_index]
								current_index += 1
							else:
								file_array[current_location] = " "
								
							current_location += 1
							
						filedata = str(file_array)

					# NOTE: Was probably supposed to be done in the previous step?
					filedata = filedata.replace("REPLACE\"", "%s\"" % world)
					
					write(filepath, filedata)

	def generate_thug(self):
		""" Thug generation step function call. """

		thug_data = read("data/templ_THUG.aip")
		for world in self.worlds:
			world_filepath = world
			if (world_filepath == ""): world_filepath = "Moon (default)"
			
			file_data = str(thug_data)

			file_name = "%s/%s/bzcthug_%s%s.aip" % (self.race, world_filepath, self.race, world)
			#print("Generating THUG: %s" % file_name)

			file_data = file_data.replace("\"sb", "\"%sb" % self.race)
			file_data = file_data.replace("\"sv", "\"%sv" % self.race)
			file_data = file_data.replace("REPLACE\"", "%s\"" % world)
	
			write(file_name, file_data)

if __name__ == "__main__":
	Application().main()
