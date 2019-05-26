from cmpdl import MobPack_Downloader
import tkinter as tk
from threading import Thread

class GUIAPP(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master.geometry("800x768")
        self.master.minsize(width=400,height=300)
        self.master.title("Curse ModPack downloader")
        self.pack(fill='both',expand=True)
        self.is_downloading = False
        # Create Frames
        entry_frame = tk.Frame(self)
        output_frame = tk.Frame(self)

        # entry_frame.config(bg = 'green')
        # output_frame.config(bg = 'blue')
        
        entry_frame.pack(fill='x',ipady=5,ipadx=5)        
        entry_frame.columnconfigure(1,weight=1)
        output_frame.pack(fill='both',ipady=5,ipadx=5,expand=True)
        output_frame.columnconfigure(0,weight=1)
        output_frame.rowconfigure(0,weight=1)

        # Create widgets
        lb_path = tk.Label(entry_frame,text='Modpack Path:')
        self.ent_path = tk.Entry(entry_frame)
        self.btn_openfilediagle = tk.Button(entry_frame,text='Brower',command=self._brower)
        self.btn_download = tk.Button(entry_frame,text='Start download',font="system 16",command=self._download_start)

        self.txt_log = tk.Text(output_frame)
        self.txt_log.config(
            relief = 'sunken',
            # state = 'disabled',
            wrap = 'none',
            bg = '#101010',
            fg = 'green',
            font = 'system 14'
        )

        scroll_log = tk.Scrollbar(output_frame,command=self.txt_log.yview)

        # Layout widgets
        lb_path.grid(row=0,column=0,padx=5)
        self.ent_path.grid(row=0,column=1,pady=5,sticky=('e','w'))
        self.btn_openfilediagle.grid(row=0,column=2,padx=5,sticky='e')
        self.btn_download.grid(row=1,column=0,columnspan=3,padx=5,sticky=('e','w'))

        self.txt_log.grid(row=0,column=0,sticky=('n','s','e','w'))

    def _message_output(self,message,level):
        msg = '[%s] %s \n' % (level.upper(),message)
        self.txt_log.insert(tk.END,msg)

    def _download_start(self):
        if self.is_downloading:
            self.txt_log.insert(tk.END,'Download is runing!Please wait until it finish!\n')
        else:
            self.txt_log.delete(1.0,tk.END)
            path = self.ent_path.get()
            self.txt_log.insert(tk.END,path + '\n')
            dl = MobPack_Downloader(self._message_output)
            t = Thread(target=dl.download_modpack,args=(path,self._on_start,self._on_finish),daemon=True)
            t.start()

    def _brower(self):
        if self.is_downloading:
            self.txt_log.insert(tk.END,'Download is runing!Please wait until it finish!\n')
        else:
            self.txt_log.insert(tk.END,'Download is not runing!\n')
    
    def _on_start(self):
        self.btn_download.disabled = True
        self.is_downloading = True
    
    def _on_finish(self):
        self.btn_download.disabled = False
        self.is_downloading = False

if __name__ == '__main__':
    root = tk.Tk()
    app = GUIAPP(root)
    app.mainloop()