#-------------------------------------------------------------------------------
# Name:        main
# Purpose:
#
# Author:      m.j_banitaba
#
# Created:     14/07/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from tkinter import *
import urllib
from urllib.request import urlopen
import urllib.request
from html.parser import HTMLParser
import traceback
import logging
logging.basicConfig(level=logging.DEBUG)
call_backs={}
def binding(event_name,func,*globals_args):
    global call_backs
    call_backs[event_name]=(func,globals_args)
def invoke(event_name,*args):
    global call_backs
    if event_name in call_backs:
        func,globals_args=call_backs[event_name]
        func(*(globals_args+args))
    pass
def ent(event):
    logging.debug(event.keysym_num)
    if event.keysym_num==65293:
        #return key pressed
        invoke('change url')
        return 'break'
def load_url(url):
    logging.debug(url)
    try:
        req = urllib.request.Request(url=url)
        with urllib.request.urlopen(req) as f:
            data = f.read().decode('utf-8')
    except Exception as e:
        traceback.print_exc()
        data = ""
    return data

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.objects=[]
        self.parent=[]
        self.current=None
    def handle_starttag(self, tag, attrs):
##        logging.debug ("Encountered a start tag:", tag)
        t=[]
        for attr in attrs:
##            logging.debug( "     attr:", attr)
            t.append(attr)
        nob={
            'name':tag,
            'attr':t,
            'parent':None,
            'childs':[],
            'data':None
            }
##        print nob
        if self.current:
            self.parent.append(self.current)
            nob['parent']=self.current
            self.current['childs'].append(nob)
            self.current=nob
        else:
            self.objects.append(nob)
            self.current=nob

    def handle_endtag(self, tag):
##        logging.debug "Encountered an end tag :", tag
        if self.current['name']==tag:
            if len(self.parent)>0:
                self.current=self.parent.pop()
            else:
                self.current=None
        else:
            #error
            pass
    def handle_data(self, data):
##        logging.debug "Encountered some data  :", data
        if self.current:
            self.current['data']=data
    def handle_comment(self,comment):
##        logging.debug "Encountered some comment  :", comment
        return
    def handle_decl(self,decl):
##        logging.debug "Encountered some decl  :", decl
        return
    def unknown_decl(self,decl):
##        logging.debug "Encountered some unknown decl  :", decl
        return

    def get_objects(self):
        return self.objects
def data_to_object(data):

    p=MyHTMLParser()
    p.feed(data)
    return p.get_objects()
def object_to_tkinter(root,objects,master):
    for itm  in objects:
        name=itm['name']
        if name=='html':
            f=Frame(master,background='red')
            f.pack(fill=BOTH,expand=YES)
##            if itm['data']<>None:
##                logging.debug itm['data']
##                l=Label(f,text=itm['data'],background='blue')
##                l.pack()
            object_to_tkinter(root,itm['childs'],f)
        elif name=='meta':
            logging.debug(itm['data'])
        elif name=='script':
            logging.debug(itm['data'])
        
        elif name=='body':
            f=Frame(master,background='red')
            f.pack()
            if itm['data']:
                logging.debug(itm['data'])
                l=Label(f,text=itm['data'],background='blue')
                l.pack()
            object_to_tkinter(root,itm['childs'],f)
        elif name=='div':
            f=Frame(master,background='orange')
            f.pack()
            if itm['data']:
                logging.debug(itm['data'])
                l=Label(f,text=itm['data'],background='blue')
                l.pack()
            object_to_tkinter(root,itm['childs'],f)
        elif name=='head':
            f=Frame(master,background='red')
            f.pack()
            if itm['data']:
                logging.debug(itm['data'])
                l=Label(f,text=itm['data'],background='blue')
                l.pack()
            object_to_tkinter(root,itm['childs'],f)
        elif name=='title':
            root.wm_title(itm['data'])
        elif name=='style':
            pass
        elif name=='h2':
            l=Label(master,text=itm['data'],background='blue')
            l.pack()
            object_to_tkinter(root,itm['childs'],l)
        else:
            logging.debug('unknown tag %s',itm['name'])
            f=Frame(master,background='red')
            f.pack()
            if itm['data']:
                logging.debug(itm['data'])
                l=Label(f,text=itm['data'],background='blue')
                l.pack()
            object_to_tkinter(root,itm['childs'],f)
            break



def event_change_url(root,url_widget,frame_widget):
    url=url_widget.get(1.0,END)
    url_data=load_url( url)
    url_object=data_to_object(url_data)
##    logging.debug url_object
    for child in frame_widget.winfo_children():
        child.destroy()
    object_to_tkinter(root,url_object,frame_widget)
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))
def FrameWidth( event):
    canvas_width = event.width
    event.widget.itemconfig(event.widget.c_w, width = canvas_width)
def main():

    root = Tk()
    address= Text(root,height=1)
    address.grid(pady=0)
    address.pack( fill=X)
    address.bind('<Key>',ent)
##    address.insert(END,"http://localhost/")
    # address.insert(END,"https://www.google.com/")
    address.insert(END,"https://time.ir/")

    w=root.winfo_reqwidth()
    canvas = Canvas(root, borderwidth=0, background="#000")
    f=Frame(canvas,background='black',height=w)
    canvas.ff=f
##    f.grid(pady=0,ipadx=1)
##    f.pack(fill=BOTH,expand=YES)
    vsb = Scrollbar(canvas, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.c_w=canvas.create_window((0,0), window=f, anchor="nw")
    canvas.bind('<Configure>', FrameWidth)
    f.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    binding('change url',event_change_url,root,address,f)
    invoke('change url')
    root.mainloop()
    pass

if __name__ == '__main__':
    main()
