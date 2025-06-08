import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import sys
from pathlib import Path
import traceback
import proglog
import contextlib

class ConversionError(Exception):
    pass

def conversion(input_path: Path, output_path: Path) -> None:
    try:
        with open(os.devnull, 'w') as devnull:
                with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
                    # Run the conversion inside the silenced context
                    with VideoFileClip(str(input_path)) as video:
                        video.write_videofile(
                            str(output_path),
                            codec="libx264",
                            audio_codec="aac" if video.audio else None
                            # Leave logger and verbose at their default, working values
                    )
    except Exception as e:
        # The exception is caught outside the redirection, so we can
        # still print the error to the now-restored console.
        tb_str = traceback.format_exc()
        print(f"An error occurred during conversion. Traceback:\n{tb_str}")
        raise ConversionError(f"MoviePy failed during conversion.")

def ppath(input_path_str: str) -> str:
    input_path = Path(input_path_str)

    if not input_path.is_file():
        raise FileNotFoundError(f"'{input_path_str}' is not a valid file.")

    if input_path.suffix.lower() == '.mp4':
        return str(input_path.resolve())

    cache_directory = Path.home() / ".ccache"
    output_filename = input_path.with_suffix(".mp4").name
    output_path = cache_directory / output_filename

    try:
        cache_directory.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise ConversionError(f"Could not create cache directory '{cache_directory}'.")

    conversion(input_path, output_path)

    return str(output_path.resolve())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("conv <path_to_video>", file=sys.stderr)
        sys.exit(1)
    try:
        final_path = ppath(sys.argv[1])
        #print(final_path)
    except (ConversionError, FileNotFoundError) as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)