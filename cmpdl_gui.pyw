from cmpdl.downloader import do_download
import tkinter as tk 

class GUIAPP(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master.geometry("800x768")
        self.master.minsize(width=400,height=300)
        self.master.title("Curse ModPack downloader for mulit-mc")
        self.pack(fill='both',expand=True)
        # Create Frames
        entry_frame = tk.Frame(self)
        output_frame = tk.Frame(self)

        entry_frame.config(bg = 'green')
        output_frame.config(bg = 'blue')
        
        entry_frame.pack(fill='x',ipady=5,ipadx=5)        
        entry_frame.columnconfigure(1,weight=1)
        output_frame.pack(fill='both',ipady=5,ipadx=5,expand=True)
        output_frame.columnconfigure(0,weight=1)
        output_frame.rowconfigure(0,weight=1)

        # Create widgets
        lb_path = tk.Label(entry_frame,text='Modpack Path:')
        ent_path = tk.Entry(entry_frame)
        btn_openfilediagle = tk.Button(entry_frame,text='Brower')
        btn_download = tk.Button(entry_frame,text='Start download',font="system 16")


        txt_log = tk.Text(output_frame)
        txt_log.config(
            relief = 'sunken',
            # state = 'disabled',
            wrap = 'none',
            bg = '#101010',
            fg = 'green',
            font = 'system 14'
        )

        scroll_log = tk.Scrollbar(output_frame,command=txt_log.yview)

        # Layout widgets
        lb_path.grid(row=0,column=0,padx=5)
        ent_path.grid(row=0,column=1,pady=5,sticky=('e','w'))
        btn_openfilediagle.grid(row=0,column=2,padx=5,sticky='e')
        btn_download.grid(row=1,column=0,columnspan=3,padx=5,sticky=('e','w'))

        txt_log.grid(row=0,column=0,sticky=('n','s','e','w'))


if __name__ == '__main__':
    root = tk.Tk()
    app = GUIAPP(root)
    app.mainloop()