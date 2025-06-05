# Paperlike, dynamic wallpaper for Linux
Thanks weebp

This is a rewrite of weebp in Python, which aim to port the software to Linux (since the repo owner is better at Python).

This rewrite is only compatitable with .mp4 files. No other format is supported, although a conversion function is yet to be implemented.

This was written for like 2 hours with the help of Gemini 2.5 Pro. Of course, I'm still the main contributer though.

# Roadmap
- [x] Works on Wayland

- [x] External arguments to mpv

- [ ] Works on X11 (untested)

- [ ] Works on KDE Plasma (fuck that shit)

- [ ] Have a convert function for any other file type --> .mp4 (soon!)

- [ ] Load playlist/anything from the Internet


# Installation
Download from Release.

Launch:

`
./main <your video file>
`
Same applies to the source Python file

The software defaults to rendering by CPU. External arguments is needed to use the GPU (see below)

There is a demo video on the /src/ directory. You can try with it. If your PC is capable enough, use the 4K video.

And for dependencies (ha! caught the lazy reader): mpv, mpvpaper

And to compile mpvpaper: libmpv-dev (apt), mpv-libs-devel (dnf). Arch users need not to worry about this

# Launch arguments
`
main.py <file> "(your mpv arguments go here)"
`

mpv arguments are available at [their wiki](https://mpv.io/manual/stable/). Some crucial arguments are added in the source code.

Here is how you can force to render by GPU (I'm defaulting to VAAPI protocol):

`
python main.py main.mp4 "--vo=gpu --hwdec=vaapi"
`
# Issues
Currently our only issue is with KDE Plasma.
