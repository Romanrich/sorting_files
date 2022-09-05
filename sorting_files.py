import shutil
import sys
import os

def get_dir_name():
    work_dir = ''
    args = sys.argv
    if len(args) == 1:
        work_dir = input('Enter path to directory: ')   
    else:
        work_dir = args[1]
    while True:
        if not os.path.exists(work_dir):
            work_dir = input('Enter path to directory: ')
        else:
            break
    return work_dir

def read_dir(namedir):
    return os.listdir(namedir)

def is_free_dir(namedir):
    global name_folder
    lists_free_dir = (
        os.path.join(name_folder, 'images'),
        os.path.join(name_folder, 'video'),
        os.path.join(name_folder, 'documents'),
        os.path.join(name_folder, 'audio'),
        os.path.join(name_folder, 'archives'),
    )
    return True if namedir in lists_free_dir else False 

def check_file_type(file):
    ext = file.split('.')
    if len(ext) > 1:
        if ext[len(ext)-1] in ('jpeg', 'png', 'jpg', 'svg'):
            return 'images'
        elif ext[len(ext)-1] in ('avi', 'mp4', 'mov', 'mkv'):
            return 'video'
        elif ext[len(ext)-1] in ('doc', 'docx', 'txt', 'pdf', 'xls', 'xlsx', 'pptx'):
            return 'documents'
        elif ext[len(ext)-1] in ('mp3', 'ogg', 'mov', 'amr'):
            return 'audio'
        elif ext[len(ext)-1] in ('zip', 'gz', 'tar'):
            return 'archives'
        else:
            return None
    else:
        return None

def rename_file(folder_to, folder_from, file):
    global name_folder
    path_to = os.path.join(name_folder, folder_to)
    if not os.path.exists(path_to):
        os.makedirs(path_to)
    if folder_to != 'archives':
        os.rename(os.path.join(folder_from, file), os.path.join(path_to, normalize(file)))
    else:
        f = normalize(file).split('.')
        shutil.unpack_archive(os.path.join(folder_from, file), os.path.join(path_to, f[0]), f[1])
        os.remove(os.path.join(folder_from, file))

def normalize(file):
    map = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 
    'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 
    'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'і': 'i',  'є': 'e', 'ї': 'i', 'А': 'A', 
    'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 
    'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 
    'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', 'І': 'I',  'Є': 'E',  'Ї': 'I'}
    lists = file.split('.')
    name_file = '.'.join(lists[0:len(lists)-1])
    new_name = ''
    for el in name_file:
        if el in map.keys():
            new_name += map[el]
        elif (66 <= ord(el) <= 90) or (97 <= ord(el) <= 122) or el.isdigit():
            new_name += el
        else:
            new_name += '_'
    return new_name + '.' + lists[len(lists)-1]

def sorting_dir(namedir):
    lists = read_dir(namedir)
    for el in lists:
        path_file = os.path.join(namedir, el)
        if is_free_dir(path_file):
            continue
        if os.path.isdir(path_file):
            sorting_dir(path_file)
        else:
            folder = check_file_type(el)
            if folder:
                rename_file(folder, namedir, el)

def check_clear_dir(namedir):
    lists = os.listdir(namedir)
    if len(lists) == 0 and not is_free_dir(namedir):
        os.rmdir(namedir)
    else:
        for el in lists:
            path_el = os.path.join(namedir, el)
            if os.path.isdir(path_el):
                check_clear_dir(path_el)

if __name__ == '__main__':
    name_folder = get_dir_name()
    sorting_dir(name_folder)
    check_clear_dir(name_folder)

