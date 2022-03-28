# Cookie Clicker Bot

## Table Of Contents

- [Description](#Description)
- [Functionalities](#Functionalities)
- [Setup](#Setup)
- [Details](#Details)
- [Contact](#Contact)

## Description

Hello! This is a Python Bot powered with Selenium. A bot that automates cookie clicker
for you.

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
  [chrome webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
  is installed and have downloaded the correct webdriver for your version of chrome.
- **You can immediately start by just running** `main.py` **to start the bot.**

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

## Details

- I highly recommend you leave `"controlled"` set as `true` but if you really don't want to
  have any controls, you can set `"controlled"` in `data/settings.json` to `false`. One warning
  though, without the controls the bot doesn't automatically save your game so you have to
  do it manually in the game.

### Controls

- Numpad 1 -> to turn on automation
- Numpad 2 -> to turn off automation
- Numpad 3 -> to quit the game. It also saves your game right before it exits.

**Note:** You can change these controls in `data/settings.json` at the `"controls"`
property.

## Contact

If you want to contact me about suggestions or problems with this project, you
can contact me via discord. My discord tag is **DragonWF#9321**.
