# -*- encoding:utf8 -*-
'''
@author:linsenGuo
@email:guolinsen123@gmail.com
'''
#import ordered dict module
from collections import OrderedDict
import os,sys
from optparse import OptionParser 
def print_tree(root):
    buff=['root']
    print_node(root,buff,'')
    print('\n'.join(buff))
def print_node(node,buff,prefix):
    childNumber=len(node.children)
    for num,child in node.children.items():
        childNumber-=1
        if child:
            buff.append('%s +- %s' % (prefix, num))
            if childNumber:
                print_node(child,buff,prefix+' |  ')
            else:
                print_node(child,buff,prefix+'    ')

class TreeNode():
    def __init__(self,number,occurCnt=1,parent=None):
        self.number=number
        self.count=occurCnt
        #connect the horizontal node 
        self.nodeLink=None
        self.parent=parent
        self.children={}
    def inc(self,occurCnt=1):
        self.count+=occurCnt
class FPGrowth():
    def __init__(self,minSupport=2):
        self.minSupport=minSupport
        self.id2term={}
        self.term2id={}
        self.documents=[]
        self.freqItems=[]
    def loadData(self,filepath):
        if os.path.exists(filepath):
            f=open(filepath,'r')
            lines=f.readlines()
            f.close()
            lines=[line.strip() for line in lines]
            result={}
            termSet=set()
            count=0
            for line in lines:
                document=[]
                key=set()
                terms=set(line.split(' '))
                for term in terms:
                    if term not in termSet:
                        termSet.add(term)
                        count+=1
                        if term=='':
                            print(line)
                        self.id2term[count]=term
                        self.term2id[term]=count
                        key.add(self.term2id[term])
                    else:
                        key.add(self.term2id[term])
                    document.append(self.term2id[term])
                self.documents.append(document)
                result[frozenset(key)]=1
            return result
        else:
            raise Exception('File Not Exist')
    def changeId2Term(self,data):
        for i in range(len(data)):
            items=set()
            for j in data[i]:
                items.add(self.id2term[j])
            data[i]=items
        return data
    def createTree(self,transactions):
        headerTable={}
        '''
        transactions is a dict(key=transaction,value=occurence)
        '''
        for transaction in transactions:
            for item in transaction:
                headerTable[item]=headerTable.get(item,0)+transactions[transaction]
        '''
        delete items which its value is less than minSupport
        '''
        for k in list(headerTable.keys()):
            if headerTable[k]<self.minSupport:
                del headerTable[k]
        '''
        sorted headerTable in a descend order
        '''
        headerTable=OrderedDict(sorted(headerTable.items(),key=lambda t:t[1],reverse=True))
        '''
        '''
        if len(headerTable)==0:
            return None,None
        '''
        add one item to record same element treenode
        headerTable[item]=[count,node]
        '''
        for item,value in headerTable.items():
            headerTable[item]=[headerTable[item],None]
        '''
        init rootNode
        '''
        rootNode=TreeNode(None,None,None)
        '''
        recursive create tree
        '''
        for transaction,count in transactions.items():
            '''
            sort the transaction by word occurence number and update the tree
            '''
            items={}
            for item in transaction:
                if item in headerTable:
                    items[item]=headerTable[item][0]
            if len(items)>0:
                orderedItems=[x[0] for x in sorted(items.items(), key=lambda obj: obj[1], reverse=True)]
                self.updateTree(orderedItems,rootNode,headerTable,count)
        return rootNode,headerTable
    def updateTree(self,items,parent,headerTable,count):
        #print(items,count)
        if items[0] in parent.children:
            parent.children[items[0]].inc(count)
        else:
            parent.children[items[0]]=TreeNode(items[0],count,parent)
            if headerTable[items[0]][1]==None:
                headerTable[items[0]][1]=parent.children[items[0]]
            else:
                self.updateHeader(headerTable[items[0]][1],parent.children[items[0]])
        if len(items)>1:
            self.updateTree(items[1:],parent.children[items[0]],headerTable,count)
    def updateHeader(self,origin_treenode,new_treenode):
        while (origin_treenode.nodeLink!=None):
            origin_treenode=origin_treenode.nodeLink
        origin_treenode.nodeLink=new_treenode
    def findConditionalPatternBases(self,treenode):
        conditionalPatternBases={}
        while treenode!=None:
            path=[]
            self.recursiveGetfullPath(treenode,path)
            if len(path)>1:
                conditionalPatternBases[frozenset(path[1:])]=treenode.count
            treenode=treenode.nodeLink
        return conditionalPatternBases
    def recursiveGetfullPath(self,treenode,path):
        if treenode.parent!=None:
            path.append(treenode.number)
            self.recursiveGetfullPath(treenode.parent,path)
    def mineTree(self,rootNode,headerTable,prefix,result):
        '''
        sorted headerTable by element occurence count
        '''
        headerLst=[x[0] for x in sorted(headerTable.items(),key=lambda obj:obj[1][0])]
        #print(headerTable.items())
        for element in headerLst:
            freqSet=prefix.copy()
            freqSet.add(element)
            result.append(freqSet)
            condPatBases=self.findConditionalPatternBases(headerTable[element][1])
            condTree,headerForCondTree=self.createTree(condPatBases)
            '''
            if conditional Tree not null then carry on mine freq pattern
            '''
            if headerForCondTree!=None:
                self.mineTree(condTree,headerForCondTree,freqSet,result)
    def fpgrowth(self,dataSet,minSupport,minLength=2):
        self.minSupport=minSupport
        self.minLength=minLength
        fptree,header=self.createTree(dataSet)
        if header!=None:
            '''
            store all extracted frequent items
            '''
            results=[]
            self.mineTree(fptree,header,set([]),results)
            self.freqItems=results
            #self.outputVocabulary()
            #self.outputFreqItems()
            #self.outputDocuments()
            result=self.changeId2Term(results)
            self.outputFreqItems()
            return result
        else:
            print('fptree is null')
    '''
    output vocabulary
    it consist of n lines,representing n different words in corpus
    each line has a id and a word like following form:
    id_1 term_1
    id_2 term_2
    ...
    id_n term_n
    '''
    def outputVocabulary(self):
        f=open('vocabulary.txt','w')
        voca=sorted(self.id2term.items(),key=lambda o:o[0])
        for [i,w] in voca:
            f.write('%d %s\n'%(i,w))
        f.close()
    '''
    output frequent items in term's id form
    '''
    def outputFreqItems(self):
        f=open('freqItems.txt','w')
        for item in self.freqItems:
            item=sorted(list(item))
            if len(item)<self.minLength:
                continue
            for i in item:
                f.write(str(i)+' ')
            f.write('\n')
        f.close()
    '''
    output document in term's id form
    '''
    def outputDocuments(self):
        f=open('documents.txt','w')
        for document in self.documents:
            for word in document:
                f.write(str(word)+' ')
            f.write('\n')
        f.close()
if __name__=='__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",default='test.txt',
                  help="input documents")
    parser.add_option("-s", "--minsupport",dest="minSupport",type='int',default=2,
                  help="min support")
    parser.add_option("-l", "--minlength",dest="minLength",type='int',default=2,
                  help="min length")
    (option,argv)=parser.parse_args(sys.argv[1:])
    fpgrowth=FPGrowth()
    dataSet=fpgrowth.loadData(option.filename)
    result=fpgrowth.fpgrowth(dataSet,option.minSupport,option.minLength)