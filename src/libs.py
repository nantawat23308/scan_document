from os import PathLike
from pathlib import Path
import os
from datetime import datetime
from stat import filemode, S_ISDIR, S_ISREG
from pwd import getpwuid
import mimetypes
from src import utility
import stat

ROOT_PATH = root_path = Path('/')
CURRENT_PATH = Path(__file__).resolve().parent
CURRENT_FILE = Path(__file__).resolve()
DIRECTORY_PATH = "/home/nantawat/Desktop/template_code_structure/config"
PATH_CONFIG = os.path.join(DIRECTORY_PATH, "config.json")
FILE_EXTENSION = ["py", "txt", "json", "xlsx", "xls", "csv"]
IMAGE_EXTENSION = ["png", "jpg", "jpeg", "gif", "bmp"]

def get_file_metadata(file_path):
    """
    Extract metadata from file
    os.stat_result(
        st_mode=33204,
        st_ino=28196404,
        st_dev=2053,
        st_nlink=1,
        st_uid=1001,
        st_gid=1001,
        st_size=1595,
        st_atime=1741059044,
        st_mtime=1739942132,
        st_ctime=1741059007)

    parameter: file_path (str) file path for get metadata using os.stat will return to os.stat_result
    return: dict
        {
        "absolute_path": absolute path of file,
        "file_name": name of file
        "file_type":  type of file
        "file_size": file size
        "modified_time": last time modified
        "file_permission": file permission ext. -rw-r--r--
        "DIRorREGFILE": directory or regular file
        "owner_uid": owner user id
        "owner_gid": owner group id
        "name_owner": name of owner
        }
    """


    file_stats = os.stat(file_path)
    mt = mimetypes.guess_type(file_path)
    # replace None with "NULL"
    null = "NULL" # None
    metadata = {
        "absolute_path": os.path.abspath(file_path),
        "file_name": os.path.basename(file_path),
        "file_type": ''.join(Path(file_path).suffixes) if S_ISREG(file_stats.st_mode) and mt[0] else null,
        "file_encode": mt[1] if S_ISREG(file_stats.st_mode) else null,
        "file_size": file_stats.st_size if S_ISREG(file_stats.st_mode) else null,  # in bytes
        "modified_time": datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        "file_permission": filemode(file_stats.st_mode),
        "DIRorREGFILE": "DIR" if S_ISDIR(file_stats.st_mode) else null,
        "owner_uid": file_stats.st_uid,
        "owner_gid": file_stats.st_gid,
        "name_owner": getpwuid(file_stats.st_uid).pw_name,
        "md5": null # utility.calculate_checksum(file_path, "md5") if S_ISREG(file_stats.st_mode) and file_stats.st_mode & stat.S_IRUSR else None
    }
    # metadata = {k: "NULL" if v is None else v for k, v in metadata.items()}
    return metadata


def walktree(top, callback):
    """
    recursively descend the directory tree rooted at top,
    calling the callback function for each regular file
    """
    list_dir = []
    for f in list_all_inside(top):
        pathname = os.path.join(top, f)
        if not os.access(pathname, os.R_OK):
            continue
        mode = os.lstat(pathname).st_mode
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            list_dir.append(get_file_metadata(pathname))
            list_dir.extend(walktree(pathname, callback))
        elif S_ISREG(mode):
            # It's a file, call the callback function
            list_dir.append(callback(pathname))
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)
    return list_dir

def visit_file(file):
    return get_file_metadata(file)

def list_all_inside(directory: str | PathLike) -> list[str]:
    files = []
    try:
        files = os.listdir(directory)
    except (PermissionError, FileNotFoundError):
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    return files

if __name__ == '__main__':
    pass
    # list_dir_all = walktree("/tftpboot", visit_file)
    # print(list_dir_all)
    # print(len(list_dir_all))
    # for i in list_dir_all:
    #     print(i)
    # json_write(list_dir_all, "/home/nantawat/Desktop/template_code_structure/debug/debug.json")
    # print(list_dir_all[0])
    # df = pd.DataFrame(list_dir_all)
    # df.to_csv("/home/nantawat/Desktop/template_code_structure/debug/debug.csv", index=False)
    # print(df.head())
    # print(df.shape)
    # print(df.columns)
    # conn = MySqlConnector(
    #     **{"host": "172.17.106.183",
    #        "user": "root",
    #        "password": "1qaz2wsx",
    #        "database": "nantawats"}
    # )
    # conn.insert_many_to_table(table_name="scan_dir", columns=list(df.columns), json_data=list_dir_all)