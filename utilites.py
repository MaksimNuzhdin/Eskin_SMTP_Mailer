import json
import math
import pathlib
import random
from time import sleep
from tkinter import messagebox
import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
from mailer_class import Mailer, Recievers, Letter, History
from tkinter import *
from tkinter.ttk import *

def choose_sender(mailer_obj, label) -> str:
    senders_w=Toplevel()
    senders=mailer_obj.read_config_dict()
    r_var = IntVar()
    
    val_radb=0
    
    for next_sender in senders:
        r1 = Radiobutton(senders_w, text=next_sender,
                 variable=r_var, value=val_radb)
        r1.grid(row=val_radb, column=0, sticky='w')
        val_radb+=1
    
    get_sender=Button(senders_w, text='Save', command= lambda s=r_var: get_sender_by_id(mailer_obj,s, senders_w ))
    get_sender.grid(row=val_radb, column=0, sticky='w')
    pass

    def get_sender_by_id(mailer_obj,num, wind ):
        num_int=num.get()
        senders=mailer_obj.read_senders_list()
        sender=senders[num_int]
        save_sender(mailer_obj,sender,label )
        wind.destroy()
        pass
    def save_sender(mailer_obj,sender, label):
        mailer_obj.save_sender(sender)
        label['text']=sender
        
        messagebox.showinfo(message=f'Current sender: {sender}')

    pass

def add_senders(mailer_obj):
    add_sender_w= Toplevel()

    new_mail_lbl=Label(add_sender_w,text='Mail: ')
    new_smpt_lbl=Label(add_sender_w,text='SMTP adress: ')
    new_password_lbl=Label(add_sender_w,text='password: ')
    new_port_lbl=Label(add_sender_w,text='Port (465): ')

    new_mail_ent=Entry(add_sender_w,)
    new_smpt_ent=Entry(add_sender_w,)
    new_smpt_ent.insert(0,'smtp.gmail.com')
    new_password_ent=Entry(add_sender_w,)
    new_port_ent=Entry(add_sender_w,)
    new_port_ent.insert(0,'465')
    
   

    new_mail_lbl.grid(row=0, column=0, sticky='w', padx=10)
    new_smpt_lbl.grid(row=1, column=0, sticky='w', padx=10)
    new_password_lbl.grid(row=2, column=0, sticky='w', padx=10)
    new_port_lbl.grid(row=3, column=0, sticky='w', padx=10)

    new_mail_ent.grid(row=0, column=1, sticky='w', padx=10)
    new_smpt_ent.grid(row=1, column=1, sticky='w', padx=10)
    new_password_ent.grid(row=2, column=1, sticky='w', padx=10)
    new_port_ent.grid(row=3, column=1, sticky='w', padx=10)
    save_btn=Button(add_sender_w, text='Save', command=lambda mail=new_mail_ent, smtp=new_smpt_ent, password=new_password_ent, port=new_port_ent:
                    get_entry_data_to_dict(mailer_obj,mail, smtp, password, port, add_sender_w))
    save_btn.grid(row=4, column=0, sticky='w', padx=10)

    def get_entry_data_to_dict(mailer_obj, new_mail, new_smtp, new_password, new_port, wind):
        mailer_obj.config_dict[new_mail.get()]={"smtp_address": new_smtp.get(),
        "password": new_password.get(),"port":new_port.get()}
        print (mailer_obj.config_dict)
        mailer_obj.save_dict(mailer_obj.config_dict)
        messagebox.showinfo(message=f'Sender {new_mail.get()} saved')
        wind.destroy()
        

    pass
