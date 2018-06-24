#!/usr/bin/python
#Assignment: Apriori implementation in less than 100 lines of code.
import sys
from itertools import chain, combinations
from collections import defaultdict
from datetime import datetime
from optparse import OptionParser

"""Function which reads from the file and yields a generator"""
def dataFromFile(fname):
    file_iter = open(fname, 'r')
    for line in file_iter:
        line = line.strip().rstrip(',')
        record = frozenset(line.split(','))
        yield record

'''
this function read the data preprocessed and return a set of items and a list of transactions.
in our case there will be 671 transactions and 11 million items
'''
def read_Data(data):
    transactions = list()
    items = set()
    Localset = defaultdict(int)
    for line in data:
        transc = frozenset(line)
        transactions.append(transc)
        for t in transc:
            item = frozenset([t.rstrip()])
            Localset[item] += 1
            items.add(item)
    return items, transactions, Localset

'''
Joinset function join items, generating candidates but applying rules given in lecuter
if A[:-1] = B[:-1], generate A + B[-1:]
'''
def joinSet(itemSet, length):
    pruning = set()
    for i in itemSet:
        for j in itemSet:
            i = list(i)
            j = list(j)
            if(len(frozenset(i).union(frozenset(j[-1:]))) == length):
            	print i , j
               
                if length == 2:
                    pruning.add(frozenset(i).union(frozenset(j)))
                if(length > 2):
                    if(i[:-1] == j[:-1]):         #A[:-1] = B[:-1], generate A + B[-1:]
                        pruning.add(frozenset(i).union(frozenset(j[-1:])))
    return pruning

'''subset return non empty subsets of array.'''
def subsets(itemset):
    return chain(*[combinations(itemset, i + 1) for i, a in enumerate(itemset)])

''' Support calculates the support and return true if satisfie the condition being greater then minSupport given, or false otherwise'''
def Support(item, transcation, minSupport):
    support = float(item)/len(transcation)
    if support >=float(minSupport):
        return True
    else:
        return False

'''ItemsWithMinSupport return the set of items which are frequent, and their support'''
def ItemsWithMinSupport(Items, transcations, minSupport, k, Localset, support):

    SetofItems = set()
    cnt = 0
    if (k > 1):
    	Localset = defaultdict(int)
    	for item in Items:
    		for t in transcations:
    			if item.issubset(t):
    				print item
    				Localset[item] += 1
    	print ('finishing counting...')
    for items, frequency in Localset.items():        
        if( Support(frequency,transcations, minSupport)):
            if len(items) > 1:
                cnt +=1
            SetofItems.add(items)
            support[items] = float(frequency)/len(transcations)
    print 'finishin adding Frequent items to list ...%d'%cnt
    return SetofItems, support

'''This function generate association rules based on Frequent items sets outputed by apriori Function'''
def generate_Rules(FreqItemSets, minSupport, minConfidence):
    Rules = []
    cnt = 0
    for item, support in FreqItemSets.items():
        if(len (item) > 1):
            for _sub in subsets(item):
                _subs = item.difference(frozenset(_sub))
                if _subs:
                    _sub = frozenset(_sub)
                    _subset = _sub | _subs
                    confidence = float(FreqItemSets[_subset]) / FreqItemSets[_sub]
                    if(confidence >= float(minConfidence)):
                        cnt += 1
                        Rules.append((_sub, _subs, confidence))
    print('Found %d Rules '%(cnt))
    return Rules

'''Apriori is the main function where all the work  is done. it reads the data, generate candidate and return a list of frequent itemsets'''
def Apriori(input_data, minSupport, minConfidence):

    begin = datetime.now()
    Items, Transactions, Localset = read_Data(input_data)
    
 
    end = datetime.now()
    diff = begin - end
    print('Finished reading data in  %d'%diff.total_seconds())
    final_Item_list = dict()
    largeSet = dict()
    support = dict()
    k = 1

    while True:
        if k > 1:
            Items = joinSet(l_Item_min_support, k)                       #2 or more candidate generation

        l_Item_min_support,support = ItemsWithMinSupport(Items, Transactions, minSupport, k, Localset, support)    
        if not l_Item_min_support:
            break
       
       
        k += 1
    return support

'''Printing the outputs'''
def print_FItemSets(Freq_itemset, filename):
    file = open(filename, 'w')
    for item, support in sorted(Freq_itemset.items(), key=lambda (item, support): support):
        file.write('{} : {} \n'.format(tuple(item), round(support, 4)))
        print item, support
    file.close()

def print_rules(Rules,filename):
    file = open(filename, 'w')
    for a, b, confidence in sorted(Rules, key=lambda (a, b, confidence): confidence):
        file.write("Rule: {} ==> {} : {} \n".format(tuple(a), tuple(b), round(confidence,4)))
    file.close()



begin = datetime.now()
print('Starting Program ...')
optparser = OptionParser()
optparser.add_option('-i', '--inputFile',
                     dest='input',
                     help='filename containing csv',
                     default=None)
optparser.add_option('-s', '--minSupport',
                     dest='minS',
                     help='minimum support value',
                     default=0.1,
                     type='float')
optparser.add_option('-c', '--minConfidence',
                     dest='minC',
                     help='minimum confidence value',
                     default=0.6,
                     type='float')
optparser.add_option('-f', '--OutputFIS',
                     dest='FIS',
                     help='output file writing Frequent Item Set',
                     default=None)
optparser.add_option('-r', '--oRule',
                     dest='Rule',
                     help='output file writing the rules',
                     default=0.6)

(options, args) = optparser.parse_args()


if options.FIS is None:
    print ('Please specify your output file for Frequent Item Sets')
    sys.exit(1)
elif options.Rule is None:
    print('Please specify your output file for Association Rules')
    sys.exit(1)
elif options.input is not None:
    input_data = dataFromFile(options.input)
    print options.FIS
    items = Apriori(input_data, options.minS, options.minC)
    print(' Finished apriori run ..')
    print('Printing Frequent ItemsSets')
    print_FItemSets(items,options.FIS)
    end_apriori = datetime.now()
    diff = begin - end_apriori
    print('The system perform Apriori step in %d'%diff.total_seconds())
    '''print( 'Printing Rules')
                Rules = generate_Rules(items,options.minS, options.minC)
                print_rules(Rules,options.Rule)
                end = datetime.now()
                diff = end_apriori - end
                diff_total = begin - end
                print('The system perform Association Rules Generation step in %d and Total Progran run in %d'%(diff.total_seconds(),diff_total.total_seconds()))'''
else:
    print('Please specify your input file.')
    sys.exit(1)

