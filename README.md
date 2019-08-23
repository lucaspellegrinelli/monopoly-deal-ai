# Monopoly Deal Engine/AI

## The Game
You can read the rules, check out the cards and everything in http://monopolydealrules.com/

## The Project
This is a toy project that aims to create a fully working Monopoly Deal simulator and a sort of framework where I (and you) can create bots to play it. Maybe in the future if I'm very bored I'll make UI for all of this...

## How to use it
You'll need first to have Python (I've tested with both 2.7.12 and 3.7.3). You also won't need any other packages, the vanilla version of Python is sufficient.

To run a match with the bots, you can check the [```run.py```](https://github.com/lucaspellegrinelli/monopoly-deal-ai/blob/master/run.py) file, it is a very simple and straightforward example on how to build and run a match.

After that, just run

```
python run.py
```

### Disclaimer
Although this simulator seems to work, I have no guarantee that it actually works flawlessly (or works at all, I've never watched a full game the bots played to see if there's an illegal move). The only benchmark I used to "make sure" it works is counting the number of cards of each type in the game to make sure none of them were getting lost or duplicated and some eye ball check to see if the plays made sense rullings wise. Take it with a grain of salt.
