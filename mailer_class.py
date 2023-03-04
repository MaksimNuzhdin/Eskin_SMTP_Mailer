import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import pathlib
import smtplib
import ssl
from tkinter import END, SINGLE, Listbox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from datetime import datetime



class Mailer:

    def __init__(self, config_journal) -> None:
        self.journal_config_file=config_journal
        self.current_sender_file=pathlib.Path(__file__).parent.joinpath('current_sender.txt')
        self.senders=[]
        self.config_file=pathlib.Path(__file__).parent.joinpath('main_config.json')
        with open (self.journal_config_file, 'w') as j: 
            j.write(str(self.config_file))
        try:
            self.read_config_dict()
        except FileNotFoundError: 
            filetypes = (
                ("JSON files", "*.json"),
                )
            new_file=askopenfilename(title="Select file to open",
            filetypes=filetypes)
            with open(self.journal_config_file, 'w') as jcf: jcf.write(new_file)
            self.read_config_dict()
        for next_sender in self.config_dict:
            self.senders.append(next_sender)
        
        pass
    def save_sender(self, sender):
        with open (self.current_sender_file, 'w') as csf: csf.write(sender)
        pass
    def read_sender(self):
        with open (self.current_sender_file, 'r') as csf: 
            sender=csf.read()
            return sender
    def save_dict(self, data:dict):
        with open (self.config_file, 'w')as cw: json.dump(data, cw)

        pass
    def read_config_dict(self):
        with open (self.config_file, 'r')as cf:
            self.config_dict=json.load(cf)
        return self.config_dict
    def read_senders_list(self):
        senders_d=self.read_config_dict()
        senders_list=list(senders_d.keys())
        return senders_list
    def delete_sender(self, sender):
        old_dict=self.read_config_dict()
        del old_dict[sender]
        self.save_dict(old_dict)
        pass
    def create_config_file(self):
        filetypes = (
        ("JSON Files", "*.json"),
        )

        file_name = asksaveasfilename(
        title="Create file",
        filetypes=filetypes
        )
        new_file_dict={"Test Mail": {
        "smtp_address": "test SMTP",
        "password": "TestPassword",
        "port":"TestPort"
        }}
        self.change_current_file(file_name)
        self.save_dict(new_file_dict)
        return file_name
    def change_current_file(self, file_name):
        with open(self.journal_config_file, 'w') as jcf: jcf.write(file_name)
        with open (self.journal_config_file, 'r') as j: self.config_file=j.read()
        pass
    

class Recievers:
    
    def get_from_csv(self, file, key_w):
        self.mail_kw=key_w 
        self.read_to_list(file)
        self.read_to_dict(key_w)
        

        
        pass
    def read_to_list(self, file):
        with open (file,'r') as f:
            self.headers=f.readline().strip().split(',')
            recievers=f.readlines()
        self.recievers_list=[]
        for next_reciever in recievers:
            self.recievers_list.append(next_reciever.strip().split(','))
        return self.recievers_list
    def read_to_dict(self, key_w):
        self.recievers_dict={}
        for reciever in self.recievers_list:
            rec_dict={}
            key_ind=0
            for val in reciever:
                
                rec_dict[self.headers[key_ind]]=val
                key_ind+=1

            
            # print( self.headers, key_w)
            # print(self.headers.index(key_w))
            # print(reciever[self.headers.index(key_w)])
            self.recievers_dict[reciever[self.headers.index(key_w)]]=rec_dict
        return self.recievers_dict
    
    pass

class Letter:
    def __init__(self, sender, recievers_list: list, recievers_dict: dict, read_html:bool, title, text, files:list, body_img_list:list) -> None:
        self.sender=sender
        self.recievers_list=recievers_list
        self.recievers_dict=recievers_dict
        self.read_html=read_html
        self.title=title
        self.text=text
        self.files=files
        self.body_img_list=body_img_list
        
        pass
    def test_print(self):
        print( self.sender,self.recievers_list,self.recievers_dict,self.read_html,self.title, self.text, self.files,self.body_img_list, sep='\n')
        pass
    def get_personal_title_and_text(self):
        pass
    def send(self, reciever, title, text):
        journal_sender_file=pathlib.Path(__file__).parent.joinpath('current_file.txt')
        with open (journal_sender_file, 'r') as j: journal=j.read()
        with open (journal, 'r') as j: config_dict=json.load(j)
        message = MIMEMultipart('alternative')
        message['Subject'] = title
        message['From'] = self.sender
        message['To'] = reciever
        if self.read_html==False:
            part1 = MIMEText(text, 'plain')
            message.attach(part1)
        elif self.read_html==True:
            part2 = MIMEText(text, 'html')
            message.attach(part2)
        for file in self.files:
            with open(file, 'rb') as f: attachment1 = f.read()
            attach_part_1 = MIMEBase('application', 'octet-stream')
            attach_part_1.set_payload(attachment1)
            encoders.encode_base64(attach_part_1)
            # headers for attachment
            attach_part_1.add_header(
                'Content-Disposition',
                f'attachment; filename={pathlib.PosixPath(file).name}'
            )
            message.attach(attach_part_1)
        for body_file in self.body_img_list:
            with open(body_file, 'rb') as f: attachment2 = f.read()
            attach_part_2 = MIMEBase('application', 'octet-stream')
            attach_part_2.set_payload(attachment2)
            encoders.encode_base64(attach_part_2)
            # headers for attachment
            attach_part_2.add_header(
                'Content-Disposition',
                f'attachment; filename={pathlib.PosixPath(body_file).name}'
            )
            attach_part_2.add_header(
                'Content-ID', f'<my_img{self.body_img_list.index(body_file)+1}>'
            )
            message.attach(attach_part_2)
        context = ssl._create_unverified_context()
        try:

            with smtplib.SMTP_SSL(config_dict[self.sender]['smtp_address'], config_dict[self.sender]['port'], context=context) as server:
                server.login(self.sender, config_dict[self.sender]['password'])
                print(server.sendmail(self.sender, [reciever], message.as_string()))
        except Exception as e:
            print(f'Something wrong \n Error: {e}')

        
        pass
    def save_to_journal(self,sender,reciever, title):
        history_file=pathlib.Path(__file__).parent.joinpath('history.csv')
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        current_time=f'{current_time.hour}:{current_time.minute}'
        with open (history_file, 'r') as hf:
            lines=hf.readlines()
        write_data=f'{len(lines)},{current_date},{current_time},{sender},{reciever}, {title}'
        with open (history_file, 'a') as hf:
            hf.write(f'\n{write_data}')
        pass
class History():
    def __init__(self) -> None:
        self.history_file=pathlib.Path(__file__).parent.joinpath('history.csv')
        with open (self.history_file, 'r') as hf:
            keys_list=hf.readline()
            self.keys_list=keys_list.strip().split(',')
            lines=hf.readlines()
            self.lines=[]

            for row in lines:
                self.lines.append(row.strip().split(',')) 
        pass
    def view_journal():
        pass
    
    def readToDict(self, key_word):
        key_list=[]
        persons_list=[]
        result_dict={}
        with open (self.history_file) as hf:
            headers = hf.readline()
            persons = hf.readlines()
        for key in headers.strip().split(','):
            key_list.append(key)
        for next_person in persons:
            persons_list.append(next_person.strip().split(','))
        for person in persons_list:
            person_dict = {}
            for val in person:
                person_dict[key_list[person.index(val)]] = val           
            # print(person_dict[key_word])
            result_dict[person_dict[key_word]]=person_dict

        
        

    pass