def delete_sender(mailer_obj):
    senders_w=Toplevel()
    senders=mailer_obj.read_config_dict()
    r_var = IntVar()
    
    val_radb=0
    
    for next_sender in senders:
        r1 = Radiobutton(senders_w, text=next_sender,
                 variable=r_var, value=val_radb)
        r1.grid(row=val_radb, column=0, sticky='w')
        val_radb+=1
    
    get_sender=Button(senders_w, text='Delete', command= lambda s=r_var: get_sender_by_id(mailer_obj,s, senders_w ))
    get_sender.grid(row=val_radb, column=0, sticky='w')
    def get_sender_by_id(mailer_obj,num, wind ):
        num_int=num.get()
        senders=mailer_obj.read_senders_list()
        sender=senders[num_int]
        mailer_obj.delete_sender(sender )
        messagebox.showinfo(message=f'Sender {sender} deleted')
        wind.destroy()
        pass
def create_config_file(mailer_obj):
    new_file=mailer_obj.create_config_file()
    new_currrent_file=messagebox.askyesno(message=f'File {new_file} created!\n Do you want to make this file current?')
    if new_currrent_file==True: mailer_obj.change_current_file(new_file)
def change_config_file(mailer_obj):
    file_name=ask_current_file()  
    if file_name!='':
        mailer_obj.change_current_file(file_name)
        messagebox.showinfo(message=f'New current file is: {file_name}')
def ask_current_file():
    filetypes = (
        ("JSON files", "*.json"),
        ("CSV files", "*.CSV")
        )
    new_file=askopenfilename(title="Select file to open",
    filetypes=filetypes)
    return new_file
def load_recievers(mailer_obj, rec_obj):
    file_name=ask_current_file()
    ask_for_key=Toplevel()
    ask_label=Label(ask_for_key,text='Enter name of column with e-mails: ')
    ask_kew_w=Entry(ask_for_key)
    ask_kew_w.focus()
    load_btn=Button(ask_for_key,text='Load', 
                    command=lambda file= file_name, key_entry=ask_kew_w: 
                    read_csv_to_dict(ask_for_key,file, key_entry, rec_obj)
                    )
    ask_label.grid(row=0, column=0, sticky='w')
    ask_kew_w.grid(row=1, column=0, sticky='w')
    load_btn.grid(row=2, column=0, sticky='w')
    print(file_name)
def read_csv_to_dict(wind,file_name, key_w, rec_obj):
    if type(key_w)==tkinter.ttk.Entry:
        key_w=key_w.get()
        
        rec_obj.get_from_csv(file_name, key_w)
    # save_recievers(rec_obj.recievers_dict)
    messagebox.showinfo(message=f'{len(rec_obj.recievers_dict)} recievers loaded')
    wind.destroy()
    read_recievers(rec_obj)
    return (rec_obj.recievers_dict)
def read_recievers(rec_obj):

    listbox = Listbox(selectmode=SINGLE)
    for row in rec_obj.recievers_list:
            listbox.insert(END, row)
    listbox.grid(row=0,column=4, rowspan=10,padx=10, pady=5, columnspan=5, sticky=(N,S,W,E))
    listbox.bind("<Return>", lambda e, rec_obj=rec_obj: choose_person(e,rec_obj))
def choose_person(event, rec_obj):
    for i in event.widget.curselection() :
        person_list= event.widget.get(i)
    person_dict={}
    for val in person_list:

            person_dict[rec_obj.headers[person_list.index(val)]] = val
    

    create_person_wind(person_dict,rec_obj)
    pass
