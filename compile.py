"""
	Compiler script that sticks the compiled version of BZCAIP in
	the dist folder with the data.

	This software is licensed under the GNU General Public License
	version 3. Please refer to gpl.txt for more information.
	Copyright (c) 2004 Robert MacGregor
"""

import shutil

import source

if __name__ == "__main__":
	shutil.copyfile("source/bzcaip.pyc", "dist/bzcaip.pyc")
