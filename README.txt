====================================================
BZCAIP AIP Generator v0.1.0 for BattleZone II Classic Mod.

This software is licensed under the GNU General Public License
version 3. Please refer to gpl.txt for more information.
Copyright (c) 2013 DarkDragonDX
====================================================

Table of Contents:
	I. Usage
	II. Packaging Executables
	
I. USAGE
	Using the software is easy.
	
	With Python:
		You first need to run the compile.py script so that the .pyc is placed underneath of
		dist/ where its data is:
			python compile.py
		
		Then you may run the application:
			python ./bzcaip.py <RACENAME>
	
	The executables work the same way except they do not require compile.py to be executed
	and have no dependencies on Python:
		bzcaip.exe <RACENAME>

II. Packaging Executables
	With the provided development environment, one can produce a modified version
	of the executable using PyInstaller ( http://pyinstaller.org ) and an appropriate
	version of Python ( http://www.python.org ).
	
	From the command line (Windows):
		pyi-build bzcaip.spec
		
	The bzcaip.exe will be created in the dist/ directory running the code contained in source/bzcaip.py
	at the time of creation. From this point on, the .exe is in no way dependent upon source/bzcaip.py.