#!/home/dopel/venv/notify/bin/python

from methods import compare_last_episode, save_csv, getting, log_config
from notifypy import Notify
import argparse
from time import sleep

def arguments():
    parser = argparse.ArgumentParser(description = 'Es uno notificador de episodio nuevo de mushoku en Jkanime.net', prog='Notify Mushoku')
    parser.add_argument('--interval', type=int, default=10, help='Interval in minutes')
    parser.add_argument('--update', type=bool, default=False, help='actualizar list_episodes')
    parser.add_argument('--timeout', type=int, default=8, help='timeout in hours')
    args = parser.parse_args()

    return args

def notification_main():
    notification = Notify()
    notification.message = 'Ya salio un nuevo episodio'
    notification.title = 'Mushoku Jobless'

    if not compare_last_episode('list_episodes.csv'):
        notification.send()

def main():
    args = arguments()
    log_config(args) # init configuration de logging
    interval = 60 * args.interval
    timeout = int((args.timeout * 60) / args.interval)
    for _ in range(timeout):
        notification_main()
        if(args.update) and not compare_last_episode('list_episodes.csv'):
            _, list_episodes = getting()
            save_csv(list_episodes)

        sleep(interval)
            
    

if __name__ == '__main__':
    main()
