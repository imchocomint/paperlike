# conv.py (Enhanced Debugging Version)

import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import sys
from pathlib import Path

def conversion(input_path: Path, output_path: Path) -> bool:
    """
    Converts a video file to MP4, with verbose debugging.
    """
    print("--- [conv.py] DEBUG: Starting conversion function...", file=sys.stderr)
    try:
        # Use a progress bar logger to see ffmpeg's activity
        with VideoFileClip(str(input_path)) as video:
            if video.audio is None:
                print("--- [conv.py] DEBUG: No audio detected. Writing video track only.", file=sys.stderr)
                video.write_videofile(str(output_path), codec="libx264", logger='bar')
            else:
                print("--- [conv.py] DEBUG: Audio detected. Writing video and audio.", file=sys.stderr)
                video.write_videofile(str(output_path), codec="libx264", audio_codec="aac", logger='bar')
        print("--- [conv.py] DEBUG: MoviePy write_videofile completed successfully.", file=sys.stderr)
        return True
    except Exception as e:
        print("--- [conv.py] FATAL: An exception occurred inside the conversion function! ---", file=sys.stderr)
        print(f"--- [conv.py] The specific error is: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc() # Print the full error traceback
        return False

def ppath(input_path_str: str):
    """
    Processes the file path and calls the conversion function.
    """
    print(f"--- [conv.py] DEBUG: ppath received input: {input_path_str}", file=sys.stderr)
    input_path = Path(input_path_str)

    if not input_path.is_file():
        print(f"--- [conv.py] FATAL: Input path '{input_path_str}' is not a valid file.", file=sys.stderr)
        sys.exit(1)
    if input_path.suffix.lower() == '.mp4':
        print(str(input_path.resolve()))
        return

    cache_directory = Path.home() / ".ccache"
    output_filename = input_path.with_suffix(".mp4").name
    output_path = cache_directory / output_filename
    
    try:
        cache_directory.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"--- [conv.py] FATAL: Could not create cache directory '{cache_directory}'. Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"--- [conv.py] DEBUG: Starting conversion for '{input_path}'...", file=sys.stderr)
    if conversion(input_path, output_path):
        print(str(output_path.resolve())) # This prints the final path to main.py
    else:
        print("--- [conv.py] DEBUG: conversion() returned False. Exiting with error code 1.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python conv.py <path_to_video>", file=sys.stderr)
        sys.exit(1)
    ppath(sys.argv[1])