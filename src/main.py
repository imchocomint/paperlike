import argparse
import subprocess
import sys
import os
#import moviepy.editor as mp

def set_video_wallpaper_wl(video_file, extarg=None):
    command = [
        'mpvpaper',
        'ALL',
        '-fs',
        '-l',
        'background',
        '-o'
    ]
    mpv_options_list = [
        '--no-audio',
        '--loop=inf',
        '--no-stop-screensaver',
        '--player-operation-mode=pseudo-gui'
    ]

    if extarg:
        mpv_options_list.extend(extarg.split())

    mpv_options_string = " ".join(mpv_options_list)
    command.append(mpv_options_string)

    command.append(video_file)


    try:
        process = subprocess.Popen(command)
        # process.wait() 
    except FileNotFoundError:
        print("Error: 'mpv' and/or mpvpaper can't be used.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def set_video_wallpaper_x11(video_file, extarg=None):
    command = [
        'mpv',
        '--wid=0',
        '--loop=inf',
        '--no-audio',      
        '--no-stop-screensaver',
        '--player-operation-mode=pseudo-gui',
        video_file
    ]
    if extarg:
        command.extend(extarg.split())
    
    command.append(video_file)

    try:
        process = subprocess.Popen(command)
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
        if xdg_session_type.lower() == "wayland": # Case-insensitive compare
            return "Wayland"
        elif xdg_session_type.lower() == "x11": # Case-insensitive compare
            return "X11"
        else:
            return "Unknown"


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
    parser.add_argument(
        "extarg",
        nargs='?',
        default=None,
        help="Optional external arguments for mpv/mpvpaper (see mpv wiki). Enclose in quotes if multiple."
    )
    
    args = parser.parse_args()
    session = get_display_server()

    if not args.video_file or not os.path.exists(args.video_file):
        print(f"Error: Video file '{args.video_file}' not found or not specified.", file=sys.stderr)
        sys.exit(1)

    if session == "Unknown":
        sys.exit(1)
    elif session == "Wayland":
        set_video_wallpaper_wl(args.video_file, args.extarg)
    else:
        set_video_wallpaper_x11(args.video_file, args.extarg)


if __name__ == "__main__":
    main()
