from bs4 import BeautifulSoup, SoupStrainer
from html.parser import *
import http.client
import urllib.request
from urllib.request import urlopen, Request

#used for later y/n questions
yes = ['y','ye','yes']
no = ['n','no']

  
def getImages():
    #choosing the engine
    choice = ""
    while choice not in ["g","b","y","all"]:
        choice = input("Which engine do you want to use? (g/b/y/all) ")
    if choice == "g":
        search_engine = "Google"
    if choice == "b":
        search_engine = "Bing"
    if choice == "y":
        search_engine = "Yahoo"

    #asking for term
    search_term = str(input(search_engine+' Image Search: ')).replace(" ", "+")

    #asking for maximum number of links
    link_limit = int(input("Enter link limit: "))

    #save links to text file question
    save_links_yn = str(input("Write links to a file? (y/n) ")).lower()
    if save_links_yn in yes:
        filename_links = str(input("How should the text file be named? "))

    #save picturse as, question
    download_pictures_yn = str(input("Download pictures? (y/n) ")).lower()
    if download_pictures_yn in yes:
        filename_pictures = str(input("How should the image files be named? "))

    save_error_links_yn = str(input("Save links causing errors? (y/n) ")).lower()
    if save_error_links_yn in yes:
        filename_errors = str(input("How should the text file be named? "))

    #setting search url according to engine choice
    if choice == "g":
        search_url = 'https://www.google.ch/search?site=webhp&tbm=isch&source=hp&q='+search_term+'&oq='+search_term
    if choice == "b":
        search_url = 'http://www.bing.com/images/search?q='+search_term
    if choice == "y":
        pass

    #just checking the url for mistakes
    print("Scraping following URL:\n"+search_url+"\n")

    #adding newest chrome header to fool engines and defining request
    req = Request(search_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'})
    soup = BeautifulSoup(urllib.request.urlopen(req), 'html.parser')

    #for reverse engineering purposes only
    open('this-is-soup.html', 'w').write(str(soup.encode("utf-8")))

    #finding tags containing links according to choice of engine
    if choice == "g":
        link_containers = soup.findAll("div", { "class" : "rg_meta" })
    if choice == "b":
        link_containers = soup.findAll("a", attrs={"m": True})
    if choice == "y":
        pass

    #extracting every link container after setting counters to zero
    link_counter = 0
    exception_counter = 0
    
    for link_container in link_containers:
        try:
            #stripping link container string of unnecessary characters according to engine choice
            if choice == "g":
                link_container = str(link_container).partition('"ou":"')[-1]
                link_container = link_container.rpartition('","ow"')[0]
            if choice == "b":
                link_container = str(link_container).partition('",imgurl:"')[-1]
                link_container = link_container.rpartition('",tid:"')[0]
            if choice == "y":
                pass
            link_container = str(link_container)

            #writing links to file if wanted
            if save_links_yn in yes:
                open(filename_links+'.txt', 'a').write(link_container+"\n")

            #downloading the images if wanted
            if download_pictures_yn in yes:
                urllib.request.urlretrieve(link_container, filename_pictures+str(link_counter+1)+".jpg")

            #if counter's limit is reached, stop
            link_counter += 1
            if link_counter == link_limit:
                break
        except IOError:
            print("Error with:",link_container)
            exception_counter += 1
            link_counter -= 1

            #write error links to file if wanted
            if save_error_links_yn in yes:
                open(filename_errors+'.txt', 'a').write(link_container+"\n")

    print("\nlinks found:", link_counter)
    print("\nexceptions thrown:", exception_counter)


#looped program until quit
while True:
    getImages()
    #want to quit?
    if input("Press <Enter> to continue, n to quit: ").lower() in no:
        break






#everything ran smoothly, more or less
input("\n\n--------------------\n   END OF PROGRAM") 

    
