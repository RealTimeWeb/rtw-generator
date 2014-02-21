package realtimeweb.earthquakewatcher.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


/**
 * A list of authors.
 */
public class MyAuthors {
	
    private ArrayList<String> books;
    private ArrayList<Integer> years;
    
    
    /*
     * @return All the authors.
     */
    public ArrayList<String> getBooks() {
        return this.books;
    }
    
    /*
     * @param All the authors.
     * @return ArrayList<String>
     */
    public void setBooks(ArrayList<String> books) {
        this.books = books;
    }
    
    /*
     * @return All the years.
     */
    public ArrayList<Integer> getYears() {
        return this.years;
    }
    
    /*
     * @param All the years.
     * @return ArrayList<Integer>
     */
    public void setYears(ArrayList<Integer> years) {
        this.years = years;
    }
    
	
	/**
	 * Creates a string based representation of this MyAuthors.
	
	 * @return String
	 */
	public String toString() {
		return "Report[" +books+", "+years+"]";
	}
	
	/**
	 * Internal constructor to create a MyAuthors from a xml representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    
    public MyAuthors(Node raw) {
        XPath xPath =  XPathFactory.newInstance().newXPath();
        
        NodeList items = (NodeList) xPath.evaluate("/bookstore/book/author", raw, XPathConstants.NODESET);
        this.books = new ArrayList<String>();
        for (int i = 0; i < items.getLength(); i++) {
            Node aNode = items.get(i);
            this.books.add(new String(booksIter.next()));
        }
        NodeList items = (NodeList) xPath.evaluate("/bookstore/book/year", raw, XPathConstants.NODESET);
        this.years = new ArrayList<Integer>();
        for (int i = 0; i < items.getLength(); i++) {
            Node aNode = items.get(i);
            this.years.add(new Integer(yearsIter.next()));
        }
    
	}	
}