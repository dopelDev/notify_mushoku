from bs4 import BeautifulSoup
from requests import get
from pprint import pprint as pp
from json import loads
from typing import NamedTuple, Dict, List
from csv import writer
import pandas as pd
import logging
from os.path import exists
from os import getcwd

def log_config(args):
    format_config = '%(asctime)s:%(levelname)s:%(message)s'
    logging.basicConfig(level=logging.INFO, filename='moshuko.log', format=format_config, filemode='w')
    logging.info('arguments choice : {}'.format(args))

class Results(NamedTuple):
    last_episode : Dict
    episodes : Dict

def getting() -> Results:
    Urls = {'last_episode' : 'https://jkanime.net/ajax/last_episode/2951/', 'list_episodes' : 'https://jkanime.net/ajax/pagination_episodes/2951/1/'}
    result_last_episode = get(Urls.get('last_episode'))
    result_list = get(Urls.get('list_episodes'))
    result_last_episode_json = loads(result_last_episode.text)
    result_list_json = loads(result_list.text)

    # json.loads regresa un lista con el json o dicta

    return Results(result_last_episode_json[0], result_list_json)
    
def save_csv(list_episodes : List):
    headers = list_episodes[0].keys()
    with open('list_episodes.csv', 'w') as file:
        writer_file = writer(file)
        writer_file.writerow(headers)
        for item in list_episodes:
            writer_file.writerow(item.values())
        file.close()

def compare_last_episode(path : str) -> bool :
    data_Frame = pd.read_csv(path)
    last_episode, _ = getting()
    logging.info('el ultimo episodio es : {}'.format(last_episode['number'])) 
    # pasar data_Frame como str porque al salir de pandas sale como numpy Number

    return True if last_episode['number'] == str(data_Frame.iloc[-1].at['number']) else False

def exists_csv():
    path = getcwd()
    if exists(path + '/list_episodes.csv'):
        pass
    else:
        result_list = get('https://jkanime.net/ajax/pagination_episodes/2951/1/')
        result_list_json = loads(result_list.text)
        save_csv(result_list_json)
        logging.info('No existia la lista de episodios. Se a creado una')

