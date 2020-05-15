#created by Tushar Kapoor(taunskhiatra@gmail.com)

import threading
from tkinter import *
from tkinter.ttk import *
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time as t
import pytube as py
import requests
from bs4 import BeautifulSoup as bs
import os
#from PIL import ImageTk, Image
window=Tk()
window.geometry('820x250')
window.title('                                                                                -------YOUTUBE DOWNLOADER------',)
Label(window,text='Search Keyword',width=22).grid(row=0,column=0)
Label(window,text='  No of scroll',width=22).grid(row=0,column=2)
Label(window,text='Destination Path',width=22).grid(row=1,column=0)
Label(window,text='',width=20).grid(row=2,column=0)
l1=Label(window,text='  Waiting ...',width=22)
l1.grid(row=1,column=2)


e1=Entry(window,width=40)
e1.grid(row=0,column=1)
e2=Entry(window,width=40)
e2.grid(row=0,column=3)
e3=Entry(window,width=40)
e3.grid(row=1,column=1)
exec_dir=os.getcwd()
exec_path=exec_dir+'\\chromedriver.exe'

Interpreter =Text(window,height=10,width=60)
Interpreter.grid(row=3,column=0,rowspan=12,columnspan=3)
progress=Progressbar(window, orient = HORIZONTAL,length = 246, mode = 'determinate')
progress.grid(row=1,column=3)

def Interpreter1(message):
    Interpreter['state']='normal'
    Interpreter.delete('1.0','end')
    Interpreter.insert('end',message)
    Interpreter['state']='disabled'

def submit():
    global Keyword_value,Scroll_Value,Destination_folder
    Keyword_value=e1.get()
    Scroll_Value=e2.get()
    Destination_folder=e3.get()
    if Keyword_value !='' and Scroll_Value !='' and Destination_folder != '':
        if os.path.isdir(Destination_folder) == True:
            Interpreter1('Your inputs are as follow:\n\nKeyword='+Keyword_value+'\nNo of Scroll='+Scroll_Value+'\nDestination='+Destination_folder)
            b2['state']='normal'
        else:
            Interpreter1('The Destination folder is incorrect. Please correct and try submitting again.')
    else:
        Interpreter1('\n\n\n Please enter all three attribute values...')

def open_youtube():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    driver=webdriver.Chrome(options=options, executable_path=exec_path)
    Base_Url='https://www.youtube.com/results?search_query='
    Search_Keyword=Keyword_value
    Search_Url=Base_Url+Search_Keyword
    try:
        driver.get(Search_Url)
        t.sleep(5)
        scroll=driver.find_element_by_xpath('//a[@class="yt-simple-endpoint style-scope ytd-toggle-button-renderer"]')
        for i in range(0,int(Scroll_Value)):
            scroll.send_keys(Keys.PAGE_DOWN)
        t.sleep(2)
        Url_Data = driver.find_elements_by_xpath('//*[@id="video-title"]')
        global Video_Links
        Video_Links = []
# Extract Video links after the Scrolling and store them in the list
        for i in Url_Data:
            Video_Links.append(i.get_attribute('href'))
        Interpreter1('Number of videos to download = '+str(len(Video_Links))+'\nIf you wish to download more please increase the number of scroll and Submit again to start over')
        b3['state']='normal'
        #Video_Links=['https://www.youtube.com/watch?v=MYhNORGrWC8','https://www.youtube.com/watch?v=MYhNORkdjGrWC8']
        #return Video_Links
        driver.quit()
    except:
        Interpreter1('\nYoutube is not reachable or extremely slow.Please try again later.')
        Interpreter['state']='disabled'
        driver.quit()

def start_download():
    skip=[]
    start_time = t.time()
#    print(Video_Links)

    #Interpreter1(msg)
    t.sleep(5)
    for i in Video_Links:
        try:
            content = requests.get(i)
            soup = bs(content.content, "html.parser")
            Pub_Data=soup.find("strong", attrs={"class": "watch-time-text"}).text
