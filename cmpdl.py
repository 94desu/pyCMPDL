from os import cpu_count,mkdir,getcwd
from urllib.parse import unquote
from requests import get as reget
import json
from pathlib import Path
from threading import Thread,Lock

def do_download(modpack_dir,mulit_thread_on=None,thread_count=None):
    #pre-set the default parameters
    if mulit_thread_on is None : mulit_thread_on = True
    if thread_count is None : thread_count = 4
    if thread_count > 4 : thread_count = 4

    modpackPath = Path(modpack_dir)
    if not modpackPath.exists():
        print('ModPack path not found: "%s"' % str(modpackPath))
        print('Task end without success!')
        return
    manifestPath = modpackPath / 'manifest.json'
    if not manifestPath.exists():
        print('"manifest.json" not found in path: "%s"' % str(modpackPath))
        print('Task end without success!')
        return
    mcPath = modpackPath / 'minecraft'   
    modsPath = mcPath / 'mods'
    if not mcPath.exists(): mkdir(mcPath)
    if not modsPath.exists(): mkdir(modsPath)
    modlist = __get_files_url_list(manifestPath)

    if mulit_thread_on:
        modlist_list = []
        for i in range(thread_count):
            modlist_list.append(modlist[i::thread_count])
        
        ths = []
        for modl in modlist_list:
            ths.append(Thread(target=__download_files,args=(modl,modsPath),daemon=True))

        for th in ths:
            th.start()

        for th in ths:
            th.join()
    else:
        __download_files(modlist,modsPath)
    print('Download has been done!')

def __download_files(file_url_list,targetPath):
    for furl in file_url_list:
        file_resp = reget(furl,stream=True)
        end_url = file_resp.history[-1].url
        filePath = Path(end_url)
        fileName = unquote(filePath.name)
        if not fileName =='download':
            with open(str(targetPath / fileName),'wb') as fmod:
                fmod.write(file_resp.content)
            print('%s is downloaded!' % fileName)
        else:
            print('file not found with url : %s' % end_url)

def __read_manifest(manifest):
    mf = open(manifest,'r')
    dic_mf = json.load(mf)
    mf.close()
    return dic_mf

def __get_files_url_list(manifest):
    filesurl_prefix = 'https://minecraft.curseforge.com/projects/'
    dic_m = __read_manifest(manifest)
    mods_list = []
    for m in dic_m['files']:
        if m['required'] == True:
            mod_url = "%s%s/files/%s/download" % (filesurl_prefix,m['projectID'],m['fileID'])
            mods_list.append(mod_url)
    return mods_list

def __do_overrides(overridesPath):
    if overridesPath.exists():
        pass
    else:
        print('Override directory not found!')
    pass

if __name__ == '__main__':
    do_download(getcwd())