from tkinter import *
from tkinter.ttk import *
from mailer_class import Mailer, Letter
from utilites import *
import pathlib


journal_current_file=pathlib.Path(__file__).parent.joinpath('current_file.txt')


mailer=Mailer(journal_current_file)
rec_obj=Recievers()
root_windows = Tk()
root_windows.grid_columnconfigure(4, weight=5)
root_windows.title("Eskin SMTP Mailer")
frame_entry=Frame(root_windows)
frame_buttoms=Frame(root_windows)
current_sender=mailer.read_sender()
sender_label=Label(frame_entry,text="Sender: ")
sender_mail=Label(frame_entry,text=current_sender)
# update_sender_btn=Button(frame_entry,text='Update sender', command=lambda mail_obj=mailer, lbl=sender_mail: update_sender(mail_obj, lbl))
receiver_mail_label=Label(frame_entry, text= 'Send to: ')
receiver_mail_enter=Entry(frame_entry)
load_senders_from_csv=Button(frame_entry,text='From CSV', command= lambda mailer_obj=mailer:load_recievers(mailer_obj, rec_obj))
var1 = BooleanVar()
var1.set(0)
read_html = Checkbutton(frame_entry, text="Read HTML tags",
                 variable=var1,
                 onvalue=1, offvalue=0)


title_label=Label(frame_entry, text= 'Title ')
title_enter=Entry(frame_entry)
text_label=Label(frame_entry, text= 'Text: ')
text_enter=Text(frame_entry)
file_list=[]
body_img_list=[]

file_number=Label(frame_entry,text= f'Selected {len(file_list)} files')
body_file_number=Label(frame_entry,text= f'Selected {len(body_img_list)} files')
file_btn=Button(frame_entry, text='Select file', command= lambda lbl= file_number :add_file(file_list, lbl  ))
body_file_btn=Button(frame_entry, text='Body file', command= lambda lbl= body_file_number :add_file(body_img_list, lbl  ))
send_status_label=Label(frame_entry, text='')
send_btn=Button(frame_entry, text='SEND',command= lambda sender=current_sender, recievers=receiver_mail_enter,
                                                                           read_html=var1, title=title_enter, 
                                                                           text=text_enter, files=file_list, lbl=send_status_label: 
                                                                           sending(rec_obj, sender, recievers,read_html, title, text, files, body_img_list, lbl))
tamlate_btn=Button(frame_entry, text='Load tamplate',command= lambda title=title_enter, text=text_enter: choose_template(title, text))


#Grid block
    #Frames
frame_entry.grid(row=0, column=0, padx= 10)
frame_buttoms.grid(row=0, column=1)
    #Entry Frame
sender_label.grid(row=0, column=0, sticky='w')
sender_mail.grid(row=0, column=1, sticky='w')
tamlate_btn.grid(row=0, column=2, sticky='w')
# update_sender_btn.grid(row=0, column=2, sticky='w')
receiver_mail_label.grid(row=1, column=0, sticky='w')
receiver_mail_enter.grid(row=1, column=1, sticky='w')
load_senders_from_csv.grid(row=1, column=2, sticky='w')
read_html.grid(row=2, column=2, sticky='w')
title_label.grid(row=2, column=0, sticky='w')
title_enter.grid(row=2, column=1, sticky='w')
text_label.grid(row=3, column=0, sticky='nw')
text_enter.grid(row=3, column=1, sticky='w', columnspan=4)
file_btn.grid(row=4,column=1,sticky='w')
body_file_btn.grid(row=5,column=1,sticky='w')
file_number.grid(row=4, column=2, sticky='w')
body_file_number.grid(row=5, column=2, sticky='w')
send_btn.grid(row=6,column=1,sticky='w')
send_status_label.grid(row=6,column=2,sticky='w')

#end grid



#Main Menu
mainmenu = Menu(root_windows) 
root_windows.config(menu=mainmenu)
filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="New config file", command= lambda mailer_obj=mailer: create_config_file(mailer_obj))
filemenu.add_command(label="Choose config file", command= lambda mailer_obj=mailer: change_config_file(mailer_obj))
filemenu.add_command(label="View Journal", command=view_journal)
mainmenu.add_cascade(label="File", menu=filemenu)
settingsmenu = Menu(mainmenu, tearoff=0)
settingsmenu.add_command(label="Choose sender", command=lambda mailer_obj=mailer, lbl=sender_mail: choose_sender (mailer_obj, lbl))
settingsmenu.add_command(label="Add Sender", command= lambda mailer_obj=mailer: add_senders(mailer_obj))
settingsmenu.add_command(label="Delete sender", command= lambda mailer_obj=mailer: delete_sender(mailer_obj))
mainmenu.add_cascade(label="Settings", menu=settingsmenu)
templatemenu=Menu(mainmenu,tearoff=0)
templatemenu.add_command(label='New tamplate', command= create_temlate)
templatemenu.add_command(label='Choose tamplate', command= lambda title=title_enter, text=text_enter: choose_template(title, text))
templatemenu.add_command(label='Delete tamplate',command= delete_tamplate)
mainmenu.add_cascade(label="Tamplates", menu=templatemenu)
aboutmenu= Menu(mainmenu, tearoff=0)
aboutmenu.add_command(label='About App', command=about_app)
aboutmenu.add_command(label='About Developer',command=about_developer)
mainmenu.add_cascade(label="About", menu=aboutmenu)

#endblock menu


root_windows.mainloop()