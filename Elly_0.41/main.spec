# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas += [
    ('./font/Futura/Futura Heavy font.ttf', './font/Futura/Futura Heavy font.ttf', 'DATA'),
    ('./images/icons/connection.png', './images/icons/connection.png', 'DATA'),
    ('./images/icons/camera.png', './images/icons/camera.png', 'DATA'),
    ('./images/icons/gantry.png', './images/icons/gantry.png', 'DATA'),
    ('./images/icons/arduinoringlight.png', './images/icons/arduinoringlight.png', 'DATA'),
    ('./images/icons/program.png', './images/icons/program.png', 'DATA'),
    ('./images/icons/logo_500x500.png', './images/icons/logo_500x500.png', 'DATA'),
    ('./images/icons/logo_500x500.ico', './images/icons/logo_500x500.ico', 'DATA')   
]

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='Elly 0.41',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='./images/icons/logo_500x500.ico',
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Elly 0.41')
