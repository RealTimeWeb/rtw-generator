package realtimeweb.earthquakewatcher.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;


import org.htmlcleaner.TagNode;


import realtimeweb.earthquakewatcher.domain.Earthquake;

/**
 * A list of authors.
 */
public class MyAuthors {
	
    private String test;
    private ArrayList<String> books;
    private Earthquake other;
    private ArrayList<Integer> years;
    
    
    /*
     * @return amazing
     */
    public String getTest() {
        return this.test;
    }
    
    /*
     * @param amazing
     * @return String
     */
    public void setTest(String test) {
        this.test = test;
    }
    
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
     * @return amazing
     */
    public Earthquake getOther() {
        return this.other;
    }
    
    /*
     * @param amazing
     * @return Earthquake
     */
    public void setOther(Earthquake other) {
        this.other = other;
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
		return "Report[" +test+", "+books+", "+other+", "+years+"]";
	}
	
	/**
	 * Internal constructor to create a MyAuthors from a html representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    
    public MyAuthors(TagNode raw) {
        
        this.test = raw.evaluateXPath("/bookstore/").toString();
        Object[] booksItems = raw.evaluateXPath("/bookstore/book/author");
        this.books = new ArrayList<String>();
        for (int i = 0; i < booksItems.length; i++) {
            TagNode aNode = (TagNode)booksItems[i];
            this.books.add((aNode.toString()));
        }
        this.other = new Earthquake((TagNode) raw.evaluateXPath("/bookstore/"));
        Object[] yearsItems = raw.evaluateXPath("/bookstore/book/year");
        this.years = new ArrayList<Integer>();
        for (int i = 0; i < yearsItems.length; i++) {
            TagNode aNode = (TagNode)yearsItems[i];
            this.years.add(Integer.parseInt(aNode.toString()));
        }
    
	}	
}