def create_person_wind(person_dict:dict, rec_obj):
    person_wind=Toplevel()
    person_wind.geometry('500x700')
    k_row=0
    k_column=0
    v_row=0
    v_column=1
    for k,v in person_dict.items():
        key_lab=Label(person_wind,text=f'{k}: ')
        val_lab=Label(person_wind,text=v)
        key_lab.grid(row=k_row, column=k_column, sticky='w')
        val_lab.grid(row=v_row, column=v_column, sticky='w')
        k_column+=2
        v_column+=2
        if k_column>=4:
            k_row+=1
            v_row+=1
            k_column=0
            v_column=1
    edit_btn=Button(person_wind,text="Edit person", command=lambda person=person_dict: edit_person(person_wind,person,rec_obj))
    edit_btn.grid(column=0, row=k_row+1, padx=10)
    pass
    def edit_person(person_wind,person_dict:dict, rec_obj):
        edit_person_w=Toplevel()
        edit_person_w.geometry('700x700')
        k_row=0
        k_column=0
        v_row=0
        v_column=1
        enteries=[]
        for k,v in person_dict.items():
            key_lab=Label(edit_person_w,text=f'{k}: ')
            val_ent=Entry(edit_person_w)
            enteries.append(val_ent)
            val_ent.insert(0,v)
            key_lab.grid(row=k_row, column=k_column, sticky='w')
            val_ent.grid(row=v_row, column=v_column, sticky='w')
            k_column+=2
            v_column+=2
            if k_column>=4:
                k_row+=1
                v_row+=1
                k_column=0
                v_column=1
        
        edit_btn=Button(edit_person_w,text="Save", command=lambda person_list=enteries: save_to_dict(person_wind,edit_person_w,person_list, rec_obj))
        edit_btn.grid(column=0, row=k_row+1, padx=10)
        pass
    def save_to_dict(person_wind,wind_edit,person_list:list, rec_obj):
        header_data=[]
        person_data=[]
        save_data=[]
        for key in rec_obj.headers:
            header_data.append(key)
        # save_data.append(header_data)
        
        for person in rec_obj.recievers_list:
            save_data.append(person)
        
        for i in person_list:
            person_data.append(i.get())
        id_person=int(person_data[0])-1

        
        rec_obj.recievers_list[id_person]=person_data
        read_recievers(rec_obj)
        messagebox.showinfo(message='Saved')
        wind_edit.destroy()
        person_wind.destroy()
        
        print ( rec_obj.recievers_list)
        rec_obj.recievers_dict={}
        rec_obj.read_to_dict(rec_obj.mail_kw)
        # for rec in rec_obj.recievers_list:
        #     pers_dict={}
        #     for k in rec_obj.headers
        print(rec_obj.recievers_dict)

        pass
        

    pass

# def save_recievers(rec_dict:dict):
#     recievers_journal=pathlib.Path(__file__).parent.joinpath('recievers.json')
#     with open (recievers_journal, 'w') as rj: json.dump(rec_dict, rj)

def add_file(file_list, lbl):
        filetypes = (
        ("Text files", "*.txt"),
        ("CSV files", "*.csv"),
        ("JSON files", "*.json"),
        ("JPEG files", "*.jpeg"),
        ("PNG files", "*.png"),
        ('all files', '*.*')
        )
        file_name = askopenfilename(
        title="Select file to for add",
        filetypes=filetypes
        )
        if file_name!='':
            file_list.append(file_name)
        lbl['text']= f'Selected {len(file_list)} files'
        print (file_list)
        pass
