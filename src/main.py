import argparse
import subprocess
import sys
import os
#import moviepy.editor as mp

def set_video_wallpaper_wl(video_file):
    command = [
        'mpvpaper',
        'ALL',
        '-fs',
        '-l',
        'background',
        video_file
   ]
    try:
        # Using subprocess.run to execute the command.
        # This will block the script until you close mpv (e.g., by killing it).
        # For a true background process, you would use subprocess.Popen.
        process = subprocess.Popen(command)
        # You can optionally wait for it to finish or just let it run
        # process.wait() 
    except FileNotFoundError:
        print("Error: 'mpv' and/or mpvpaper can't be used.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def set_video_wallpaper_x11(video_file):
    command = [
        'mpv',
        '--wid=0',
        '--loop=inf',
        '--no-audio',      
        '--no-stop-screensaver',
        '--player-operation-mode=pseudo-gui', 
        video_file
    ]

    try:
        # Using subprocess.run to execute the command.
        # This will block the script until you close mpv (e.g., by killing it).
        # For a true background process, you would use subprocess.Popen.
        process = subprocess.Popen(command)
        # You can optionally wait for it to finish or just let it run
        # process.wait() 
    except FileNotFoundError:
        print("Error: 'mpv' can't be used.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def get_display_server():
    xdg_session_type = os.environ.get("XDG_SESSION_TYPE")
    if xdg_session_type:
        return xdg_session_type.capitalize()

    if "WAYLAND_DISPLAY" in os.environ:
        return "Wayland"

    if "DISPLAY" in os.environ:
        return "X11"

    return "Unknown"

def main():
    parser = argparse.ArgumentParser(
        description="A Python script to set a video wallpaper on Linux using mpv/mpvpaper."
    )
    parser.add_argument(
        "video_file",
        help="The path to the video file you want to set as the wallpaper."
    )
    session = get_display_server()
    if session == "Unknown":
        sys.exit(1)
    elif session == "Wayland":
        args = parser.parse_args()
        set_video_wallpaper_wl(args.video_file)
    else:
        args = parser.parse_args()
        set_video_wallpaper_x11(args.video_file)

if __name__ == "__main__":
    main()
