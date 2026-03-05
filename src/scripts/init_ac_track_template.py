import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import subprocess
import json
from pathlib import Path
from config import PROJECT_SAVE_DIRECTORY
from scripts.init_blender_file import create_and_save

GITATTRIBUTES = """\
*.kn5 filter=lfs diff=lfs merge=lfs -text
*.ai filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.blend filter=lfs diff=lfs merge=lfs -text
"""

GITIGNORE = """\
# macOS
.DS_Store
.AppleDouble
.LSOverride
._*
.Spotlight-V100
.Trashes
.fseventsd
.VolumeIcon.icns

# Blender backups
*.blend1
*.blend2

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/

# Editors
.vscode/
.idea/
"""

AUDIO_SOURCES_INI = """\
[REVERB_0]
ENABLED=0
NODE=AC_REVERB_TUNNEL
MINDISTANCE=12
MAXDISTANCE=35
PRESET=SEWERPIPE
"""

CAMERAS_INI = """\
[HEADER]
VERSION=3
CAMERA_COUNT=1
SET_NAME=TV 1

[CAMERA_0]
NAME=cam01
POSITION=0,5,0
FORWARD=0,0,-1
UP=0,1,0
MIN_FOV=3
MAX_FOV=6
IN_POINT=0
OUT_POINT=1
SHADOW_SPLIT0=1.8
SHADOW_SPLIT1=20
SHADOW_SPLIT2=180
NEAR_PLANE=0.1
FAR_PLANE=35000
MIN_EXPOSURE=0.35
MAX_EXPOSURE=0.55
DOF_FACTOR=2.5
DOF_RANGE=350
DOF_FOCUS=50
DOF_MANUAL=0
SPLINE=
SPLINE_ROTATION=0
FOV_GAMMA=1
SPLINE_ANIMATION_LENGTH=15
IS_FIXED=0
"""

CREW_INI = """\
[HEADER]
SIDE=-1\t\t; 1 = left , -1 = right
"""

GROOVE_INI = """\
[HEADER]
GROOVES_NUMBER=4

[GROOVE_0]
NAME=groove1a
MIN=0.7
MAX=1.1
MULT=5

[GROOVE_1]
NAME=groove1b
MIN=0.7
MAX=1.1
MULT=5

[GROOVE_2]
NAME=groove2a
MIN=0.6
MAX=1
MULT=8

[GROOVE_3]
NAME=groove2b
MIN=0.6
MAX=1
MULT=8
"""

LIGHTING_INI = """\
[LIGHTING]
SUN_PITCH_ANGLE=50
SUN_HEADING_ANGLE=250
AMBIENT_COLOR=127,127,127
SUN_COLOR=204,197,176
"""

SURFACES_INI = """\
[SURFACE_0]
KEY=TARMAC
FRICTION=0.99
DAMPING=0
WAV=
WAV_PITCH=0
FF_EFFECT=NULL
DIRT_ADDITIVE=0
IS_VALID_TRACK=1
BLACK_FLAG_TIME=0
SIN_HEIGHT=0
SIN_LENGTH=0
IS_PITLANE=0
VIBRATION_GAIN=0
VIBRATION_LENGTH=0

[SURFACE_1]
KEY=KERB
FRICTION=0.94
DAMPING=0
WAV=kerb.wav
WAV_PITCH=1.3
FF_EFFECT=1
DIRT_ADDITIVE=0
IS_VALID_TRACK=1
BLACK_FLAG_TIME=0
SIN_HEIGHT=0
SIN_LENGTH=0
IS_PITLANE=0
VIBRATION_GAIN=0.5
VIBRATION_LENGTH=1.5

[SURFACE_2]
KEY=PITLANE
FRICTION=0.95
DAMPING=0
WAV=
WAV_PITCH=0
FF_EFFECT=NULL
DIRT_ADDITIVE=0
IS_VALID_TRACK=1
BLACK_FLAG_TIME=0
SIN_HEIGHT=0
SIN_LENGTH=0
IS_PITLANE=1
VIBRATION_GAIN=0
VIBRATION_LENGTH=0

[SURFACE_3]
KEY=SAND
FRICTION=0.8
DAMPING=0.1
WAV=sand.wav
WAV_PITCH=0
FF_EFFECT=0
DIRT_ADDITIVE=1
IS_VALID_TRACK=0
BLACK_FLAG_TIME=0
SIN_HEIGHT=0.01
SIN_LENGTH=0.1
IS_PITLANE=0
VIBRATION_GAIN=0.2
VIBRATION_LENGTH=0.3

[SURFACE_4]
KEY=OFFTRACK
FRICTION=0.95
DAMPING=0
WAV=
WAV_PITCH=0
FF_EFFECT=NULL
DIRT_ADDITIVE=0
IS_VALID_TRACK=0
BLACK_FLAG_TIME=0
SIN_HEIGHT=0
SIN_LENGTH=0
IS_PITLANE=0
VIBRATION_GAIN=0
VIBRATION_LENGTH=0

[SURFACE_5]
KEY=CONCRETE
FRICTION=0.94
DAMPING=0
WAV=extraturf.wav
WAV_PITCH=0
FF_EFFECT=NULL
DIRT_ADDITIVE=0
IS_VALID_TRACK=1
BLACK_FLAG_TIME=0
SIN_HEIGHT=0
SIN_LENGTH=0
IS_PITLANE=0
VIBRATION_GAIN=0
VIBRATION_LENGTH=0
"""


