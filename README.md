# Paperlike, dynamic wallpaper for Linux
Thanks weebp

This is a rewrite of weebp in Python, which aim to port the software to Linux (since the repo owner is better at Python)

This was written for like 2 hours with the help of Gemini 2.5 Pro. Of course, I'm still the main contributer though.

# Roadmap
[x] Works on Wayland

[ ] Works on X11 (untested)

[ ] Works on KDE Plasma (fuck that shit)

[ ] Have a convert function for any other file type --> .mp4

[ ] Load playlist/anything from the Internet


# Installation
Since no binary package is available, you may want to use the script with Python:

`
python3 main.py /your/video/file/gohere/
`

Unless you want to shit yourself out of your ass, please install python-is-python3

`
python main.py /your/video/file/gohere/
`

See? Much better

There is a demo video on the /src/ directory. You can try with it.

And for dependencies (ha! caught the lazy reader): mpv, mpvpaper

And to compile mpvpaper: libmpv-dev (apt), mpv-libs-devel (dnf). Arch users need not to worry about this

# Issues
Currently our only issue is with KDE Plasma. The software is untested elsewhere.
