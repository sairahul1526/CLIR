import threading
import math
import csv
threadLock=threading.Lock()
class OThread(threading.Thread):
    def __init__(self,i,thread_name,threadLock,parent_thread):
        threading.Thread.__init__(self)
        self.name=thread_name
        self.threadLock=threadLock
        self.parent=parent_thread
        self.thread_id=i
        self.thread_name=thread_name

    def run(self):
        
        while(self.parent.stopFlag==False):
            processed_sentences=self.parent.processed_sentences
            next_batch_upper_bound=processed_sentences+5000
            if(processed_sentences+5000>len(self.parent.english_sentences)):
                next_batch_upper_bound=len(self.parent.english_sentences)-1
                self.parent.stopFlag=True           
            self.parent.processed_sentences=next_batch_upper_bound
            print("%s started working on the chunck from %s to %s"%(self.thread_id,processed_sentences,next_batch_upper_bound))
            steps = 0
            t=self.parent.t
            
            while steps < 5:
                steps += 1
                E=None
                F=None
                for i in range(processed_sentences,next_batch_upper_bound):
                    E = self.parent.english_sentences[i].split(" ")
                    F = self.parent.french_sentences[i].split(" ")
                    count={}
                    total={}
                    for e in E:
                        count[e] = {}
                        for f in F:
                            count[e][f] = 0
                            total[f] = 0

                    s_total = {}
                    for e in E:
                        s_total[e] = 0
                        for f in F:
                            if e in t:
                                if f in t[e]:
                                    s_total[e] += t[e][f]
                                else:
                                    t[e][f] = 1.0/self.parent.no_english_words
                                    s_total[e] += t[e][f]
                            else:
                                t[e] = {}
                                t[e][f] = 1.0/self.parent.no_english_words
                                s_total[e] += t[e][f]

                    for e in E:
                        for f in F:
                            if s_total[e] != 0:
                                count[e][f] += t[e][f]/s_total[e]
                                total[f] += t[e][f]/s_total[e]

                    for e in E:
                        for f in F:
                            if total[f] != 0:
                                t[e][f] = count[e][f]/total[f]
                                # print(str(t[e][f]) + " : " + e + " - " + f)
            self.parent.t=t
class Demo():
    def __init__(self,english_words,french_words,english_sentences,french_sentences):
        self.count={}
        self.total={}
        self.no_english_words=english_words
        self.no_french_words=french_words
        self.english_sentences=english_sentences
        self.french_sentences=french_sentences
        self.processed_sentences=0
        self.stopFlag=False
        self.t={}
def main():
    # my code here
    english_file = open("english.txt","r",encoding='utf-8', errors='ignore').read()
    french_file = open("french.txt","r",encoding='utf-8', errors='ignore').read()

    english_file = english_file.lower()
    french_file = french_file.lower()

    punctuations = '''!|()-[]{};:"\,<>./?@#$%^&*_~'''
    for char in punctuations:
        # print(char)
        english_file = english_file.replace(char, "")
        french_file = french_file.replace(char, "")

    english_file = english_file.splitlines()
    french_file = french_file.splitlines()

    # minimum_iter = int(2*len(english_sentences)/5)
    # maximum_iter = int(3*len(english_sentences)/5)

    iteration = 0
    # minimum = 400*iteration + minimum_iter
    # maximum = min(400*(iteration+1),maximum_iter) + minimum_iter
    english_words = []
    french_words = []

    for i in range(len(english_file)):
        english_words.extend(english_file[i].split(" "))
        french_words.extend(french_file[i].split(" "))

    english_words = list(set(english_words))
    french_words = list(set(french_words))

    no_english_words = len(english_words)
    no_french_words = len(french_words)
    english_words=None
    french_words=None
    demo=Demo(no_english_words,no_french_words,english_file,french_file)

    threads=[]
    for i in range(10):
        thread=OThread("Thread:"+str(i),i,threadLock,demo)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    with open("frenchToEnglish.csv", 'a') as outcsv:
        #configure writer to write standard csv file
        writer = csv.writer(outcsv, delimiter=',', lineterminator='\n')
        for e in demo.t:
            for f in demo.t[e]:
                if round(demo.t[e][f],4) > 0.8:
                    #Write item to outcsv
                    writer.writerow([str(demo.t[e][f]),e,f.encode("utf-8").decode('utf-8')])

if __name__ == "__main__":
    main()
