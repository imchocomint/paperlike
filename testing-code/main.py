from conv import ppath, ConversionError
import argparse
import subprocess
import sys
import os
import shutil

def set_video_wallpaper_wl(video_file, extarg=None):
    command = [ 'mpvpaper', 'ALL', '-l', 'background', '-o' ]
    mpv_options_list = [ '--no-audio', '--loop=inf', '--fs', '--no-stop-screensaver', '--player-operation-mode=pseudo-gui' ]
    if extarg: mpv_options_list.extend(extarg.split())
    mpv_options_string = " ".join(mpv_options_list)
    command.append(mpv_options_string)
    command.append(video_file)
    try:
        process = subprocess.Popen(command)
    except Exception as e:
        print(f"Wallpaper did not start successfully: {e}", file=sys.stderr)
        sys.exit(1)

def set_video_wallpaper_x11(video_file, extarg=None):
    command = [ 'mpv', '--wid=0', '--loop=inf', '--no-audio', '--no-stop-screensaver', '--player-operation-mode=pseudo-gui' ]
    if extarg: command.extend(extarg.split())
    command.append(video_file)
    try:
        process = subprocess.Popen(command)
    except Exception as e:
        print(f"Wallpaper did not start successfully: {e}", file=sys.stderr)
        sys.exit(1)

def get_display_server():
    xdg_session_type = os.environ.get("XDG_SESSION_TYPE")
    if xdg_session_type:
        if xdg_session_type.lower() == "wayland": 
            return "Wayland"
        elif xdg_session_type.lower() == "x11": 
            return "X11"
    if "WAYLAND_DISPLAY" in os.environ: 
        return "Wayland"
    if "DISPLAY" in os.environ: 
        return "X11"
    return "Unknown"

def convert_and_get_path(video_file_path: str) -> str:
    formats_to_convert = (".gif",".mov", ".avi", ".wmv", ".flv", ".mkv", ".webm", ".avchd", ".mpeg", ".mpg", ".vob", ".3gp", ".m4v", ".ts", ".rmvb", ".asf", ".f4v", ".ogv")
    if video_file_path.lower().endswith(formats_to_convert):
        try:
            # Direct function call, wrapped in try/except
            new_path = ppath(video_file_path)
            return new_path
        except ConversionError as e:
            # The exception raised by conv.py is caught here
            print(f"FATAL: The conversion failed.", file=sys.stderr)
            print(f"Reason: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        return video_file_path

def main():
    dependencies = ['ffmpeg', 'mpv', 'mpvpaper']
    missing_deps = [dep for dep in dependencies if not shutil.which(dep)]

    if missing_deps:
        print("Error: Missing required system dependencies.", file=sys.stderr)
        for dep in missing_deps:
            print(f"  - '{dep}' was not found in your system's PATH.", file=sys.stderr)
        sys.exit(1)
    parser = argparse.ArgumentParser(description="Application to set a video wallpaper on Linux using mpv/mpvpaper.")
    parser.add_argument("video_file", help="The path to the video file you want to set as the wallpaper.")
    parser.add_argument("extarg", nargs='?', default=None, help="Optional external arguments for mpv. Enclose in quotes if multiple.")
    args = parser.parse_args()
    
    if not args.video_file or not os.path.exists(args.video_file):
        print(f"Error: Video file '{args.video_file}' not found or not specified.", file=sys.stderr)
        sys.exit(1)

    session = get_display_server()
    usable_video_path = convert_and_get_path(args.video_file)

    if session == "Unknown":
        sys.exit(1)
    elif session == "Wayland":
        set_video_wallpaper_wl(usable_video_path, args.extarg)
    else:
        set_video_wallpaper_x11(usable_video_path, args.extarg)

if __name__ == "__main__":
    main()