import patoolib, start, shutil, os, time
from logger import lof_file

patch, all_format, program = start.get_setting()


def unzip(file):

    outdirect = f'{file.split('.')[0]}'

    try:
        direct = os.listdir(patch)

        if outdirect.split('\\')[-1] in direct:
            shutil.rmtree(outdirect)
        time.sleep(1.2)
        patoolib.extract_archive(archive=file, verbosity=-1, outdir=outdirect, program=program)
        time_now = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())
        print(f"{time_now} - Разархивирован файл: {file}")
        lof_file(f"{time_now} - Разархивирован файл: {file}\n")
        time.sleep(1.2)
        os.remove(file)
        time_now = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())
        print(f"{time_now} - Удалён файл: {file}")
        lof_file(f"{time_now} - Удалён файл: {file}\n")
        return True, file
    except Exception as Exc:
        #print(Exc)
        return False, file




