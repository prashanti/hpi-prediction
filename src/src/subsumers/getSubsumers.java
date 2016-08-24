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
// javac -cp .:/Users/pmanda/Documents/JARs/org.semanticweb.owl.owlapi-4.1.jar:/Users/pmanda/Documents/JARs/elk-owlapi.jar:/Users/pmanda/Documents/JARs/log4j-1.2.17.jar ./subsumers/getSubsumers.java

// java -cp .:/Users/pmanda/Documents/JARs/org.semanticweb.owl.owlapi-4.1.jar:/Users/pmanda/Documents/JARs/elk-owlapi.jar:/Users/pmanda/Documents/JARs/log4j-1.2.17.jar subsumers/getSubsumers ../../data/go-plus.owl ../../data/GO_Subsumers.tsv

public class getSubsumers 
{

	public static void main(String[] args) throws IOException, OWLOntologyStorageException, OWLOntologyCreationException,  ParserException, ClassNotFoundException, SQLException 
	{
		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		File inputont = new File(args[0]);
	    PrintWriter printWriter = new PrintWriter (args[1]);
		OWLOntology ontology = manager.loadOntologyFromOntologyDocument(inputont);
	    OWLReasonerFactory reasonerFactory = new ElkReasonerFactory();
	    OWLReasoner reasoner = reasonerFactory.createReasoner(ontology);
	    reasoner.precomputeInferences(InferenceType.CLASS_HIERARCHY); 
	    for (OWLClass cls : ontology.getClassesInSignature()){
			Set<OWLClass> supclses = reasoner.getSuperClasses(cls, false).getFlattened();
	        for (OWLClass subsumer : supclses) {
	        	for(OWLAnnotationAssertionAxiom annotations:subsumer.getAnnotationAssertionAxioms(ontology)){
	    		    if (annotations.getProperty().getIRI().getFragment().toString().equals("hasOBONamespace")){
	                	if (annotations.getValue().toString().contains("cellular_component")){
	                		printWriter.write((cls.toString()+"\t"+subsumer.toString()+"\n").replace("<http://purl.obolibrary.org/obo/", "").replace(">", ""));
	                	}
	                }
	    		}
	        }
	    }
		printWriter.close();	
	}
}



