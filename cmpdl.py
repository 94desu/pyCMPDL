from os           import mkdir,getcwd
from urllib.parse import unquote
from pathlib      import Path
from threading    import Thread,Lock
from queue        import Queue
from requests     import get as reget
import json


class MobPack_Downloader():

    def __init__(self,message_handler=None):
        self.download_lock = Lock()
        self.logs = []
        self.message_handler = message_handler if message_handler else self._log


    def download_modpack(self,modpack_directory,on_start=None,on_finish=None):
        modpackPath = Path(modpack_directory)
        if not modpackPath.exists():
            self._message('ModPack path not found: "%s"' % str(modpackPath),'error')
            if on_finish:on_finish()
            return False

        manifestFile = modpackPath / 'manifest.json'
        if not manifestFile.exists():
            self._message('"manifest.json" not found in path: "%s"' % str(modpackPath),'error')
            if on_finish:on_finish()
            return False
        
        if on_start:on_start()
        self._message("Start download mod pack!")
        self.logs = []
        manifest = self._read_manifest(manifestFile)

        # create folder './minecraft/mods' if it's not exists
        mcPath = modpackPath / 'minecraft'
        modsFolder = mcPath / 'mods'
        if not mcPath.exists(): mkdir(mcPath)
        if not modsFolder.exists(): mkdir(modsFolder)

        download_queue = self._get_download_queue(manifest['files'])
        self.dl_total = download_queue.qsize()
        self.dl_done = 0

        for i in range(4):
            t = Thread(target = self._download_files, args=(download_queue,modsFolder), daemon=True)
            t.start()

        download_queue.join()
        self._message("Finish download mod pack!")
        if on_finish:on_finish()


    def _download_files(self,download_queue,targetPath):
        while not download_queue.empty():
            # get content(reget() = requests.get())
            file_resp = reget(download_queue.get(block=False),stream=True)

            # read the final redirection link url 
            end_url = file_resp.history[-1].url

            # get the file name from end_url
            filePath = Path(end_url)
            fileName = unquote(filePath.name)
            if not fileName =='download':
                with open(str(targetPath / fileName),'wb') as f:
                    f.write(file_resp.content)
                with self.download_lock:
                    self.dl_done += 1
                    self._message('[%d/%d] File is downloaded:%s' % (self.dl_done,self.dl_total,fileName))
            else:
                with self.download_lock:
                    self.dl_done += 1
                    self._message('[%d/%d] File is not found: %s' % (self.dl_done,self.dl_total,end_url),'warning')
            download_queue.task_done()

    def _get_download_queue(self,files):
        filesurl_prefix = 'https://minecraft.curseforge.com/projects'
        dl_queue = Queue()
        for m in files:
            mod_url = "%s/%s/files/%s/download" % (filesurl_prefix,m['projectID'],m['fileID'])
            dl_queue.put(mod_url)
        return dl_queue

    def _read_manifest(self,manifestFile):
        with open(manifestFile,'r') as mf:
            dic_mf = json.load(mf)
        return dic_mf


    def _message(self,message,level=None):
        level = level if level else 'info'
        if level not in self._MSG_LEVEL:level = 'info'
        self.message_handler(message,level)


    #default message handler
    def _log(self,message,level):
        log_msg = '[%s][%s] %s' % (level.upper(),'timestmap here',message)
        print(log_msg)
        self.logs.append(log_msg)

    _MSG_LEVEL = ('debug','info','warning','error')


if __name__ == '__main__':
    dl = MobPack_Downloader()
    dl.download_modpack(getcwd())