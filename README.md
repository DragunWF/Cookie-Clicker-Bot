# Cookie Clicker Bot

![GitHub top language](https://img.shields.io/github/languages/top/DragunWF/Cookie-Clicker-Bot)
![Lines of code](https://img.shields.io/tokei/lines/github/DragunWF/Cookie-Clicker-Bot)
![GitHub repo size](https://img.shields.io/github/repo-size/DragunWF/Cookie-Clicker-Bot)

## Table Of Contents

- [Description](#Description)
- [Functionalities](#Functionalities)
- [Setup](#Setup)
- [Details](#Details)
- [Packages](#Packages)
- [Contact](#Contact)

## Description

Hello! This is a Python bot powered with Selenium. A bot that automates cookie clicker
for your desires. Have fun!

**Note:** This project is not being updated anymore.

## Functionalities

- Automatically clicks the big cookie for you.
- Automatically upgrades products whenever they're available (Mines, Farms, Factories, etc...).
- Automatically buys product buffs from the store.
- Automatically clicks golden cookies as soon as they appear on the screen.
- Automatically saves your game at the end of each session (Given if you use the quit key to exit).
- Automatically saves the stats at the start and of each session at `data/sessions.json`.
- Can automatically load your save file when enabled in `data/settings.json`.

## Setup

- Just like every bot with Selenium, you got to make sure your
  [chrome web driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
  is installed and have downloaded the correct web driver for your version of chrome.
- Given if you have the prerequisites stated above, **you can immediately start by just running**
  `main.py` **to start the bot.**

```json
[
  {
    "controlled": true,
    "bakery_names": [
      "Robot",
      "Catharsis",
      "Ruthenia",
      "Starling",
      "Enderalean",
      "Nether"
    ],
    "controls": {
      "start_automation": "num 1",
      "stop_automation": "num 2",
      "quit_game": "num 3"
    },
    "saves": {
      "load_save_file": false,
      "location": "data/saves/EnderaleanBakery.txt"
    }
  }
]
```

- If you want to change the bot's settings you can either do it at the start of the program
  by inputting `n` where my program asks you if you want to use the default settings or you
  can change it by directly editing the values at `data/settings.json`.
- If you want to load a save file once the bot starts, you can do so going to `data/settings.json`
  then setting `"load_save_file"`to `true` and by specifying the file path to your save file
  in `"location"` at `"saves"`.

## Details

- The `"bakery_names"` property in `data/settings.json` is an array of strings used for choosing
  a random bakery name on startup. If you want it to only choose one name, you can remove all other
  elements of the array and only add one string with your desired bakery name in it.
- I highly recommend you leave `"controlled"` set as `true` but if you really don't want to
  have any controls, you can set `"controlled"` in `data/settings.json` to `false`. One warning
  though, without the controls the bot doesn't automatically save your game so you have to
  do it manually in the game.
- For the controls you have to hold the key for it to trigger instead of pressing it lightly.

### Modules

- `selenium=4.2.0`
- `webdriver-manager=3.7.0`
- `pyttsx=2.87`
- `keyboard`

### Controls

- **Numpad 1** -> To turn on automation
- **Numpad 2** -> To turn off automation
- **Numpad 3** -> To quit the game. It also saves your game right before it exits.

**Note:** You can change these controls in `data/settings.json` at the `"controls"`
property.

## Contact

If you want to contact me about suggestions or bugs to report with this project, you
can contact me via discord. My discord tag is **dragunwf**.
