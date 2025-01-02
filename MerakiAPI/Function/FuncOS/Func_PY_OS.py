import os
# FUNZIONI SU SISTEMA WINDOWS

def getFileName(total_path):
    list_fn=[]
    for path in os.listdir(total_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(total_path, path)):
            list_fn.append(path)
    return list_fn
