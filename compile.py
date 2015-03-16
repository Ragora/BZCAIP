"""
	Compiler script that sticks the compiled version of BZCAIP in
	the dist folder with the data.

	This software is licensed under the MIT license. Refer to LICENSE.txt
    for more information.
"""

import shutil

import source

if __name__ == "__main__":
	shutil.copyfile("source/bzcaip.pyc", "dist/bzcaip.pyc")
	shutil.copyfile("source/settings.pyc", "dist/settings.pyc")
