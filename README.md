
# JumpcutterV3GUI
Automatically cuts silent sections of videos - Originally inspired by carykh.

Carykh's video: https://www.youtube.com/watch?v=DQ8orIurGxw

Carykh's program: https://github.com/carykh/jumpcutter

# Windows Setup (GUI)
[JumpCutter_AIO.exe](https://github.com/seaty6/jumpcutterV2/releases/latest/download/JumpCutter_AIO.exe)

The above is simply JumpCutter_AIO.py compiled with pyinstaller - it should work on Windows without having to install Python, but you will have to install ffmpeg. The easiest way to do this is to install chocolatey and let it do the work for you.
From an administrative command prompt:

```@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command " [System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"```

Close, then reopen the Administrative command prompt, and run:

`choco install ffmpeg`

And you're done! You can now run the executable. You may have to install a codec pack depending on the file format you're trying to convert. CCCP and K-lite Basic have been tested and are confirmed working - you can install CCCP from [Ninite]([https://ninite.com/cccp/](https://ninite.com/cccp/)), the official [CCCP website]([http://www.cccp-project.net/](http://www.cccp-project.net/)), or  with the following command in an Administrative Command Prompt:

```choco install cccp```

# Windows Setup (CLI)
 [fast_video.exe](https://github.com/seaty6/jumpcutterV2/releases/latest/download/fast_video.exe)

Everything is the same except for the file - get this one instead, and run ```fast_video.exe -h``` to get a list of all the parameters. 



# Python Setup (GUI)
1. Download ```arraywav.py``` and ```jumpcutterGUI_AIO.py``` to the same folder
2. Ensure that a 64bit version of Python is installed and in use ([Python download](https://www.python.org/downloads/))

    > Note: You can check this by running `python -c "import struct; print(struct.calcsize('P')*8)"`. Should return `64`.

3. Using pip, install the modules in [requirements.txt](https://github.com/seaty6/jumpcutterV2/releases/latest/download/requirements.txt)
4. Install ffmpeg and add it to PATH ([ffmpeg download](https://www.ffmpeg.org/download.html) and a [Guide](https://windowsloop.com/install-ffmpeg-windows-10/))
5. Run ```python jumpcutterGUI_AIO.py```.
6. Done.


# Python Setup (CLI)
1. Download ```arraywav.py``` and ```fast_video.py``` to the same folder
2. Ensure that a 64bit version of Python is installed and in use ([Python download](https://www.python.org/downloads/))

    > Note: You can check this by running `python -c "import struct; print(struct.calcsize('P')*8)"`. Should return `64`.

3. Using pip, install the modules in [requirements.txt](https://github.com/seaty6/jumpcutterV2/releases/latest/download/requirements.txt)
4. Install ffmpeg and add it to PATH ([ffmpeg download](https://www.ffmpeg.org/download.html) and a [Guide](https://windowsloop.com/install-ffmpeg-windows-10/))
5. Refer to the [Usage Section](#usage).
6. Done.


# Differences
1. Can no longer specify: sounded_speed, frame_rate, and frame_quality
2. Can't download YouTube videos
3. Doesn't take up a large amount of space by splitting up each frame
4. Goes much faster

# Usage
Windows (GUI):
run ```JumpCutterGui_AIO.exe```

Windows (CLI):
`fast_video.exe {video file name} --silentSpeed {float} --silentThreshold {float} --floatMargin {float}`

Python (GUI):
run ```JumpCutterGui_AIO.py```

Python (CLI):
`python3 fast_video.py {video file name} --silentSpeed {float} --silentThreshold {float} --floatMargin {float}`

Using shorts:
`fast_video.exe {video file name} -s {float} -t {float} -m {float}`

> Note: On Linux and Windows, `python3` may not work. Use `python` instead. Alternatively, you could use the executable if on Windows, in the releases tab.

## Argument Values
| Argument | Default Value | Why adjust? |
| -------- | ------------- | ---------- |
| `silentSpeed` | 99999 | Lower for less "jump" |
| `silentThreshold` | 0.04 | Vary between 0-1 for less/more "silence" (Higher values mean more of the video is cut out) |
| `frameMargin` | 1 | Increase by whole numbers to require larger pauses before cutting out a section |

# Heads up
Based on Python3
