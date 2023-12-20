import os
import sys
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import openai
from langchain.chat_models import ChatOpenAI
from colorama import Fore
import requests
from bs4 import BeautifulSoup
import config
import pyttsx3 

#function to fetch the courses available in GEHU
def fetchNames(url):
    Names =[]
    for i in range(1,13):
        r = requests.get(url +"page/"+ str(i)+"/?" + "level=ug")
        soup = BeautifulSoup(r.text,"html.parser")
        names = soup.find_all("h3",class_="gdlr-core-course-item-title") 
        
        for name in names:
            Names.append(name.text)    
    return Names

#function to fetch Details about GEHU
def fetchDetails():
    sec = ["","about-us","academics","admissions","placements","university-life","international","research"]
    details = ""
    for i in sec:
        r = requests.get("https://dehradun.gehu.ac.in/" + i)
        soup = BeautifulSoup(r.text,"html.parser")
        details = details + soup.text  
    return details

if os.path.isfile("Data.txt") != True:
    coursesUrl = "https://dehradun.gehu.ac.in/course-search/"
    coursesNames = fetchNames(coursesUrl)
    details = fetchDetails()

    #writing all the details in a text file.
    fp = open("Data.txt", "a", encoding="utf-8")
    for item in coursesNames:
        fp.write(item+"\n")

    gehuDetails = os.linesep.join([line for line in details.splitlines() if line])
    fp.write(gehuDetails)
    fp.close()


#setting up bot

os.environ["OPENAI_API_KEY"] = config.apiKey

#training the bot with the fetched data
loader = TextLoader('Data.txt')
index = VectorstoreIndexCreator().from_loaders([loader])

#To keep the converstion going.
engine = pyttsx3.init()
while (1):
    query = input(Fore.GREEN +"You: ")

    if("bye" in query or "goodbye" in query or "exit" in query or "close" in query):
        break
    engine.say(index.query(query))
    print(Fore.BLUE+"GEHU: ",index.query(query))
    engine.runAndWait()