def create_temlate():
    new_tamplate=Toplevel()
    title_label=Label(new_tamplate, text='Create new tamplate')
    name_tmp_lbl=Label(new_tamplate, text= 'Name tamplate')
    name_tmp_entry=Entry(new_tamplate)
    title_tmp=Label(new_tamplate, text='Title')
    title_entry=Entry(new_tamplate)
    file_btn=Button(new_tamplate, text= 'Read file',command= lambda temp_name=name_tmp_entry, title=title_entry: read_file(new_tamplate,temp_name,title))
    text_btn=Button(new_tamplate, text='Write text',command= lambda temp_name=name_tmp_entry, title=title_entry: write_text(new_tamplate,temp_name,title))
    


    title_label.grid(row=0, column=0, columnspan=2, sticky='ns', padx=10, pady=20)
    name_tmp_lbl.grid(row=1, column=0, padx=10, sticky='w')
    name_tmp_entry.grid(row=1, column=1, padx=10, sticky='w')
    title_tmp.grid(row=2, column=0, padx=10, sticky='w')
    title_entry.grid(row=2, column=1, padx=10, sticky='w')
    file_btn.grid(row=3, column=0, padx=10, sticky='w')
    text_btn.grid(row=3, column=1, padx=10, sticky='w')
    def read_file(new_tamplate,name_tmp_entry, title_entry,):
        temp_name=name_tmp_entry.get()
        title=title_entry.get()
        filetypes = (
                    ("html files", "*.html"),
                    ("txt files", "*.txt")
                    )
        file=askopenfilename(title="Select file to open",
                filetypes=filetypes)
        with open (file, 'r') as f: text=f.read()
        create_temp_dict_html(new_tamplate,temp_name, title, file)
    def write_text(window, name_tmp_entry, title_entry):
        temp_name=name_tmp_entry.get()
        title=title_entry.get()
        text_entry=Text(window)
        save_btn=Button(window, text='Save', command=lambda :create_temp_dict(new_tamplate,temp_name, title, text_entry))
        text_entry.grid(row=4, column=0, padx=10, sticky='w', columnspan=2)
        save_btn.grid(row=5, column=0, padx=10, sticky='w')


    def create_temp_dict_html(new_tamplate,*args):
        name=args[0]
        title=args[1]
        text=args[2]

        if type(args[2]) != str:
            text=args[2]
            text=text.get("1.0",'end')
        args

        temp_dict={name:{'Title':title, 'Way':text}}
        save_temp(new_tamplate,temp_dict)
        pass
    def create_temp_dict(new_tamplate,*args):
        name=args[0]
        title=args[1]
        text=args[2]
        filetypes = (
                    ("html files", "*.html"),
                    ("txt files", "*.txt")
                    )
        way=asksaveasfilename(title='Save template', filetypes=filetypes)
        with open (way, 'w')as w: w.write(text.get(1.0, END))
        if type(args[2]) != str:
            text=args[2]
            text=text.get("1.0",'end')
        args

        temp_dict={name:{'Title':title, 'Way':way}}
        save_temp(new_tamplate,temp_dict)
    def save_temp(new_tamplate,temp_dict:dict):
        templates_file=choose_template_config()
        
        with open (templates_file, 'r') as tf: file_dict=json.load(tf)
        for k,v in temp_dict.items():
            file_dict[k]=v
        with open (templates_file, 'w') as tf: file_dict=json.dump(file_dict,tf)
        messagebox.showinfo(message=f'Tamplate saved')
        new_tamplate.destroy()
def delete_tamplate():
    del_tamplate=Toplevel()
    templates_file=choose_template_config()    
    with open (templates_file, 'r') as tf: file_dict=json.load(tf)
    r_var = IntVar()
    
    val_radb=0
    
    for next_temp in file_dict:
        r1 = Radiobutton(del_tamplate, text=next_temp,
                 variable=r_var, value=val_radb)
        r1.grid(row=val_radb, column=0, sticky='w')
        val_radb+=1
    
    get_sender=Button(del_tamplate, text='Delete', command= lambda s=r_var: get_temp_by_id(s, del_tamplate, file_dict ))
    get_sender.grid(row=val_radb, column=0, sticky='w')
    def get_temp_by_id(num, window,file_dict):
        num_int=num.get()
        templates=list(file_dict.keys())
        template=templates[num_int]
        del_temp(file_dict, template, window)
    def del_temp(file_dict,tamplate, window):
        del file_dict[tamplate]
        
        messagebox.showinfo(message=f'Tamplate {tamplate} deleted')
        tamplates_file=choose_template_config()     
        with open (tamplates_file, 'w') as tf: json.dump(file_dict,tf)
        window.destroy()
def choose_template_config():
    templates_file=pathlib.Path(__file__).parent.joinpath('temlates_file.json') 
    return templates_file

