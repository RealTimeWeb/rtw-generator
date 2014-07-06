package realtimeweb.magicthegatheringservice.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;




/**
 * The print expansion this belongs to.
 */
public class Print {
	
    private String set;
    private Integer id;
    
    
    /*
     * @return The ID code of this set.
     */
    public String getSet() {
        return this.set;
    }
    
    /*
     * @param The ID code of this set.
     * @return String
     */
    public void setSet(String set) {
        this.set = set;
    }
    
    /*
     * @return The unique id number of this set.
     */
    public Integer getId() {
        return this.id;
    }
    
    /*
     * @param The unique id number of this set.
     * @return Integer
     */
    public void setId(Integer id) {
        this.id = id;
    }
    
	
	/**
	 * Creates a string based representation of this Print.
	
	 * @return String
	 */
	public String toString() {
		return "Print[" +set+", "+id+"]";
	}
	
	/**
	 * Internal constructor to create a Print from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    public Print(Map<String, Object> raw) {
        // TODO: Check that the data has the correct schema.
        // NOTE: It's much safer to check the Map for fields than to catch a runtime exception.
        try {
            this.set = raw.get("set").toString();
            this.id = Integer.parseInt(raw.get("id").toString());
        } catch (NullPointerException e) {
    		System.err.println("Could not convert the response to a Print; a field was missing.");
    		e.printStackTrace();
    	} catch (ClassCastException e) {
    		System.err.println("Could not convert the response to a Print; a field had the wrong structure.");
    		e.printStackTrace();
        }
    
	}	
}