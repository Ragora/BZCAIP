# -*- mode: python -*-
import os
import sys
a = Analysis(['source/bzcaip.py'],
             pathex=[os.getcwd()],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)


out = 'bzcaip'
if ('linux' not in sys.platform):
	out += '.exe'

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=out,
	  icon='dist/bzcaip.ico',
          debug=False,
          strip=None,
          upx=True,
          console=True )
