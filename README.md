# Paperlike, dynamic wallpaper for Linux
Thanks weebp

This is a rewrite of weebp in Python, which aim to port the software to Linux (since the repo owner is better at Python).

This rewrite is only compatitable with .mp4 files. No other format is supported, and a convert function is available.

This was written with the help of AI. Of course, I'm still the main contributer though.

# Roadmap
- [x] Works on Wayland (Hyprland; other untested)
- [x] Works on X11 (i3wm; others untested)
- [x] External arguments to mpv
- [x] Have a convert function for any other file type --> .mp4
- [ ] Load playlist/anything from the Internet
- [ ] Works on KDE Plasma (fuck that shit)

# Installation & Usage (stable)
Dependencies: mpv, mpvpaper, ffmpeg

To compile mpvpaper: libmpv-dev (apt), mpv-libs-devel (dnf). Arch users need not to worry about this

`
wget https://github.com/imchocomint/paperlike/releases/download/dotone/install.sh
`

`
sudo ./install.sh
`

## Launch

`
paperlike <your video file>
`

Same applies to the source Python file

The software defaults to rendering by CPU. External arguments is needed to use the GPU (see below).

There are demo files on the /demo-files/ directory. You can try them.

## Launch arguments
`
paperlike <file> "(your mpv arguments go here)"
`

mpv arguments are available at [their wiki](https://mpv.io/manual/stable/). Some crucial arguments are added in the source code.

Here is how you can force to render by GPU (I'm defaulting to VAAPI protocol):

`
paperlike main.mp4 "--vo=gpu --hwdec=vaapi"
`
# Install (development/debugging)
Currently no debugging version is active/live/available. The software will be in this form for a while.

For extended development, clone the repository. Install proglog and moviepy.

# Issues
Currently our only issue is with KDE Plasma.
