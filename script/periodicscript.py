import time
from csv import writer
from collectdata import CollectData
import logging
logging.basicConfig(level = logging.INFO)

import pandas as pd
import os

import datetime

PATH = os.getcwd()
MINUTES = 10
DESTINATION_DIR = '../data/data.csv'
def PeriodicJob():
    '''
    Every 15 minutes, fetches the 2 hour forecast from data.gov.sg API and
    writes the Timestamp of the forecast as well as the Valid Period into
    data.csv. This allows us to keep track of how often the forecasts are
    updated as time passes.
    '''

    logging.info(f'Runnning a periodic script! This script will execute once every {MINUTES} minutes!')

    while True:
        now = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        data = pd.read_csv(os.path.join(PATH, 'frequencydata', 'data.csv'), on_bad_lines='warn')
        MostRecentTimestamp = data['Timestamp'].iloc[-1]

        logging.info(f'Data collected from data.gov.sg API, time now is {now}!')
        NextInput = CollectData()
        NextInput.append(now)
        CurrentTimestamp = NextInput[0]

        if MostRecentTimestamp != CurrentTimestamp: # Checks if the most recent Timestamp is 
                                                    # same as the current Timestamp

            # Writes the latest forecast Timestamp into data.csv
            with open(DESTINATION_DIR, 'a') as f_object:
        
                writer_object = writer(f_object)

                logging.info('Current Timestamp is different from most recent Timestamp, writing into data.csv now...')
                writer_object.writerow(NextInput)
            
                # Close the file object
                f_object.close()

        else:
            logging.info('Current Timestamp is the same as the most recent Timestamp, doing nothing...')

        time.sleep(MINUTES*60) # run the job every 10 minutes

if __name__ == '__main__':
    PeriodicJob()