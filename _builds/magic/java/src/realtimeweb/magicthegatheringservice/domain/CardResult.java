package realtimeweb.magicthegatheringservice.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;




/**
 * The result of a card search, only having the ID and card name. You can look up the card by its ID for more complete information.
 */
public class CardResult {
	
    private Integer id;
    private String name;
    
    
    /*
     * @return The unique id number of this card
     */
    public Integer getId() {
        return this.id;
    }
    
    /*
     * @param The unique id number of this card
     * @return Integer
     */
    public void setId(Integer id) {
        this.id = id;
    }
    
    /*
     * @return The name of this card.
     */
    public String getName() {
        return this.name;
    }
    
    /*
     * @param The name of this card.
     * @return String
     */
    public void setName(String name) {
        this.name = name;
    }
    
	
	/**
	 * Creates a string based representation of this CardResult.
	
	 * @return String
	 */
	public String toString() {
		return "CardResult[" +id+", "+name+"]";
	}
	
	/**
	 * Internal constructor to create a CardResult from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    public CardResult(Map<String, Object> raw) {
        // TODO: Check that the data has the correct schema.
        // NOTE: It's much safer to check the Map for fields than to catch a runtime exception.
        try {
            this.id = Integer.parseInt(raw.get("id").toString());
            this.name = raw.get("name").toString();
        } catch (NullPointerException e) {
    		System.err.println("Could not convert the response to a CardResult; a field was missing.");
    		e.printStackTrace();
    	} catch (ClassCastException e) {
    		System.err.println("Could not convert the response to a CardResult; a field had the wrong structure.");
    		e.printStackTrace();
        }
    
	}	
}