# He Huan Song Syue Lodge Booker

This is a booker bot that helps you fill in information when trying to reserve for a spot in the lodge.

:::info
:bulb: The project is far from finished and currently only supports a semi-automated process. **YOU STILL HAVE TO SELECT YOUR ROOM TYPE AND PRESS CONFIRM IN THE END**.
:::

:::warning
:alarm: The Tesseract configuration has a 20% chane of misguessing the Captcha number and the program will terminate immediately. Make sure to take back manual control or reexecute the script when that happens!
:::

## Getting started

### Prerequisites

* Python 3
* [Chrome Driver](https://chromedriver.chromium.org/) for your platform
* [Tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html)
* A Good Internet Connection <3

### Getting Started

1. Edit config.py to contain your reservation information.

2. Install Python dependencies

```[bash]
python3 -m pip install -r requirements.txt
```

3. Run the following command to start your booking process!

```[bash]
python3 ./script.py
```
