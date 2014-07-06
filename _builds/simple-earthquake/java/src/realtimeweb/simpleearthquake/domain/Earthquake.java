package realtimeweb.simpleearthquake.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;



import realtimeweb.simpleearthquake.domain.Coordinate;

/**
 * Information about a specific earthquake.
 */
public class Earthquake {
	
    private Coordinate location;
    private Double magnitude;
    private String locationDescription;
    private String id;
    private Long time;
    
    
    /*
     * @return The location of the earthquake.
     */
    public Coordinate getLocation() {
        return this.location;
    }
    
    /*
     * @param The location of the earthquake.
     * @return Coordinate
     */
    public void setLocation(Coordinate location) {
        this.location = location;
    }
    
    /*
     * @return The magnitude of the earthquake on the Richter Scale.
     */
    public Double getMagnitude() {
        return this.magnitude;
    }
    
    /*
     * @param The magnitude of the earthquake on the Richter Scale.
     * @return Double
     */
    public void setMagnitude(Double magnitude) {
        this.magnitude = magnitude;
    }
    
    /*
     * @return A human-readable description of the location.
     */
    public String getLocationDescription() {
        return this.locationDescription;
    }
    
    /*
     * @param A human-readable description of the location.
     * @return String
     */
    public void setLocationDescription(String locationDescription) {
        this.locationDescription = locationDescription;
    }
    
    /*
     * @return A uniquely identifying id for this earthquake.
     */
    public String getId() {
        return this.id;
    }
    
    /*
     * @param A uniquely identifying id for this earthquake.
     * @return String
     */
    public void setId(String id) {
        this.id = id;
    }
    
    /*
     * @return The epoch time (http://en.wikipedia.org/wiki/Unix_time) when this earthquake occurred.
     */
    public Long getTime() {
        return this.time;
    }
    
    /*
     * @param The epoch time (http://en.wikipedia.org/wiki/Unix_time) when this earthquake occurred.
     * @return Long
     */
    public void setTime(Long time) {
        this.time = time;
    }
    
	
	/**
	 * Creates a string based representation of this Earthquake.
	
	 * @return String
	 */
	public String toString() {
		return "Report[" +location+", "+magnitude+", "+locationDescription+", "+id+", "+time+"]";
	}
	
	/**
	 * Internal constructor to create a Earthquake from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    public Earthquake(Map<String, Object> raw) {
        // TODO: Check that the data has the correct schema.
        // NOTE: It's much safer to check the Map for fields than to catch a runtime exception.
        try {
            this.location = new Coordinate((List<Object>)((Map<String, Object>) raw.get("geometry")).get("coordinates"));
            this.magnitude = Double.parseDouble(((Map<String, Object>) raw.get("properties")).get("mag").toString());
            this.locationDescription = ((Map<String, Object>) raw.get("properties")).get("place").toString();
            this.id = raw.get("id").toString();
            this.time = Long.parseLong(((Map<String, Object>) raw.get("properties")).get("time").toString());
        } catch (NullPointerException e) {
    		System.err.println("Could not convert the response to a Earthquake; a field was missing.");
    		e.printStackTrace();
    	} catch (ClassCastException e) {
    		System.err.println("Could not convert the response to a Earthquake; a field had the wrong structure.");
    		e.printStackTrace();
        }
    
	}	
}