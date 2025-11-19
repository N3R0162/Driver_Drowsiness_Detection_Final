# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['source/launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('source/*.py', 'source'),
        ('source/audio/*.mp3', 'source/audio'),
        ('source/weights', 'source/weights'),
        ('FaceBoxesV2', 'FaceBoxesV2'),
        ('experiments', 'experiments'),
        ('data', 'data'),
        ('snapshots', 'snapshots'),
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'torch',
        'cv2',
        'pygame',
        'pandas',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DrowsinessDetection',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon='icon.ico'  # Add your icon file
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DrowsinessDetection'
)