import os
import codecs


'''
This module using for additional functions and contain this functions
    check_int
        return for you True if number may to tranform into int()
    directory_finder
        return you dictionary with all necessary paths
    check_settings
        import all necessary data from "settings" file
'''


def check_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def check_bool(string):
    find = None
    if string.lower() == 'true' or string.lower() == 'yes':
        find = True
    elif string.lower() == 'false' or string.lower() == 'no':
        find = False
    return find


def directory_finder():
    from sys import platform

    if platform == "win32":
        _os_ = "windows"
        main_dir = os.getcwd()
        media_dir = main_dir + "\\media\\"
        shop_dir = media_dir + "shop\\"
        mode_dir = media_dir + "mode\\"
        slash = '\\'
        temp_dir = os.getenv('TEMP')
        if temp_dir == None: temp_dir = os.getenv('TMP')
        temp_dir += slash
    # ~ elif platform == "darwin": _os_ = "OS X"
    else:
        _os_ = "linux or MacOS"
        main_dir = os.getcwd()
        media_dir = main_dir + "/media/"
        shop_dir = media_dir + "shop/"
        mode_dir = media_dir + "mode/"
        slash = "/"
        temp_dir = os.getenv('TEMP')
        if temp_dir == None: temp_dir = os.getenv('TMP')
        temp_dir += slash

    directories = {
        "os":_os_,
        "platform": platform,
        "slash": slash,
        "temp_dir": temp_dir,
        "main_dir": main_dir,
        "media_dir": media_dir,
        "shop_dir": shop_dir,
        "mode_dir": mode_dir
    }
    return directories


directories = directory_finder()
temp_dir = directories['temp_dir']


def check_settings():
    f = open('settings')
    data = f.read()
    f.close()
    data = data.split('\n')

    keys_name = ['save_stat', 'SOUND', 'WIDTH', 'HEIGHT', 'FPS']
    settings_dict = {}
    for i in range(len(data)):
        temp = data[i].split(' ')
        first_word = temp[0]
        if data[i] != '':
            if data[i].split(' ')[-1] == 'Yes': settings_dict[keys_name[i]] = True
            else: settings_dict[keys_name[i]] = False
            if first_word in keys_name:
                for one in keys_name:
                    if one == first_word:
                        num = temp[-1]
                        if check_int(num): settings_dict[first_word] = int(num)
                        # elif check_bool(num) != None: check_bool(num)
                        else: print('Settings not correct')

    return settings_dict


def write_temp_file(file_name, *args):
    global temp_dir
    new_data = ''
    for arg in args: new_data += '{}\n'.format(arg)
    new_data = new_data.strip('\n')
    # file_name = 'count_of_shell.ai'
    f = codecs.open(temp_dir + file_name, 'w', 'utf-8')
    f.write(new_data)
    f.close()


def read_temp_file(file_name):
    global temp_dir

    # file_name = 'count_of_shell.ai'
    f = codecs.open(temp_dir + file_name, 'r', 'utf-8')
    data = f.read()
    f.close()
    new_data = []
    for line in data.split('\n'):
        if check_int(line): line = int(line)
        if line != '': new_data.append(line)

    return new_data