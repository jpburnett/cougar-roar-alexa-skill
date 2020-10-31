# cougar-roar-alexa-skill
An Alexa Skill that makes Alexa play a cougar roar sound.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://raw.githubusercontent.com/jpburnett/cougar-roar-alexa-skill/master/LICENSE)
[![Python 3.8.5](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)

## Motivation
This skill came about because Alexa could roar like a lion but not a cougar...
Also because my schools mascott is a cougar, I figured why not.

First skill I'm writing in python, so brace your self.

## Audio Formatting
This skill uses audio play back and therefore needs to be formatted correctly for an alexa friendly format.

What I did was use the following command:
`ffmpeg -i <input-file> -ac 2 -codec:a libmp3lame -b:a 48k -ar 16000 <output-file.mp3>`
