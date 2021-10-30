from methods import compare_last_episode, save_csv
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
    print(args)
    interval = 60 * args.interval
    timeout = (args.timeout * 60) / args.interval
    while(len(timeout)):
        notification_main()
        sleep(interval)
            
    if(args.update):
        save_csv('list_episodes.csv')


if __name__ == '__main__':
    main()
