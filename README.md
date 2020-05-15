# jumpcutterV2
Automatically cuts silent sections of videos - Originally inspired by carykh.

Carykh's video: https://www.youtube.com/watch?v=DQ8orIurGxw

Carykh's program: https://github.com/carykh/jumpcutter

# Windows Setup
[fast_video.exe](https://github.com/seaty6/jumpcutterV2/releases/latest/download/fast_video.exe)

The above is simply the python file compiled with pyinstaller - it should work on Windows without having to install Python, but you will have to install ffmpeg. The easiest way to do this is to install chocolatey and let it do the work for you.
From an administrative command prompt:

```@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command " [System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"```

Close, then reopen the command prompt, and run:

`choco install ffmpeg`

And you're done! You can now run the executable.

# Python Setup
[fast_video.py](https://github.com/seaty6/jumpcutterV2/releases/latest/download/fast_video.py)
[arrayWav.py](https://github.com/seaty6/jumpcutterV2/releases/latest/download/arrayWav.py)

1. Download both the above files to the same folder
2. Ensure that a 64bit version of Python is installed and in use ([Python download](https://www.python.org/downloads/))

    > Note: You can check this by running `python -c "import struct; print(struct.calcsize('P')*8)"`. Should return `64`.

3. Using pip3, install the modules in [requirements.txt](https://github.com/seaty6/jumpcutterV2/releases/latest/download/requirements.txt)
4. Install ffmpeg and add it to PATH \([ffmpeg download] (https://www.ffmpeg.org/download.html) and a [Guide](https://windowsloop.com/install-ffmpeg-windows-10/)\)
5. Done

# Differences
1. Can no longer specify: sounded_speed, frame_rate, and frame_quality
2. Can't download youtube videos
3. Doesn't take up a large amount of space by splitting up each frame
4. Goes much faster

# Usage
Windows:
`fast_video.exe {video file name} --silentSpeed {float} --silentThreshold {float} --floatMargin {float}`

Python:
`python3 fast_video.py {video file name} --silentSpeed {float} --silentThreshold {float} --floatMargin {float}`

Using shorts:
`fast_video.exe {video file name} -s {float} -t {float} -m {float}`

> Note: On Linux and Windows, `python3` doesn't work. Use `python` instead. Alternatively, you could use the executable if on Windows, in the releases tab.

## Argument Values
| Argument | Default Value | Why adjust? |
| -------- | ------------- | ---------- |
| `silentSpeed` | 99999 | Lower for less "jump" |
| `silentThreshold` | 0.04 | Vary between 0-1 for less/more "silence" |
| `frameMargin` | 1 | Increase by whole numbers for more buffer around jumps |

# Heads up
Based on Python3

# Credits:
Thanks to [gusals3587](https://github.com/gusals3587/jumpcutterV2) for reworking the code to be much more optimized

Thanks to [WyattBlue](https://github.com/WyattBlue/jumpcutterV2) for adding back the all but the frame_margin parameter
