This is readme file for question 3

How to run:
1. Install Pythonv3.6.4
2. Run the implementation by entering command on your command line python by command -
   python filename
3.The program asks
Path where data is stored -Enter Path of Data :
Path where output is to be stored - Enter Path for Output:

4. Unigrams.txt will contain count of unigrams
5. Clusters.txt will contain Clusters
6. Strings.txt will contain Bianry Strings
7. Cosine_Distance.txt will conatin Cosine Distance of clusters.

Cosine_Distance.txt has average cosine distance computed of clusters. The cosine distnace of cluster is shown by first word of cluster and the average value. 
To find the average cosine distance of a cluster find the first word in cluster. Using this word you can find Cosine Distance of that Cluster in Clusters.txt.
Cosine distnace are listed as First Word of Cluster: Value of Cosine Distance

Note -
All of these libraries  were imported make sure that they are in the system while running the program
from __future__ import division
import glob, os
import collections
import math
import operator
from collections import OrderedDict
import numpy as np - used only for vector conversion
import scipy    - used only for vector conversion
import copy  - used to copy dict