package subsumers;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.SQLException;
import java.util.Set;
import org.semanticweb.elk.owlapi.ElkReasonerFactory;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.expression.ParserException;
import org.semanticweb.owlapi.model.OWLAnnotationAssertionAxiom;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.model.OWLOntologyStorageException;
import org.semanticweb.owlapi.reasoner.InferenceType;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
// Usage
// javac -cp .:/Users/prashantimanda/Dropbox/Research/Github/JARS/org.semanticweb.owl.owlapi-4.1.jar:/Users/prashantimanda/Dropbox/Research/Github/JARS/elk-owlapi.jar:/Users/prashantimanda/Dropbox/Research/Github/JARS/log4j-1.2.17.jar ./subsumers/GetChildren.java
// java -cp .:/Users/prashantimanda/Dropbox/Research/Github/JARS/org.semanticweb.owl.owlapi-4.1.jar:/Users/prashantimanda/Dropbox/Research/Github/JARS/elk-owlapi.jar:/Users/prashantimanda/Dropbox/Research/Github/JARS/log4j-1.2.17.jar subsumers/GetChildren ../../data/go-plus.owl ../../data/GO_CC_AllChildren.tsv

public class GetChildren {
	public static void main(String[] args) throws IOException, OWLOntologyStorageException, OWLOntologyCreationException,  ParserException, ClassNotFoundException, SQLException {
		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		File inputont = new File(args[0]);
	    PrintWriter printWriter = new PrintWriter (args[1]);
		OWLOntology ontology = manager.loadOntologyFromOntologyDocument(inputont);
	    OWLReasonerFactory reasonerFactory = new ElkReasonerFactory();
	    OWLReasoner reasoner = reasonerFactory.createReasoner(ontology);
	    reasoner.precomputeInferences(InferenceType.CLASS_HIERARCHY); 
	    for (OWLClass cls : ontology.getClassesInSignature()){
			Set<OWLClass> subclses = reasoner.getSubClasses(cls, false).getFlattened();
	        for (OWLClass subclass : subclses) {
	        	for(OWLAnnotationAssertionAxiom annotations:subclass.getAnnotationAssertionAxioms(ontology)){
	    		    if (annotations.getProperty().getIRI().getFragment().toString().equals("hasOBONamespace")){
	                	if (annotations.getValue().toString().contains("cellular_component")){
	                		printWriter.write((cls.toString()+"\t"+subclass.toString()+"\n").replace("<http://purl.obolibrary.org/obo/", "").replace(">", ""));}}}}}
	     printWriter.close();}}	
	
