#importing libraries
from __future__ import division
import glob, os
import collections
import math
import operator
from collections import OrderedDict
import numpy as np
import scipy
import copy
import string



#Function for generating ngrams
def ngrams(data, n):

  #Creating a list to store n grams
  lst=list()

  #Intially splitting file using spaces
  data = data.split()

  #to remove bigram having START
  data.pop(0)

  #Ordered List
  ordered_list= []

  #Making ngrams
  for i in range(len(data)-n+1):
     #Apending data in ordered_list
     ordered_list = ' '.join(data[i:i+n])

     #Apending data in normal list
     lst.append(ordered_list)

  #Returning list
  return lst

#Method used to genrate binary strings
def updatestrings(C, c1, c2, strings):
    #earlier cluster on the list gets the code 0
    for s in C[c1]:
        if s in strings.keys():
            strings[s]= "0" + strings[s]
        else:
            strings[s]= "0"

    #the later cluster gets the code 1
    for s in C[c2]:
        if s in strings.keys():
            strings[s]= "1" + strings[s]
        else:
            strings[s]= "1"

    #returning modofied dict
    return strings

#deleting bigram count of clusters
def deletebigramcount(C, c1 , c2, B, W):
    #updating bigram counts of clustors
    for key in list(B.keys()):

        #splitting key
        x = key.split()[0]
        y = key.split()[1]

        #checking the clustor whoose count is being updated
        if ( x == C[c1][0]):
                akey = C[c2][0] + " " + y
                B[key] = B[key] + B[akey]


        if ( y == C[c1][0]):
                bkey = x + " " + C[c2][0]
                B[key] = B[key] + B[bkey]

#deleting weight count of clusters
def deleteweightcount(C, c1 , c2, P, B, W):
    for key in W.keys():
        #splitting key
        x = key.split()[0]
        y = key.split()[1]

        #checking the clustor whoose quality is being updated
        if (x == C[c1][0]):

            #if bigram count of clustors is 0 then value is 0
            if(B[key] == 0):
                value1 = 0

            #calculating quality value
            else:
                value1 =  (B[key]/n) * (math.log((B[key] * n)/(P[y]*P[x])))

            rev_key = y + " " + x

            #if bigram count of rev key or clustors is 0 then value is 0
            if(B[rev_key] == 0):
                value2 =0

            #calculating quality value
            else:
                value2 =  (B[rev_key]/n)*(math.log( (B[rev_key] * n)/(P[y]*P[x])))

            #assigning the quality value
            W[key] = value1 + value2
            W[rev_key] = value1 + value2

#deleting difference in quality count of two settings
def deletequalitycount(C, c1 , c2, P, B, W, L):
    y = 0
    cwords = C[c1][0]
    while (y != len(C)):
        key = C[y][0] + " " + cwords
        rev_key = cwords + " " +  C[y][0]
        z = 0
        while (z != len(C)):
            value1 = 0
            value2 = 0
            key1 = cwords+ " " + C[z][0]
            key2 = C[y][0]+ " " + C[z][0]

            if B[key1]+B[key2]== 0:
                value1 = 0
            else:
                value1 =  ((B[key1]+B[key2])/n) * (math.log(((B[key1]+B[key2]) * n)/((P[cwords]+P[C[y][0]]) * P[C[z][0]])))

            rev_key1 = C[z][0]+ " " + C[y][0]
            rev_key2 = C[z][0]+ " " + cwords

            if B[rev_key1]+B[rev_key2] == 0:
                value2 = 0

            else:
                value2 =  ((B[rev_key1]+B[rev_key2])/n) *  (math.log(((B[rev_key1]+B[rev_key2]) * n)/((P[cwords]+P[C[y][0]]) * P[C[z][0]])))

            #updating the fifference
            if key in L.keys() and (key1 in W.keys() and key2 in W.keys()):
                L[key] = L[key] + value1 + value2 - W[key1] - W[key2]
            elif rev_key in L.keys() and (key1 in W.keys() and key2 in W.keys()):
                L[rev_key] =  L[rev_key] + value1 + value2 - W[key1] - W[key2]

            z = z + 1
        y = y + 1

#method to delete a clustor if it is to be merged
def deleteclustors(C, c1 , c2, P, B, W, L):

    # merging the clusters
    C[c1].extend(C[c2])

    #updating unigram counts
    P[C[c1][0]] = P[C[c1][0]] + P[C[c2][0]]

    deletebigramcount(C,c1,c2,B,W)

    #deleting bigram and quality record of merged clustor
    for key in list(B.keys()):
        x = key.split()[0]
        y = key.split()[1]
        if (x == C[c2][0] or y == C[c2][0]):
            B.pop(key,None)
            W.pop(key,None)
            L.pop(key,None)

    #deleting unigram record of merged clustor
    del P[C[c2][0]]

    #deleting merged clustor
    del C[c2]

    deleteweightcount(C, c1 , c2, P, B, W)
    deletequalitycount(C, c1 ,c2, P, B, W, L)

    for k in list(L.keys()):
        if(k.split()[0] == k.split()[1]):
            L.pop(k)




