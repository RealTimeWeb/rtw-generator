package realtimeweb.earthquakewatcher.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;




/**
 * The longitudinal, latitudinal, and depth of the region required to display all the earthquakes.
 */
public class BoundingBox {
	
    // For some unclear reason, these are stored as a list instead of a dictionary.
    
    private Double minimumLongitude;
    private Double minimumLatitude;
    private Double minimumDepth;
    private Double maximumLongitude;
    private Double maximumLatitude;
    private Double maximumDepth;
    
    
    /*
     * @return The lower longitude (West) component.
     */
    public Double getMinimumLongitude() {
        return this.minimumLongitude;
    }
    
    /*
     * @param The lower longitude (West) component.
     * @return Double
     */
    public void setMinimumLongitude(Double minimumLongitude) {
        this.minimumLongitude = minimumLongitude;
    }
    
    /*
     * @return The lower latitude (South) component.
     */
    public Double getMinimumLatitude() {
        return this.minimumLatitude;
    }
    
    /*
     * @param The lower latitude (South) component.
     * @return Double
     */
    public void setMinimumLatitude(Double minimumLatitude) {
        this.minimumLatitude = minimumLatitude;
    }
    
    /*
     * @return The lower depth (closer or farther from the surface) component.
     */
    public Double getMinimumDepth() {
        return this.minimumDepth;
    }
    
    /*
     * @param The lower depth (closer or farther from the surface) component.
     * @return Double
     */
    public void setMinimumDepth(Double minimumDepth) {
        this.minimumDepth = minimumDepth;
    }
    
    /*
     * @return The higher longitude (East) component.
     */
    public Double getMaximumLongitude() {
        return this.maximumLongitude;
    }
    
    /*
     * @param The higher longitude (East) component.
     * @return Double
     */
    public void setMaximumLongitude(Double maximumLongitude) {
        this.maximumLongitude = maximumLongitude;
    }
    
    /*
     * @return The higher latitude (North) component.
     */
    public Double getMaximumLatitude() {
        return this.maximumLatitude;
    }
    
    /*
     * @param The higher latitude (North) component.
     * @return Double
     */
    public void setMaximumLatitude(Double maximumLatitude) {
        this.maximumLatitude = maximumLatitude;
    }
    
    /*
     * @return The higher depth (closer or farther from the surface) component.
     */
    public Double getMaximumDepth() {
        return this.maximumDepth;
    }
    
    /*
     * @param The higher depth (closer or farther from the surface) component.
     * @return Double
     */
    public void setMaximumDepth(Double maximumDepth) {
        this.maximumDepth = maximumDepth;
    }
    
	
	/**
	 * Creates a string based representation of this BoundingBox.
	
	 * @return String
	 */
	public String toString() {
		return "Report[" +minimumLongitude+", "+minimumLatitude+", "+minimumDepth+", "+maximumLongitude+", "+maximumLatitude+", "+maximumDepth+"]";
	}
	
	/**
	 * Internal constructor to create a BoundingBox from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    public BoundingBox(List<Object> raw) {
        // TODO: Check that the data has the correct schema.
        // NOTE: It's much safer to check the Map for fields than to catch a runtime exception.
        try {
            this.minimumLongitude = Double.parseDouble(raw.get(0).toString());
            this.minimumLatitude = Double.parseDouble(raw.get(1).toString());
            this.minimumDepth = Double.parseDouble(raw.get(2).toString());
            this.maximumLongitude = Double.parseDouble(raw.get(3).toString());
            this.maximumLatitude = Double.parseDouble(raw.get(4).toString());
            this.maximumDepth = Double.parseDouble(raw.get(5).toString());
        } catch (NullPointerException e) {
    		System.err.println("Could not convert the response to a BoundingBox; a field was missing.");
    		e.printStackTrace();
    	} catch (ClassCastException e) {
    		System.err.println("Could not convert the response to a BoundingBox; a field had the wrong structure.");
    		e.printStackTrace();
        }
    
	}	
}