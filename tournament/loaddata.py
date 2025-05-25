import os
import re 
import numpy as np
import glob
if __name__ =="__main__":
    
    directory = "jobs/11x11-mohex-mohex-cg2010-vs-mohex-mohex-weak"
    directories = [f.name for f in os.scandir("jobs") if f.is_dir()]
    cooleumwandlung = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9,'k':10,'l':11}
    for dir in directories:
        games = glob.glob(os.path.join("jobs/"+dir,"[0-9][0-9][0-9][0-9].sgf"))
        games.sort()
        actions = []
        for path in games:
            arr = []
            with open(path,"r") as file:
                for count, line in enumerate(file):
                    arr.append(line.strip('\n')) #maybe needs to change on diffrent system idk
            #print(arr)
            pattern = r'(\d{2})x(\d{2})'
            match = re.search(pattern, arr[2])
            s1, s2 = match.groups()
            size = (s1,s2)
            win = arr[8][23]
            arr2 = np.zeros((int(s1),int(s2)),dtype = int)
            
            for x in range(count-10):
                string =arr[10+x]
                if "resign" in string:
                    #print("fertig")
                    break
                if string == '':
                    continue
                borw = string[1]
                x =string[3]
                y = string[4]
                if "swap-pieces" in string:
                    continue
                    string1 =arr[10]
                    borw2 = string[1]
                    x1 =string[3]
                    y1= string[4]
                    arr2[cooleumwandlung[x1]][int(y1)-1] = -1 if borw2 == "B" else 1

                    actions.append("swap",int(cooleumwandlung[x])*int(s1)+(int(y)-1),borw)
                    continue
                board_before = arr2.copy()
                arr2[cooleumwandlung[x]][int(y)-1] = 1 if borw == "B" else -1
                actions.append((board_before,int(cooleumwandlung[x])*int(s1)+(int(y)-1),borw))

           # print(f"{win} won")
        
        with open("actions/v4-11x11-mohex-mohex-cg2010-vs-mohex-mohex-weak.txt","a") as f:
                f.write('\n'.join('(%s,%s,%s)' % x for x in actions))
                