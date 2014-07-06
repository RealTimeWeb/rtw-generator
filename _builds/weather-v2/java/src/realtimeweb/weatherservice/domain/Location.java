package realtimeweb.weatherservice.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;




/**
 * A detailed description of a location
 */
public class Location {
	
    private Double latitude;
    private Integer elavation;
    private String name;
    private Double longitude;
    
    
    /*
     * @return The latitude (up-down) of this location.
     */
    public Double getLatitude() {
        return this.latitude;
    }
    
    /*
     * @param The latitude (up-down) of this location.
     * @return Double
     */
    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }
    
    /*
     * @return The height above sea-level (in feet).
     */
    public Integer getElavation() {
        return this.elavation;
    }
    
    /*
     * @param The height above sea-level (in feet).
     * @return Integer
     */
    public void setElavation(Integer elavation) {
        this.elavation = elavation;
    }
    
    /*
     * @return The city and state that this location is in.
     */
    public String getName() {
        return this.name;
    }
    
    /*
     * @param The city and state that this location is in.
     * @return String
     */
    public void setName(String name) {
        this.name = name;
    }
    
    /*
     * @return The longitude (left-right) of this location.
     */
    public Double getLongitude() {
        return this.longitude;
    }
    
    /*
     * @param The longitude (left-right) of this location.
     * @return Double
     */
    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }
    
	
	/**
	 * Creates a string based representation of this Location.
	
	 * @return String
	 */
	public String toString() {
		return "Location[" +latitude+", "+elavation+", "+name+", "+longitude+"]";
	}
	
	/**
	 * Internal constructor to create a Location from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    public Location(Map<String, Object> raw) {
        // TODO: Check that the data has the correct schema.
        // NOTE: It's much safer to check the Map for fields than to catch a runtime exception.
        try {
            this.latitude = Double.parseDouble(raw.get("latitude").toString());
            this.elavation = Integer.parseInt(raw.get("elevation").toString());
            this.name = raw.get("areaDescription").toString();
            this.longitude = Double.parseDouble(raw.get("longitude").toString());
        } catch (NullPointerException e) {
    		System.err.println("Could not convert the response to a Location; a field was missing.");
    		e.printStackTrace();
    	} catch (ClassCastException e) {
    		System.err.println("Could not convert the response to a Location; a field had the wrong structure.");
    		e.printStackTrace();
        }
    
	}	
}