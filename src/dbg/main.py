# main.py (Corrected)

import argparse
import subprocess
import sys
import os

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
        print(f"An error occurred while starting wallpaper: {e}", file=sys.stderr)
        sys.exit(1)

def set_video_wallpaper_x11(video_file, extarg=None):
    command = [ 'mpv', '--wid=0', '--loop=inf', '--no-audio', '--no-stop-screensaver', '--player-operation-mode=pseudo-gui' ]
    if extarg: command.extend(extarg.split())
    command.append(video_file)
    try:
        process = subprocess.Popen(command)
    except Exception as e:
        print(f"An error occurred while starting wallpaper: {e}", file=sys.stderr)
        sys.exit(1)

def get_display_server():
    xdg_session_type = os.environ.get("XDG_SESSION_TYPE")
    if xdg_session_type:
        if xdg_session_type.lower() == "wayland": return "Wayland"
        elif xdg_session_type.lower() == "x11": return "X11"
    if "WAYLAND_DISPLAY" in os.environ: return "Wayland"
    if "DISPLAY" in os.environ: return "X11"
    return "Unknown"

def convert_and_get_path(video_file_path: str) -> str:
    formats_to_convert = (".gif",".mov", ".avi", ".wmv", ".flv", ".mkv", ".webm", ".avchd", ".mpeg", ".mpg", ".vob", ".3gp", ".m4v", ".ts", ".rmvb", ".asf", ".f4v", ".ogv")
    if video_file_path.lower().endswith(formats_to_convert):
        print(f"--- [main.py] DEBUG: Converting '{os.path.basename(video_file_path)}' to MP4...", file=sys.stderr)
        try:
            process = subprocess.run(
                [sys.executable, "-c", f"from conv import ppath; ppath('{video_file_path}')"],
                capture_output=True, text=True, check=True, encoding='utf-8'
            )
            
            # --- START OF FIX ---
            # The output from the script contains multiple lines from moviepy.
            # We only want the last line, which is the actual file path.
            all_lines = process.stdout.strip().splitlines()
            if not all_lines:
                print("--- [main.py] FATAL: Conversion script produced no output.", file=sys.stderr)
                sys.exit(1)
            
            new_path = all_lines[-1] # Get the very last line of the output
            # --- END OF FIX ---

            if not os.path.exists(new_path):
                print("--- [main.py] FATAL: The path received from conversion script is not valid.", file=sys.stderr)
                print(f"--- [main.py] Received path: '{new_path}'", file=sys.stderr)
                print(f"--- [main.py] Full Stdout from conv.py: ---\n{process.stdout}", file=sys.stderr)
                sys.exit(1)

            print(f"--- [main.py] DEBUG: Conversion complete. Using cached file: {new_path}", file=sys.stderr)
            return new_path
        except subprocess.CalledProcessError as e:
            print("--- [main.py] FATAL: The conversion script (conv.py) exited with an error. ---", file=sys.stderr)
            print(f"--- [main.py] Exit Code: {e.returncode}", file=sys.stderr)
            print(f"--- [main.py] ---- Standard Error from conv.py ----\n{e.stderr}", file=sys.stderr)
            sys.exit(1)
    else:
        return video_file_path

def main():
    parser = argparse.ArgumentParser(description="A Python script to set a video wallpaper on Linux using mpv/mpvpaper.")
    parser.add_argument("video_file", help="The path to the video file you want to set as the wallpaper.")
    parser.add_argument("extarg", nargs='?', default=None, help="Optional external arguments for mpv. Enclose in quotes if multiple.")
    args = parser.parse_args()
    
    if not args.video_file or not os.path.exists(args.video_file):
        print(f"Error: Video file '{args.video_file}' not found or not specified.", file=sys.stderr)
        sys.exit(1)

    session = get_display_server()
    usable_video_path = convert_and_get_path(args.video_file)

    if session == "Unknown":
        print("Error: Could not determine display server type.", file=sys.stderr)
        sys.exit(1)
    elif session == "Wayland":
        set_video_wallpaper_wl(usable_video_path, args.extarg)
    else:
        set_video_wallpaper_x11(usable_video_path, args.extarg)

if __name__ == "__main__":
    main()