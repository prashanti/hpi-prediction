from __future__ import division
def load_subsumers():
	subsumers=dict()
	infile=open("../data/GO_AllSubsumers.tsv")
	infile.next()
	for line in infile:
		term,subsumer=line.strip().split("\t")
		if term not in subsumers:
			subsumers[term]=set([term])
		if subsumer !="owl:Thing":
			subsumers[term].add(subsumer)
	infile.close()
	return subsumers

def compute_ic_profile(profiles,subsumers):
	inferredprofiles=dict()
	icdict=dict()
	frequency=dict()
	annotationset=set()
	for protein in profiles:
		inferredprofiles[protein]=set()
		for annotation in profiles[protein]:
			inferredprofiles[protein].add(annotation)
			if annotation in subsumers:
				inferredprofiles[protein]=set.union(inferredprofiles[protein],subsumers[annotation])
	
	outfile=open("../data/InferredProfiles.txt",'w')	
	for protein in inferredprofiles:
		outfile.write(protein+"\t"+",".join(inferredprofiles[protein])+"\n")
		for annotation in inferredprofiles[protein]:
			if annotation not in frequency:
				frequency[annotation]=0
			frequency[annotation]+=1

	corpussize=len(profiles)
	maxic=round(-math.log(1/corpussize),2)	
	for annotation in frequency:
		ic=round((-math.log(frequency[annotation]/corpussize))/maxic,2)
		icdict[annotation]=ic
	return icdict



def compute_similarity(profiles,subsumers,icdict,comparisons):
	outfile=open("../results/SimilarityScores.tsv",'w')
	outfile.write("Host_Prot\tPath_Prot\tSimilarity_Score\n")
	bpsimilaritydict=dict()
	for pair in comparisons:
		profile1=profiles[pair[0]]
		profile2=profiles[pair[1]]
		mediansim,bpsimilaritydict=calculate_bestpairs_symmetric(profile1,profile2,icdict,subsumers,bpsimilaritydict)
		outfile.write(pair[0]+"\t"+pair[1]+"\t"+str(mediansim)+"\n")

def getmax(lcslist):
	micaic=0
	mica=""
	match=""
	for tup in lcslist:
		if tup[1]>micaic:
			micaic=tup[1]
			mica=tup[2]
			match=tup[0]
	return match,micaic,mica

def getmicaic(term1,term2,ancestors,icdict):
	micaic=0
	mica=""
	if term1 in ancestors and term2 in ancestors:
		commonancestors=set.intersection(ancestors[term1],ancestors[term2])
	else:
		commonancestors=set()
	lcslist=[(term2,icdict[anc],anc) for anc in commonancestors]
	match,micaic,mica=getmax(lcslist)
	if len(lcslist)>0:
		return micaic,mica
	else:
		return 0,"None"

def calculate_bestpairs_symmetric(profile1,profile2,icdict,subsumers,bpsimilaritydict):
	finalsim=0
	bestmatchiclist=[]
	termmatchic=[]
	matchdata=[]

	for term1 in profile1:
		termmatchic=[]
		for term2 in profile2:
			termtuple=tuple(sorted((term1,term2)))
			if termtuple in bpsimilaritydict:
				termmatchic.append(bpsimilaritydict[termtuple])
			
			else:
				micaic,mica=getmicaic(term1,term2,subsumers,icdict)
				termmatchic.append((term2,micaic,mica))
				bpsimilaritydict[termtuple]=(term2,micaic,mica)
		bestmatch,bestic,bestmica=getmax(termmatchic)
		bestmatchiclist.append(bestic)
	mediansim1=np.median(bestmatchiclist)

	finalsim=0
	bestmatchiclist=[]
	termmatchic=[]
	matchdata=[]
	for term1 in profile2:
		termmatchic=[]
		for term2 in profile1:
			termtuple=tuple(sorted((term1,term2)))
			termmatchic.append(bpsimilaritydict[termtuple])
		bestmatch,bestic,bestmica=getmax(termmatchic)
		bestmatchiclist.append(bestic)
	mediansim2=np.median(bestmatchiclist)
	return np.mean([mediansim1,mediansim2]),bpsimilaritydict

def load_profiles():
	profiles=dict()
	comparisons=set()
	infile=open("../data/combined_dataset.tsv")
	infile.next()
	for line in infile:
		data=line.strip().split("\t")
		p1,p1annlist,p2,p2annlist=data[1],data[12],data[5],data[13]
		p1annlist=p1annlist.replace(":","_")
		p2annlist=p2annlist.replace(":","_")
		comparisons.add((p1,p2))
		p1annlist=set(p1annlist.split(","))
		p2annlist=set(p2annlist.split(","))
		if p1 not in profiles:
			profiles[p1]=p1annlist	
		if p2 not in profiles:
			profiles[p2]=p2annlist
	return profiles,comparisons


def main():
	profiles,comparisons=load_profiles()
	subsumers=load_subsumers()
	icdict=compute_ic_profile(profiles,subsumers)
	compute_similarity(profiles,subsumers,icdict,comparisons)
if __name__ == "__main__":
	import math
	import os
	import json
	import numpy as np
	import sys
	main()

