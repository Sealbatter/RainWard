# RainWard (still work-in-progress!)
From personal experience, it seems like rain in Singapore is becoming increasingly unpredictable. It is now significantly harder to guess if it will rain over one's estate or not, and therefore, significantly harder to make a decision on whether or not to leave one's laundry out to dry or not. RainWard aims to inform users of the current rain areas over Singapore as well as the 2-hour forecast over every town in Singapore. 

I have not really settled on how I want to implement RainWard as a program yet, but as of now the repository contains the core scripts to perform it's core tasks - visualising current rain areas and showing current 2-hour forecasts.

# How to use
There is no user-interface yet, but there are 2 main scripts in the ```scripts/``` directory that can be run.
1.  ```visualise.py``` which outputs a plot of the most updated 5 minute rainfall readings from Singapore's extensive rain gauge network.
2. ```forecastvisualise.py``` which outputs a plot of the most updated 2-hour weather forecast over every town in Singapore.
