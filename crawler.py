from typing import Counter
import requests
from bs4 import BeautifulSoup
import re
import collections


def hist_section(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    #id="History" = id="Corporate-affairs"

    #HTML Source Code looks like:
    #
    #<h2>
    #   <span id="History">History</span>
    #</h2>
    #

    temp = ((soup.find("span", {"id": "History"})).parent).parent #<span id="History">History</span>, then out 2 parents so iteration works (single .parent does not contain any of the body text)

    history = (soup.find("span", {"id": "History"})).parent #<h2><span id="History">History</span></h2>
    corporate = (soup.find("span", {"id": "Corporate_affairs"})).parent #<h2><span id="Corporate_affairs">Corporate Affairs</span></h2>
    
    # print(start, end)   #debugging
    hist_sec = []
    
    seen_hist = False
    seen_corp = False

    for child in temp.children:
        if child == history:
            seen_hist = True
            continue
        if child == corporate:
            seen_corp = True
        if seen_hist == True and seen_corp == False: # here I am within the History section
            hist_sec.append(str(child))
        elif seen_corp == True:
            # print("exiting")  #debugging
            break

    return hist_sec
    # for item in hist_sec:    #debugging
    #     print(item)
    #     print("-------------")
    

def clean_and_count(raw_history, possesive): #this function is a bit messy and could probably be better. cleaning up text is challenging
    word_counts = Counter()
    temp = ""
    for item in raw_history:
        temp = (re.sub('<[^>]+>', '', item))  #removes all html tags and elements by removing little side carrots
        temp = (re.sub('\[[^\]]+\]', '', temp))  #removes square brackets and everything inbetween
        if possesive:
            temp = temp.replace("\'s", "")  #remove possesive, possesive version of a word counts toward its count
        temp = temp.replace('.', '')
        temp = temp.replace(',', '')
        temp = temp.replace('-', '')  
        temp = temp.replace('\"', '')
        temp = temp.replace('\' ', '')  # ^^^removing punctuation
        temp = temp.strip()  #newlines
        temp_arr = temp.split()
        for word in temp_arr:
            #print(word)
            word_counts[word.lower()] += 1
    #print(word_counts)
    return(word_counts)


def user_input():
    print("Hi! This mini web crawler grabs all the text from the Microsoft wikipedia page History section.")
    num_words = input("How many words would you like to see the count of (leave blank to see 10 words): ")
    if num_words == "":
        num_words = 10
    num_words = int(num_words)
    exclude = input("Are there any words you'd like to leave out? (type each word separated by a space, or hit enter to include all words): ")
    possesive = input("Should I count possesive versions of words as non-possesive? For instance, should 'Microsoft's' count as 'Microsoft'? (y/n): ")
    if possesive == "y":
        possesive = True
    elif possesive == "n":
        possesive = False
    else:
        exit()
    return(num_words, exclude, possesive)


    
def display(word_counts, num_words, exclude):
    exclude = exclude.split() 
    for word in exclude:
        del word_counts[word] #delete the excluded words from the counter
    print(word_counts.most_common(num_words)) #.most_common is a (pretty sweet) function of counter
    



def main():
    url = "https://en.wikipedia.org/wiki/Microsoft#History"
    html_text = requests.get(url).text

    raw_history = hist_section(html_text)

    num_words, exclude, possesive = user_input()
    
    word_counts = clean_and_count(raw_history, possesive)

    display(word_counts, num_words, exclude)




if __name__ == "__main__":
    main()

    

