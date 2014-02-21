package realtimeweb.earthquakewatcher.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


/**
 * The longitudinal, latitudinal, and depth of the region required to display all the earthquakes.
 */
public class BoundingBox {
	
    // For some unclear reason, these are stored as a list instead of a dictionary.
    
    private Double maximumLongitude;
    private Double minimumLatitude;
    private Double minimumDepth;
    private Double minimumLongitude;
    private Double maximumDepth;
    private Double maximumLatitude;
    
    
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
    
	
	/**
	 * Creates a string based representation of this BoundingBox.
	
	 * @return String
	 */
	public String toString() {
		return "Report[" +maximumLongitude+", "+minimumLatitude+", "+minimumDepth+", "+minimumLongitude+", "+maximumDepth+", "+maximumLatitude+"]";
	}
	
	/**
	 * Internal constructor to create a BoundingBox from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    
    public BoundingBox(Map<String, Object> raw) {
        
        this.maximumLongitude = Double.parseDouble(raw.get("").get(0).toString());
        this.minimumLatitude = Double.parseDouble(raw.get("").get(1).toString());
        this.minimumDepth = Double.parseDouble(raw.get("").get(2).toString());
        this.minimumLongitude = Double.parseDouble(raw.get("").get(0).toString());
        this.maximumDepth = Double.parseDouble(raw.get("").get(2).toString());
        this.maximumLatitude = Double.parseDouble(raw.get("").get(1).toString());
    
	}	
}