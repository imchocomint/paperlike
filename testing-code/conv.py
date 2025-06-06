import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import sys
from pathlib import Path
import traceback


class ConversionError(Exception):
    pass

def conversion(input_path: Path, output_path: Path) -> None:
    try:
        with VideoFileClip(str(input_path)) as video:
            video.write_videofile(
                str(output_path),
                codec="libx264",
                audio_codec="aac" if video.audio else None,
                logger='bar'
            )
    except Exception as e:
        tb_str = traceback.format_exc()
        raise ConversionError(f"MoviePy failed during conversion.\nError: {e}\nTraceback:\n{tb_str}")

def ppath(input_path_str: str) -> str:
    input_path = Path(input_path_str)

    if not input_path.is_file():
        raise FileNotFoundError(f"Input path '{input_path_str}' is not a valid file.")

    if input_path.suffix.lower() == '.mp4':
        return str(input_path.resolve())

    cache_directory = Path.home() / ".ccache"
    output_filename = input_path.with_suffix(".mp4").name
    output_path = cache_directory / output_filename

    try:
        cache_directory.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise ConversionError(f"Could not create cache directory '{cache_directory}'. Error: {e}")

    conversion(input_path, output_path)

    return str(output_path.resolve())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("conv <path_to_video>", file=sys.stderr)
        sys.exit(1)
    try:
        final_path = ppath(sys.argv[1])
        print(final_path)
    except (ConversionError, FileNotFoundError) as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)