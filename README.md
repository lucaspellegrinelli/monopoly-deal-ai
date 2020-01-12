# Monopoly Deal Engine/AI

## The Game
You can read the rules, check out the cards and everything in http://monopolydealrules.com/

## The Project
This is a toy project that aims to create a fully working Monopoly Deal simulator and a sort of framework where I (and you) can create bots to play it. Maybe in the future if I'm very bored I'll make UI for all of this...

## How run it
You'll need first to have Python (I've tested with both 2.7.12 and 3.7.3). You also won't need any other packages, the vanilla version of Python is sufficient.

To run a match with the bots, you can check the [```run.py```](https://github.com/lucaspellegrinelli/monopoly-deal-ai/blob/master/run.py) file, it is a very simple and straightforward example on how to build and run a match.

After that, just run

```
python run.py
```

## How to create a bot

You can look up [```ai.py```](https://github.com/lucaspellegrinelli/monopoly-deal-ai/blob/master/monopoly/ai.py) for a better grasp on what you'll need to do to create a bot. In that file there are "very" detailed information on what each and every method your AI class needs to have. You can also take a look on the [```RandomAI```](https://github.com/lucaspellegrinelli/monopoly-deal-ai/blob/master/bots/random_ai.py) code for a working example.

### Disclaimer
Although this simulator seems to work, I have no guarantee that it actually works flawlessly since not enough formal testing we made. Take it with a grain of salt.
