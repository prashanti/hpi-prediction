
def load_parents():
	subsumers=dict()
	# this is a file that contains Subsumers for CC annotations in a tsv format (Example_Subsumerfile.tsv)
	infile=open(sys.argv[2])
	infile.next()
	for line in infile:
		term,parent=line.strip().split("\t")
		if term not in subsumers:
			subsumers[term]=set([term])
		subsumers[term].add(parent)
	infile.close()
	return subsumers

def check_colocalization(p1cclist,p2cclist,subsumers):
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
	return colocalizeflag


def main():
	# this is a file that contains CC annotations in a tsv format (Example_Annotationfile.tsv)
	infile=open(sys.argv[1])
	infile.next()
	subsumers=load_parents()
	for line in infile:
		p1,p1cclist,p2,p2cclist=line.strip().split("\t")
		p1cclist=p1cclist.split(",")
		p2cclist=p2cclist.split(",")
		colocalizeflag=check_colocalization(p1cclist,p2cclist,subsumers)
		
		# Flag value 1 indicates colocalization and 0 otherwise
		print p1,p2,colocalizeflag
	infile.close()


if __name__ == "__main__":
    import sys
    main()    