def create_directory_structure(track_dir: Path, track_name: str):
    """
    Create the AC track directory structure with all required subdirectories
    and empty placeholder files.

    Args:
        - track_dir: Path - root directory for the track (PROJECT_SAVE_DIRECTORY/trackname)
        - track_name: str - the track name, used for the .kn5 placeholder filename
    """
    for subdir in ['__blender', 'ai', 'data', 'ui']:
        (track_dir / subdir).mkdir(parents=True, exist_ok=True)

    placeholder_files = [
        track_dir / f'{track_name}.kn5',
        track_dir / 'ai' / 'fast_lane.ai',
        track_dir / 'ai' / 'pit_lane.ai',
        track_dir / 'ui' / 'outline.png',
        track_dir / 'ui' / 'preview.png',
    ]
    for f in placeholder_files:
        f.touch()

    print(f'✓ Created directory structure at: {track_dir}')


def write_template_files(track_dir: Path, track_name: str):
    """
    Write all template .ini, .json, and .gitattributes files.

    Args:
        - track_dir: Path - root directory for the track
        - track_name: str - used to populate ui_track.json name field
    """
    (track_dir / '.gitattributes').write_text(GITATTRIBUTES)
    (track_dir / '.gitignore').write_text(GITIGNORE)

    ini_files = {
        'data/audio_sources.ini': AUDIO_SOURCES_INI,
        'data/cameras.ini': CAMERAS_INI,
        'data/crew.ini': CREW_INI,
        'data/groove.ini': GROOVE_INI,
        'data/lighting.ini': LIGHTING_INI,
        'data/surfaces.ini': SURFACES_INI,
    }
    for rel_path, content in ini_files.items():
        (track_dir / rel_path).write_text(content)

    ui_track = {
        'name': track_name,
        'description': '',
        'tags': ['circuit', 'mod'],
        'geotags': ['lat', 'lon'],
        'country': '',
        'city': '',
        'length': '',
        'width': '',
        'pitboxes': '0',
        'run': 'clockwise',
    }
    (track_dir / 'ui' / 'ui_track.json').write_text(
        json.dumps(ui_track, indent='\t') + '\n'
    )

    print('✓ Wrote template files')


def create_blend_file(track_dir: Path, track_name: str):
    """
    Create and save the initial .blend file in the __blender directory.

    Args:
        - track_dir: Path - root directory for the track
        - track_name: str - used as the .blend filename
    """
    create_and_save(str(track_dir / '__blender'), track_name)


def init_git_lfs(track_dir: Path, track_name: str):
    """
    Initialise a git repository with LFS tracking and make an initial commit.

    Args:
        - track_dir: Path - root directory for the track (will become the git root)
        - track_name: str - used in the initial commit message
    """
    cwd = str(track_dir)
    subprocess.run(['git', 'init'], cwd=cwd, check=True)
    subprocess.run(['git', 'lfs', 'install'], cwd=cwd, check=True)
    subprocess.run(['git', 'add', '.'], cwd=cwd, check=True)
    subprocess.run(
        ['git', 'commit', '-m', f'Initial track template: {track_name}'],
        cwd=cwd,
        check=True,
    )
    print('✓ Initialised git repo with LFS and made initial commit')


def main(track_name: str):
    track_dir = Path(PROJECT_SAVE_DIRECTORY) / track_name

    if track_dir.exists():
        print(f'Directory already exists: {track_dir}')
        return

    create_directory_structure(track_dir, track_name)
    write_template_files(track_dir, track_name)
    create_blend_file(track_dir, track_name)
    init_git_lfs(track_dir, track_name)

    print(f'✓ Track template ready: {track_dir}')


if __name__ == '__main__':
    main('my_test_track')
