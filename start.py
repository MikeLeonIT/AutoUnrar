def get_setting():
    with open('setting', 'r', encoding='utf-8') as file:
        setting_list = [param.rstrip() for param in file]
        path = setting_list[0].split(' = ')[-1]
        #print(setting_list)

        format = setting_list[1].split(' = ')[-1]
        all_format = [x for x in format.split(',')]
        #print(all_format)

        program = setting_list[2].split(' = ')[-1]

    return path, all_format, program


def get_path():
    with open('setting', 'r', encoding='utf-8') as file:
        setting_list = [param.rstrip() for param in file]
        path = setting_list[0].split(' = ')[-1]
        return path
#get_setting()
