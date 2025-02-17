# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

path = 'E:\python\election-s-prediction'

a = Analysis(['app.py'],
             pathex=[path,'C:\\Windows\\System32\\downlevel'],
             binaries=[],
             datas=[
                (path + '\\static','static'),
                (path + '\\template','template'),
                (path + '\\file','file'),
                (path + '\\database.db','.'),
                (path + '\\resource','.')
                ],
             hiddenimports=['pkg_resources.py2_warn','pymysql',"pandas","pandas._libs.tslibs.np_datetime",'matplotlib','numpy','sklearn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='app')
