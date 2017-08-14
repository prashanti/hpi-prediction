package subsumers;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.SQLException;
import java.util.Collections;
import java.util.HashSet;
import java.util.Set;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.expression.ParserException;
import org.semanticweb.owlapi.model.ClassExpressionType;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLClassAxiom;
import org.semanticweb.owlapi.model.OWLClassExpression;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLObjectPropertyExpression;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.model.OWLOntologyStorageException;
import org.semanticweb.owlapi.model.OWLSubClassOfAxiom;
import org.semanticweb.owlapi.model.PrefixManager;
import org.semanticweb.owlapi.util.DefaultPrefixManager;
import org.semanticweb.owlapi.util.OWLClassExpressionVisitorAdapter;
//Usage
//javac -cp .:/Users/prashantimanda/Dropbox/Research/Github/JARS/org.semanticweb.owl.owlapi-4.1.jar:/Users/prashantimanda/Dropbox/Research/Github/JARS/elk-owlapi.jar:/Users/prashantimanda/Dropbox/Research/Github/JARS/log4j-1.2.17.jar ./subsumers/GetPartOfChildren.java
//java -cp .:/Users/prashantimanda/Dropbox/Research/Github/JARS/org.semanticweb.owl.owlapi-4.1.jar:/Users/prashantimanda/Dropbox/Research/Github/JARS/elk-owlapi.jar:/Users/prashantimanda/Dropbox/Research/Github/JARS/log4j-1.2.17.jar subsumers/GetPartOfChildren ../../data/go-plus.owl ../../data/GO_CC_PartOfImmediateChildren.tsv


public class GetPartOfChildren {
	public static void main(String[] args) throws IOException, OWLOntologyStorageException, OWLOntologyCreationException,  ParserException, ClassNotFoundException, SQLException {
		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		File inputont = new File(args[0]);
		PrintWriter printWriter = new PrintWriter (args[1]);
		OWLOntology ontology = manager.loadOntologyFromOntologyDocument(inputont);
	    for (OWLClass cls : ontology.getClassesInSignature()){
		    Set<OWLClassAxiom> tempAx=ontology.getAxioms(cls);
		    String parent="";
		    for(OWLClassAxiom ax: tempAx){
		        for(OWLClassExpression nce:ax.getNestedClassExpressions())
		            if(nce.getClassExpressionType()!=ClassExpressionType.OWL_CLASS)
		                if (ax.getAxiomType().toString().equals("SubClassOf"))
		                {
		                	if (ax.toString().contains("ObjectSomeValuesFrom(<http://purl.obolibrary.org/obo/BFO_0000050>"))
		                	{
		        	        for(OWLClass sig: ax.getClassesInSignature())
		        	        {
		        	        	 if (!sig.toString().equals(cls.toString()))
		        	        	 {
		        	        		 parent=sig.toString();
		        	        	 }
		        	      
		        	        }
		        	        
		        	        printWriter.write(parent.replace("<http://purl.obolibrary.org/obo/", "").replace(">", "")+"\t"+cls.toString().replace("<http://purl.obolibrary.org/obo/", "").replace(">", "")+"\n");
		                }
		                }
		            
		    }

		   
	}
	
    printWriter.close();
}
}
	    
	    
	