def choose_template(title_e, text_e):
    ch_tamplate=Toplevel()
    templates_file=choose_template_config()    
    with open (templates_file, 'r') as tf: file_dict=json.load(tf)
    r_var = IntVar()
    
    val_radb=0
    
    for next_temp in file_dict:
        r1 = Radiobutton(ch_tamplate, text=next_temp,
                 variable=r_var, value=val_radb)
        r1.grid(row=val_radb, column=0, sticky='w')
        val_radb+=1
    
    get_sender=Button(ch_tamplate, text='Choose', command= lambda s=r_var: get_temp_by_id(s, ch_tamplate, file_dict ))
    get_sender.grid(row=val_radb, column=0, sticky='w')
    def get_temp_by_id(num, window,file_dict):
        num_int=num.get()
        templates=list(file_dict.keys())
        template=templates[num_int]
        get_temp_text(template)
        window.destroy()
    def get_temp_text(template):
        config_file=choose_template_config()
        with open (config_file, 'r') as cf: config_dict=json.load(cf)
        result_dict=config_dict[template]
        way=result_dict['Way']
        title=result_dict['Title']
        with open (way, 'r')as file: text=file.read()
        insert_template (title_e, text_e, title, text)
        pass
    def insert_template(title_e, text_e, title, text):
        title_e.insert(0,title)
        text_e.insert(1.0,text, END)
        pass
    pass
        
def sending(rec_obj,current_sender, recievers, read_html, title_enter, text_enter, file_list,body_img_list, lbl):
    lbl['text']='Sending'
    recievers=recievers.get()
    recievers=recievers.strip().split(',')
    reading_html=read_html.get()
    title_get=title_enter.get()
    text_get=text_enter.get(1.0, END)
    try: #check if we have object Recievers class
        recievers_dictionary=rec_obj.recievers_dict
    except AttributeError: recievers_dictionary={}
    lbl['text']='Sending'
    # print(recievers_dictionary,current_sender,recievers, reading_html, title_get, text_get, file_list)
    new_letter=Letter(sender=current_sender, recievers_list=recievers, recievers_dict=recievers_dictionary, 
                      read_html=reading_html, title=title_get, text=text_get, files=file_list,body_img_list=body_img_list)
    if recievers[0] !='':
        print (type(recievers[0]), recievers[0], len(recievers))
        for reciever in recievers:
            print(f'sendeing to {reciever}')
            sleep(random.randint(1,5))
            new_letter.send(reciever, title=new_letter.title, text=new_letter.text)
            new_letter.save_to_journal(current_sender, reciever,title=new_letter.title)
    for email, rec in recievers_dictionary.items():
        new_text=new_letter.text
        new_title=new_letter.title
        for k in rec:
            if f'!{k}!' in new_letter.text:
                
                new_text=new_text.replace(f'!{k}!', rec[k])
                new_title=new_title.replace(f'!{k}!', rec[k])
        print(f'sendeing to {email}')
        sleep(random.randint(1,5))        
        new_letter.send(email, title=new_title, text=new_text)
        new_letter.save_to_journal(current_sender, email,title=new_title)
    lbl['text']='All letters sended'
    messagebox.showinfo(message='Letters sended')

    pass
def about_developer():
    abdev=Toplevel()
    text='''
    Hi there! My name is Max and I'am a Python Developer
    My web-site: https://nuzhdinmaksim.com/
    More of my projects at https://codecanyon.net/
    User: Nuzhdin05
    '''
    ablbl=Label(abdev,text='About me')
    abtext=Text(abdev)
    abtext.insert(1.0,text, END)
    abtext.grid(row=1, column=0) 
    ablbl.grid(row=0, column=0, sticky='ns') 
def about_app():
    abapp=Toplevel()
    text='''
Eskin SMTP Mailer is a multifunctional program for mass mailing personalized emails.

Functions and benefits:

Ability to use keywords to insert the parameters of each recipient (first name, last name, etc.)
Ability to read HTML tags
Attaching files
Ability to embed images in the body of the email
Ability to work with a large number of senders and with different SMTP servers
Saving information about each sent message
Ability to view the history of sent messages in the application
A wide range of functions for working with sender configuration files (create, modify, delete)
Ability to create, edit and delete senders list
Ability to use templates
Ability to create, modify and delete templates'''
    ablbl=Label(abapp,text='About me')
    abtext=Text(abapp)
    abtext.insert(1.0,text, END)
    abtext.grid(row=1, column=0) 
    ablbl.grid(row=0, column=0, sticky='ns')       