# Published Date fo the Video
            Published_On=Pub_Data.split()[2:]
            Yt = py.YouTube(i)
# Download Video in your Google drive (Backup and Sync folder),edit output path as per your system
            Video = Yt.streams.filter(file_extension='mp4').first().download(output_path=Destination_folder,filename=Yt.title,filename_prefix=Published_On[0]+'_')
        except:
            skip.append(i)
            continue
    end_time=t.time()
    exec_time=end_time-start_time

    if len(skip)==0:
        Interpreter1('Total number of videos downloaded = {} \nTotal number of videos skipped = {}\nTime elapsed for download= {} sec.'.format(str(len(Video_Links) - len(skip)), str(len(skip)), str(exec_time)))
    else:
        Interpreter1('Total number of videos downloaded = {} \nTotal number of videos skipped = {}\nTime elapsed for download = {} sec.\nSkipped Video links = {}'.format(str(len(Video_Links) - len(skip)), str(len(skip)), str(exec_time),skip))
    #print(msg)
#    print(str(len(Video_Links))+' has been downloaded')
    l1.config(text='  Completed')
    progress.stop()
    
def reset():
    e1.delete(0, END)
    e1.insert(0, "")
    e2.delete(0, END)
    e2.insert(0, "")
    e3.delete(0, END)
    e3.insert(0, "")
    Keyword_value=''
    Scroll_Value=''
    Destination_folder=''
    b2['state']='disabled'
    b3['state']='disabled'
    Interpreter1('\n\n\nPlease select new values and click Submit to start over.')
    l1.config(text='  Waiting ...')

def upload_file():
    Interpreter1('\n\nGoogle drive login page will open.\nMinimize/close the app and upload the downloaded videos on your drive.')
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    driver=webdriver.Chrome(options=options, executable_path=r'C:\Users\tauns\Downloads\chromedriver_win32\chromedriver.exe')
    try:
        driver.get(r'https://drive.google.com/drive/my-drive')
        t.sleep(5)
    except:
            Interpreter1('Site not reachable.Please try after sometime')

Interpreter.insert(END,'Welcome to Youtube Downloader !!!\n\nPlease follow the below instructions to download videos :-\n# Fill the three attributes and then click Submit button.\n# Verify the entered values on the intrepreter and click on   OpenYoutube.\n# Click on Download if you are satisfied with the number of   videos.')
Interpreter['state']='disabled'

def progress_bar():
    l1.config(text='  Downloading ...')
    Interpreter1('\n\nDownload has started .......\nPlease wait for the message to update .Depends on the total number of videos selected and their size')
    progress.start(interval=5)
    

def thread_handle():
   t1=threading.Thread(target=progress_bar)
   t2=threading.Thread(target=start_download)
   t1.start()
   t2.start()
    
#list1=Listbox(window,height=6,width=35)
#list1.grid(row=2,column=0,rowspan=6,columnspan=2)

#sb1=Scrollbar(window)
#sb1.grid(row=2,column=2,rowspan=6)

#list1.configure(yscrollcommand=sb1.set)
#sb1.configure(command=list1.yview)
b1=Button(window,text='Submit',width=32,command=submit)
b1.grid(row=3,column=3)
b2=Button(window,text='OpenYoutube',width=32,command=open_youtube)
b2.grid(row=4,column=3)
b2['state']='disabled'
b3=Button(window,text='Download',width=32,command=thread_handle)
b3.grid(row=5,column=3)
b3['state']='disabled'
b4=Button(window,text='Reset',width=32,command=reset)
b4.grid(row=6,column=3)
b5=Button(window,text='Upload',width=32,command=upload_file)
b5.grid(row=7,column=3)
b6=Button(window,text='Close',width=32,command=window.destroy)
b6.grid(row=8,column=3)


window.call('wm', 'attributes', '.', '-topmost', '1')
window.mainloop()


# In[ ]:




