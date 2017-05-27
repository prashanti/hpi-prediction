def load_parents():
	subsumers=dict()
	# this is a file that contains Subsumers for CC annotations in a tsv format (Example_Subsumerfile.tsv)
	infile=open(sys.argv[2])
	for line in infile:
		term,parent=line.strip().split("\t")
		if term not in subsumers:
			subsumers[term]=set([term])
		if parent !="owl:Thing" and parent!="GO_0005575":
			subsumers[term].add(parent)
			if parent not in subsumers:
				subsumers[parent]=set([parent])
	infile.close()
	return subsumers

def get_allpart_of_children():
	# this is a file that contains part_of for CC terms
	infile=open("../data/GO_CC_PartOfImmediateChildren.tsv")
	partof=dict()
	for line in infile:
		parent,child=line.strip().split("\t")
		if parent not in partof:
			partof[parent]=set()
		partof[parent].add(child)
	for term in partof:
		childset=partof[term]
		while len(childset)>0:
			temp=set()
			for child in childset:
				if child in partof:
					partof[term]=set.union(partof[term],partof[child])
					temp=set.union(temp,partof[child])
			childset=copy.deepcopy(temp)
	return partof


def load_children():
	exceptionset=load_exceptions()
	children=dict()
	# this is a file that contains all children for CC terms
	infile=open("../data/GO_CC_AllChildren.tsv")
	for line in infile:
		term,child=line.split("\t")
		term=term.strip()
		child=child.strip()
		if term not in children:
			children[term]=set([term])
		children[term].add(child)

	infile.close()
	partofchildren=get_allpart_of_children()
	
	for term in partofchildren:
		if term in children:
			children[term]=set.union(children[term],partofchildren[term])
		else:
			children[term]=partofchildren[term]
			children[term].add(term)
	return children





def load_exceptions():
	exceptionset=set()
	for line in open("../data/hostcell2cell_mapping.txt"):
		goid1,name1,goid2,name2,subont,comment=line.split("\t")
		exceptionset.add(goid1.strip().replace(":","_"))
		exceptionset.add(goid2.strip().replace(":","_"))
	return exceptionset



def extra_colocalize():
	children=load_children()
	speciallocalizationlist=[]
	infile=open("../data/hostcell2cell_mapping.txt")
	infile.next()
	for line in infile:
		temp=[]
		goid1,name1,goid2,name2,subont,comment=line.split("\t")
		goid1=goid1.strip().replace(":","_")
		goid2=goid2.strip().replace(":","_")
		childlist=[]
		childlist=children[goid1] if goid1 in children else [goid1] # assume this contains goid1
		temp.append(childlist)
		childlist=[]
		childlist=children[goid2] if goid2 in children else [goid2] # assume this contains goid1
		temp.append(childlist)
		speciallocalizationlist.append(temp)
	return speciallocalizationlist


def check_colocalization(p1cclist,p2cclist,subsumers,speciallocalizationlist):
	p1ccsubsumers=set()
	p2ccsubsumers=set()
	colocalizeflag=0
	for term in p1cclist:
		p1ccsubsumers=set.union(p1ccsubsumers,subsumers[term])
		for term in subsumers[term]:
			p1ccsubsumers=set.union(p1ccsubsumers,subsumers[term])

	for term in p2cclist:
		p2ccsubsumers=set.union(p2ccsubsumers,subsumers[term])
		for term in subsumers[term]:
			p2ccsubsumers=set.union(p2ccsubsumers,subsumers[term])
	if len(set.intersection(p1ccsubsumers,p2ccsubsumers))>0:
		colocalizeflag=1
		return 1

	else:
		extracolocalizeflag=check_extracolocalization(p1cclist,p2cclist,speciallocalizationlist)
		return colocalizeflag ^ extracolocalizeflag

def check_extracolocalization(p1cclist,p2cclist,speciallocalizationlist):
	for pair in speciallocalizationlist:
		for ann1 in p1cclist:
			for ann2 in p2cclist:
				if ann1 in pair[0] and ann2 in pair[1]:
					return 1
				if ann1 in pair[1] and ann2 in pair[0]:
					return 1
	return 0


def main():
	# this is a file that contains CC annotations in a tsv format (Example_Annotationfile.tsv)
	infile=open(sys.argv[1])
	infile.next()
	speciallocalizationlist= extra_colocalize()
	subsumers=load_parents()
	for line in infile:
		tempannotations=set()
		p1,p1cclist,p2,p2cclist=line.split("\t")
		p1cclist=p1cclist.strip().split(",")
		p2cclist=p2cclist.strip().split(",")
		tempannotations=tempannotations|set(p1cclist)
		tempannotations=tempannotations|set(p2cclist)
		for tmp in tempannotations:
			if tmp not in subsumers:
				subsumers[tmp]=set([tmp])
		colocalizeflag=check_colocalization(p1cclist,p2cclist,subsumers,speciallocalizationlist)
		
		# Flag value 1 indicates colocalization and 0 otherwise
		print p1,p2,colocalizeflag
	infile.close()


if __name__ == "__main__":
    import sys
    import copy
    main()    