#Taking input of all path
data_path= input("Enter Path of Data :")
output_path= input("Enter Path for Output:")

#Changing directory to given path
os.chdir(data_path)
text=""

#reading all files at given data_path
for file in glob.glob("*"):

	#opening .txt files one by one
	with open(file,"r",encoding="ISO-8859-1") as f:

		#reading files one by one
		lines=f.readlines()
		for line in lines:

			#checking if there is no empty line
			if not len(line.strip()) == 0:

                #Appending START and STOP to every sentence and lowercasing every word
				line = "START " + line.lower()+" STOP"

                #Cleaning the data
				for word in line.split():
                    #removing tags
					word = " "+word.split("/")[0].strip()+" "

                    #removing punctuation
					text = text + word.translate(line.maketrans("","",string.punctuation))


#Creating counter object which counts occurence of words
count=collections.Counter()
#splitting data
count.update(text.split())
#converting to dictionary
count_dict=OrderedDict(count)

#replacing low frequency words with UNK
for key in count_dict.keys():
	if count_dict[key]>10:
		continue
	else:
		text = text.replace(" "+key+" "," UNK ")

#Creating counter object which counts occurence of words after UNK
clean_count=collections.Counter()
clean_count.update(text.split())


#deleting START and STOP from unigram
del clean_count["START"]
del clean_count["STOP"]

#converted to dictionary
clean_count_dict=OrderedDict(clean_count)

#sorted the unigram in decreasing frequency and then alphabetical
sorted_count = sorted(clean_count_dict.items(), key=lambda kv : (-kv[1], kv[0]))

with open(output_path+"/Unigrams.txt","w+") as fu:
    fu.write(str(sorted_count))

#creating bigrams from each line by splitting lines using STOP keyword
lines = text.split("STOP")

#getting bigrams
bigram_count=collections.Counter()
for line in lines:
	if not len(line.strip()) == 0:
		bigram_count.update(ngrams(line,2))

#converted to dictionary
bigram_dict = OrderedDict(bigram_count)

#getting first 101 words for clusters
classes = sorted_count[:100]

#initializing n to calculate probabilities
n = sum(clean_count_dict.values())

#list of words that are not in clusters
remaining_words = sorted_count[100:]

#converted to dictionary to only list of words
classes = OrderedDict(classes).keys()
remaining_words = OrderedDict(remaining_words).keys()

#creating first 101 clusters
Clusters =[]
for key in classes:
	Clusters.append([key])

x = 0 #loop variable

#dictionary to store unigram probabilities of cluster
P = OrderedDict()
#dictionary to store bigram probabilities of cluster
B = OrderedDict()
#dictionary to store weight value of cluster
W = OrderedDict()

#dictionary to store quality value of cluster
L = OrderedDict()


#initialization of probabilities
while(x != len(Clusters)):
    for word in Clusters[x]:
        P.update({Clusters[x][0]:clean_count[word]})
    x = x + 1


#initilaization of bigram probabilities of cluster
x = 0 #loop variable
while(x != len(Clusters)):
    y = 0 #loop variable
    while (y != len(Clusters)):
        key = Clusters[x][0] + " " + Clusters[y][0]
        if key in bigram_dict.keys():
                    B[key] =  bigram_dict[key]
        else:
            B[key]=0
        y = y + 1
    x = x + 1



#Calculating initial quality
x = 0  #loop variable

#initializing quality value with 0
quality = 0

#variable to store clusters to be merged
c1 = 0
c2 = 0

#Calculating weight value for each pair of cluster
while(x != len(Clusters)):
    y = x
    while (y != len(Clusters)):
        value1 =0
        value2 =0
        a = Clusters[x][0]
        b = Clusters[y][0]
        key = a + " " + b
        if(B[key] == 0):
            value1 =0
        else:
            value1 = (B[key]/n) * (math.log((B[key] * n)/(P[a]*P[b])))
        rev_key = b + " " + a
        if(B[rev_key] == 0):
            value2 =0
        else:
            value2 = (B[rev_key]/n)* (math.log((B[rev_key] * n )/(P[a]*P[b])))

        if( x == y):
            value = value1
        else:
            value = value1 + value2

        W.update({key: value})
        W.update({rev_key: value})
        y = y + 1
    x = x + 1

