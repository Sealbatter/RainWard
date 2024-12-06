'''
This is the main script that is to be executed every 5 minutes. The action of this script is to
Fetch precipitation data -> Check if raingauge nearest to user's location is non-zero
'''

from visualise import Visualise
from datafetch import PrecipFetch

CurrentPrecipDF = PrecipFetch
