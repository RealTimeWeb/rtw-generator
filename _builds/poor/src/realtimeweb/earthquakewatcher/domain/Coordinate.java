package realtimeweb.earthquakewatcher.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;




/**
 * The longitudinal, latitudinal, and depth where the earthquake occurred.
 */
public class Coordinate {
	
    // For some unclear reason, these are stored as a list instead of a dictionary.
    
    private Double latitude;
    private Double depth;
    private Double longitude;
    
    
    /*
     * @return The latitude (South-North) component.
     */
    public Double getLatitude() {
        return this.latitude;
    }
    
    /*
     * @param The latitude (South-North) component.
     * @return Double
     */
    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }
    
    /*
     * @return The depth (closer or farther from the surface) component.
     */
    public Double getDepth() {
        return this.depth;
    }
    
    /*
     * @param The depth (closer or farther from the surface) component.
     * @return Double
     */
    public void setDepth(Double depth) {
        this.depth = depth;
    }
    
    /*
     * @return The longitude (West-North) component.
     */
    public Double getLongitude() {
        return this.longitude;
    }
    
    /*
     * @param The longitude (West-North) component.
     * @return Double
     */
    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }
    
	
	/**
	 * Creates a string based representation of this Coordinate.
	
	 * @return String
	 */
	public String toString() {
		return "Report[" +latitude+", "+depth+", "+longitude+"]";
	}
	
	/**
	 * Internal constructor to create a Coordinate from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    
    public Coordinate(Map<String, Object> raw) {
        
        this.latitude = Double.parseDouble(raw.get("").get(1).toString());
        this.depth = Double.parseDouble(raw.get("").get(2).toString());
        this.longitude = Double.parseDouble(raw.get("").get(0).toString());
    
	}	
}