x=0
y=0
z=0

#Calculating quality value for each pair of cluster
while(x != len(Clusters)):
    y = x+1
    while (y != len(Clusters)):
        key = Clusters[x][0]+ " " + Clusters[y][0]
        z = 0
        while (z != len(Clusters)):
            if(z == x or z ==y ):
                z= z+1
                continue

            value1 = 0
            value2 = 0

            merge1 = Clusters[x][0]
            merge2 = Clusters[y][0]
            merge3 = Clusters[z][0]
            key1 = merge1 + " " + merge3
            key2 = merge2 + " " + merge3

            if B[key1]+B[key2] == 0:
                value1 = 0
            else:
                value1 =  ((B[key1]+B[key2])/n) * (math.log(((B[key1]+B[key2]) * n)/((P[merge1]+P[merge2]) * P[merge3])))

            rev_key1 = merge3 + " " + merge2
            rev_key2 = merge3 + " " + merge1

            if B[rev_key1]+B[rev_key2] == 0:
                value2 = 0
            else:
                value2 =  ((B[rev_key1]+B[rev_key2])/n) * (math.log(((B[rev_key1]+B[rev_key2]) * n)/((P[merge1]+P[merge2]) * P[merge3])))

            if key in L.keys():
                L[key] = L[key] + value1 + value2 - W[key1] - W[key2]

            else:
                L[key] =  value1 + value2 - W[key1] - W[key2]
            z = z + 1
        y = y + 1
    x = x + 1

#finding which two clusters are to be merged

for k in list(L.keys()):
    if(k.split()[0] == k.split()[1]):
        L.pop(k)

merger = max(L.items(), key=operator.itemgetter(1))[0]
for x in range(len(Clusters)):
    if (merger.split()[0] == Clusters[x][0]):
            c1 = x
    if (merger.split()[1] == Clusters[x][0]):
            c2 = x
#declaring dictionary for storing binary strings

strings = OrderedDict()

#updating binary strings after 1st merge
strings = updatestrings(Clusters, c1 ,c2 ,strings)
remaining_words =list (remaining_words)


#continuously merging till we have remaining words
for rwords in remaining_words:

    #updating n every time
    #n = n + clean_count[rwords]

    #deleting merge cluster
    deleteclustors(Clusters,c1,c2,P,B,W,L)

    # adding new cluster to clusters
    Clusters.append([rwords])

    #assigning new cluster its unigram probabilities
    P.update({rwords:clean_count[rwords]})

    #assigning new cluster its bigram probabilities
    for lst in Clusters:
        #designing bigram key of new cluster
        key = rwords + " " + lst[0]
        rev_key = lst[0] + " " + rwords

        #calculating bigram count for new cluster
        for word in lst:
            #designing bigram key for every pair of word in cluster
            bigram_key = rwords + " " + word

            #calculating bigram count for new cluster
            if bigram_key in bigram_dict.keys():
                if key in B.keys():
                    B[key] = B[key] + bigram_dict[bigram_key]
                else:
                    B[key] = bigram_dict[bigram_key]
            else:
                B[key] = 0

            rev_bigram_key = word + " " + rwords

            if rev_bigram_key in bigram_dict.keys():
                if rev_key in B.keys():
                    B[rev_key] = B[rev_key] + bigram_dict[rev_bigram_key]
                else:
                    B[rev_key] = bigram_dict[rev_bigram_key]
            else:
                B[rev_key] = 0




    #calculating quality value for new cluster
    for l in range(len(Clusters)):
        value1 = 0
        value2 = 0

        key = rwords + " " + Clusters[l][0]
        rev_key = Clusters[l][0]+ " " + rwords

        if(B[key] == 0):
            value1 =0
        else:
            value1 = (B[key]/n) *  (math.log((B[key] * n)/(P[rwords]*P[Clusters[l][0]])))

        if(B[rev_key] == 0):
            value2 =0
        else:
            value2 = (B[rev_key]/n) *  (math.log((B[rev_key] * n)/(P[rwords]*P[Clusters[l][0]])))

        W[rev_key] = value1 + value2
        W[key] = value1 + value2

    y=0
    #Ccalculating the change of quality for every cluster
    while (y != len(Clusters)):
        key = Clusters[y][0] + " " + rwords
        z = 0
        while (z != len(Clusters)):
            value1 = 0
            value2 = 0
            key1 = rwords+ " " + Clusters[z][0]
            key2 = Clusters[y][0]+ " " + Clusters[z][0]

            if B[key1]+B[key2]== 0:
                value1 = 0
            else:
                value1 =  ((B[key1]+B[key2])/n) *  (math.log(((B[key1]+B[key2]) * n)/((P[rwords]+P[Clusters[y][0]]) * P[Clusters[z][0]])))

            rev_key1 = Clusters[z][0]+ " " + Clusters[y][0]
            rev_key2 = Clusters[z][0]+ " " + rwords


            if B[rev_key1]+B[rev_key2] == 0:
                    value2 = 0
            else:
                value2 =  ((B[rev_key1]+B[rev_key2])/n) *  (math.log(((B[rev_key1]+B[rev_key2]) * n)/((P[rwords]+P[Clusters[y][0]]) * P[Clusters[z][0]])))

            if key in L.keys() and (key1 and key2 in W.keys()):
                L[key] = L[key] + value1 + value2 - W[key1] - W[key2]
            elif key1 and key2 in W.keys():
                L[key] =  value1 + value2 - W[key1] - W[key2]

            z = z + 1
        y = y + 1

        for k in list(L.keys()):
            if(k.split()[0] == k.split()[1]):
                L.pop(k)


    #finding which two clusters are to be merged
    merger = max(L.items(), key=operator.itemgetter(1))[0]
    for x in range(len(Clusters)):
        if (merger.split()[0] == Clusters[x][0]):
            c1 = x
        if (merger.split()[1] == Clusters[x][0]):
            c2 = x

    #updating strings
    strings = updatestrings(Clusters, c1 ,c2 ,strings)
    print(Clusters)


