from statistic import Stat
from additional import write_log_file

message = '''
This file exist for resetting statistics
Your last scores will deleted
Are you sure that you need to reset it? 
Write "Yes" if you need or "Not" if not 
>>>> '''
stat = Stat()
agreement = input(message)

def rewrite():
    global stat
    if len(stat.score) > 0:
        write_log_file('User reset statistics (scores: {}, levels: {})'.format(tuple(stat.score), tuple(stat.levels)))
        stat.rewrite_file(True)
    print('Statistic resetting successful !')


if __name__ == '__main__':
    if agreement.lower() == 'yes':
        rewrite()
    else: write_log_file('User canceled statistics reset.')