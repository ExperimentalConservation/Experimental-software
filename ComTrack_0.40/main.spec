# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[
                'sklearn.utils._typedefs'
             ],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [
    ('./images/icons/export.png', './images/icons/export.png', 'DATA'),
    ('./images/icons/load.png', './images/icons/load.png', 'DATA'),
    ('./images/icons/play.png', './images/icons/play.png', 'DATA'),
    ('./images/icons/reset.png', './images/icons/reset.png', 'DATA'),
    ('./images/icons/stop.png', './images/icons/stop.png', 'DATA'),
    ('./images/icons/logo256x256.png', './images/icons/logo256x256.png', 'DATA'),
    ('./images/home/home_1.png', './images/home/home_1.png', 'DATA'),
    ('./images/home/home_2.png', './images/home/home_2.png', 'DATA'),
    ('./images/home/home_3.png', './images/home/home_3.png', 'DATA'),
    ('./images/home/home_4.png', './images/home/home_4.png', 'DATA'),
    ('./images/icons/logo256x256.ico', './images/icons/logo256x256.ico', 'DATA')
]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='ComTrack 0.40',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='./images/icons/logo256x256.ico',
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='ComTrack 0.40')