def view_journal():
    def create_person_wind(person_dict:dict, ):
        person_wind=Toplevel()
        person_wind.geometry('500x300')
        k_row=0
        k_column=0
        v_row=0
        v_column=1
        for k,v in person_dict.items():
            key_lab=Label(person_wind,text=f'{k}: ')
            val_lab=Label(person_wind,text=v)
            key_lab.grid(row=k_row, column=k_column, sticky='w')
            val_lab.grid(row=v_row, column=v_column, sticky='w')
            k_column+=2
            v_column+=2
            if k_column>=4:
                k_row+=1
                v_row+=1
                k_column=0
                v_column=1
    def choose_person(event):
        for i in event.widget.curselection() :
            person_list= event.widget.get(i)
        person_dict={}
        for val in person_list:

                person_dict[history_obj.keys_list[person_list.index(val)]] = val
        

        create_person_wind(person_dict)
    def on_select_function(event):
            for i in event.widget.curselection() :
                print (event.widget.get(i))
            pass
    def find_by_key(w,key,word,row_grid):
        word=word.get()
        with open (history_obj.history_file, 'r') as hf:
            keys=hf.readline()
            key_list=keys.strip().split(',')
            rows=hf.readlines()
        rows_list=[]
        listbox_list=[]
        for row in rows:
            row=row.strip().split(',')
            rows_list.append(row)
        for row_l in rows_list:
            if row_l[key]==word:
                listbox_list.append(row_l)
        listbox = Listbox(history_w,selectmode=SINGLE)
        listbox.bind("<<ListboxSelect>>", 
                    on_select_function)
        
        listbox.bind("<Return>",  choose_person)
        listbox.grid(column=0, row=krow+1, padx=10, sticky=(W,E,N,S),columnspan=6)
        history_w.grid_rowconfigure(krow+1, weight=1)
        history_w.grid_columnconfigure(5, weight=1)

        for row in listbox_list:
        
            listbox.insert(END, row)


        

        pass
    history_obj=History()
    history_w=Toplevel()




    history_w.geometry('600x400')
    find_label=Label(history_w, text='Find by:')
    find_key_val_l=Label(history_w, text='Key value: ')
    find_key_val_e=Entry(history_w)
    find_label.grid(row=0, column=0, columnspan=4)
    find_key_val_l.grid(row=1,column=0, sticky='e')
    find_key_val_e.grid(row=1, column=1)

    
    krow=2
    kcol=0
    for next_key in history_obj.keys_list:
        key=Button(history_w, text=next_key, 
                   command=lambda window=history_w, k=history_obj.keys_list.index(next_key), val=find_key_val_e, lbrow=krow+1, : find_by_key(window,k, val, lbrow)
                # 
                )
        key.grid(row=krow, column=kcol, sticky=(W,E), padx=10)
        kcol+=1
        if kcol>3:
            krow+=1
            kcol=0
    listbox = Listbox(history_w,selectmode=SINGLE)
    listbox.bind("<<ListboxSelect>>", 
                on_select_function)
    
    listbox.bind("<Return>",  choose_person)
    # Label(history_w, text = "Test test").grid(column=5, row=2)
    listbox.grid(column=0, row=krow+1, padx=10, sticky=(W,E,N,S),columnspan=6)
    history_w.grid_rowconfigure(krow+1, weight=1)
    history_w.grid_columnconfigure(5, weight=1)
    print(krow+1)
    # scrollbar.config(command= listbox.yview)
    for row in history_obj.lines:
        
        listbox.insert(END, row)
        
    
    pass