printcount= 0

#Combining all clusters to finally get binary string
while(len(L)!= 1):

    #deleting merged clusters
    deleteclustors(Clusters,c1,c2,P,B,W,L)

    if(printcount == 0):
        with open(output_path+"/Clusters.txt","w+") as fu:
            fu.write(str(Clusters))
            Cluster_copy = copy.deepcopy(Clusters)
            printcount = 1


    #finding which two clusters are to be merged
    merger = max(L.items(), key=operator.itemgetter(1))[0]
    for x in range(len(Clusters)):
        if (merger.split()[0] == Clusters[x][0]):
            c1 = x
        if (merger.split()[1] == Clusters[x][0]):
            c2 = x

    #updating strings
    strings = updatestrings(Clusters, c1 ,c2 ,strings)
    print(Clusters)


#Finally getting 1 cluster
intstrings = dict()
deleteclustors(Clusters,c1,c2,P,B,W,L)
print(Clusters)

with open(output_path+"/Strings.txt","w+") as fu:
    fu.write(str(strings))

maxlength = 0
#find max length of binary string
for keys in strings.keys():
    if(maxlength < len(str(strings[keys]))):
        maxlength = len(str(strings[keys]))

#padding binary strings
for keys in list(strings.keys()):
    if(maxlength > len(str(strings[keys]))):
        stri = str(strings[keys])
        strings[keys] = stri.ljust(maxlength,'0')

#converting each string into list of 0 and 1
for keys in list(strings.keys()):
    lst = []
    for char in list(strings[keys]):
        lst.append(int(char))

    intstrings.update({keys: lst})

#converting list of 0 and 1 to vectors
for keys in list(intstrings.keys()):
    intstrings[keys] = np.array(intstrings[keys])

cosinedistance = dict()

#calculating cosinedistance
for clust in Cluster_copy:

    #the key is 1st word of cluster
    key = clust[0]

    #unit length clusters have 0 cosine Cosine_Distance
    if len(clust) == 1:
        cosinedistance[key] = 0

    for x in range(len(clust)):
        z = 0
        for y in range(len(clust)):
            z= z+1
            dot_product = (intstrings[clust[x]] @ intstrings[clust[y]])

            mang_a = math.sqrt(sum (intstrings[clust[x]][z]*intstrings[clust[x]][z] for z in range(len(intstrings[clust[x]]))))
            mang_b = math.sqrt(sum (intstrings[clust[y]][z]*intstrings[clust[y]][z] for z in range(len(intstrings[clust[y]]))))

            if key in cosinedistance.keys():
                if(((mang_a * mang_b) == 0) or (x == y)):
                    cosinedistance[key] = cosinedistance[key]
                else:
                    cosinedistance[key] = cosinedistance[key] + (dot_product)/(mang_a * mang_b)
            else:
                if(((mang_a * mang_b) == 0) or (x == y)):
                    cosinedistance[key] = 0
                else:
                    cosinedistance[key] = (dot_product)/(mang_a * mang_b)

        cosinedistance[key] = (cosinedistance[key]/z)


with open(output_path+"/Cosine_Distance.txt","w+") as fu:
    fu.write(str(cosinedistance))
