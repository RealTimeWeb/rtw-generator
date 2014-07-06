package realtimeweb.earthquakewatcher.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;



import realtimeweb.earthquakewatcher.domain.Coordinate;

/**
 * Information about a specific earthquake.
 */
public class Earthquake {
	
    private Double maximumEstimatedIntensity;
    private Double distance;
    private String alertLevel;
    private Integer feltReports;
    private String locationDescription;
    private String url;
    private Long time;
    private Double rootMeanSquare;
    private String eventSource;
    private Double gap;
    private Double magnitude;
    private Coordinate location;
    private Integer significance;
    private Double maximumReportedIntensity;
    private String id;
    
    
    /*
     * @return The maximum estimated instrumental intensity for the event, or null if the data is not available. While typically reported as a roman numeral, intensity is reported here as the decimal equivalent. More information can be found at http://earthquake.usgs.gov/learn/topics/mag_vs_int.php
     */
    public Double getMaximumEstimatedIntensity() {
        return this.maximumEstimatedIntensity;
    }
    
    /*
     * @param The maximum estimated instrumental intensity for the event, or null if the data is not available. While typically reported as a roman numeral, intensity is reported here as the decimal equivalent. More information can be found at http://earthquake.usgs.gov/learn/topics/mag_vs_int.php
     * @return Double
     */
    public void setMaximumEstimatedIntensity(Double maximumEstimatedIntensity) {
        this.maximumEstimatedIntensity = maximumEstimatedIntensity;
    }
    
    /*
     * @return Horizontal distance from the epicenter to the nearest station (in degrees), or null if the data is not available. 1 degree is approximately 111.2 kilometers. In general, the smaller this number, the more reliable is the calculated depth of the earthquake.
     */
    public Double getDistance() {
        return this.distance;
    }
    
    /*
     * @param Horizontal distance from the epicenter to the nearest station (in degrees), or null if the data is not available. 1 degree is approximately 111.2 kilometers. In general, the smaller this number, the more reliable is the calculated depth of the earthquake.
     * @return Double
     */
    public void setDistance(Double distance) {
        this.distance = distance;
    }
    
    /*
     * @return A color string (one of "green", "yellow", "orange", "red") indicating how dangerous the quake was, or null if the data is not available. More information about this kind of alert is available at http://earthquake.usgs.gov/research/pager/
     */
    public String getAlertLevel() {
        return this.alertLevel;
    }
    
    /*
     * @param A color string (one of "green", "yellow", "orange", "red") indicating how dangerous the quake was, or null if the data is not available. More information about this kind of alert is available at http://earthquake.usgs.gov/research/pager/
     * @return String
     */
    public void setAlertLevel(String alertLevel) {
        this.alertLevel = alertLevel;
    }
    
    /*
     * @return The total number of "Felt" reports submitted, or null if the data is not available.
     */
    public Integer getFeltReports() {
        return this.feltReports;
    }
    
    /*
     * @param The total number of "Felt" reports submitted, or null if the data is not available.
     * @return Integer
     */
    public void setFeltReports(Integer feltReports) {
        this.feltReports = feltReports;
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
     * @return A webpage with more information about the earthquake.
     */
    public String getUrl() {
        return this.url;
    }
    
    /*
     * @param A webpage with more information about the earthquake.
     * @return String
     */
    public void setUrl(String url) {
        this.url = url;
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
    
    /*
     * @return The root-mean-square (RMS) travel time residual, in sec, using all weights. This parameter provides a measure of the fit of the observed arrival times to the predicted arrival times for this location. Smaller numbers reflect a better fit of the data. The value is dependent on the accuracy of the velocity model used to compute the earthquake location, the quality weights assigned to the arrival time data, and the procedure used to locate the earthquake.
     */
    public Double getRootMeanSquare() {
        return this.rootMeanSquare;
    }
    
    /*
     * @param The root-mean-square (RMS) travel time residual, in sec, using all weights. This parameter provides a measure of the fit of the observed arrival times to the predicted arrival times for this location. Smaller numbers reflect a better fit of the data. The value is dependent on the accuracy of the velocity model used to compute the earthquake location, the quality weights assigned to the arrival time data, and the procedure used to locate the earthquake.
     * @return Double
     */
    public void setRootMeanSquare(Double rootMeanSquare) {
        this.rootMeanSquare = rootMeanSquare;
    }
    
    /*
     * @return Either "AUTOMATIC", "PUBLISHED", or "REVIEWED". Indicates how the earthquake was identified and whether it was reviewed by a human.
     */
    public String getEventSource() {
        return this.eventSource;
    }
    
    /*
     * @param Either "AUTOMATIC", "PUBLISHED", or "REVIEWED". Indicates how the earthquake was identified and whether it was reviewed by a human.
     * @return String
     */
    public void setEventSource(String eventSource) {
        this.eventSource = eventSource;
    }
    
    /*
     * @return The largest azimuthal gap between azimuthally adjacent stations (in degrees), or null if the data is not available. In general, the smaller this number, the more reliable is the calculated horizontal position of the earthquake.
     */
    public Double getGap() {
        return this.gap;
    }
    
    /*
     * @param The largest azimuthal gap between azimuthally adjacent stations (in degrees), or null if the data is not available. In general, the smaller this number, the more reliable is the calculated horizontal position of the earthquake.
     * @return Double
     */
    public void setGap(Double gap) {
        this.gap = gap;
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
     * @return A number describing how significant the event is. Larger numbers indicate a more significant event. This value is determined on a number of factors, including: magnitude, maximum estimated intensity, felt reports, and estimated impact.
     */
    public Integer getSignificance() {
        return this.significance;
    }
    
    /*
     * @param A number describing how significant the event is. Larger numbers indicate a more significant event. This value is determined on a number of factors, including: magnitude, maximum estimated intensity, felt reports, and estimated impact.
     * @return Integer
     */
    public void setSignificance(Integer significance) {
        this.significance = significance;
    }
    
    /*
     * @return The maximum reported intensity for this earthquake, or null if the data is not available. While typically reported as a roman numeral, intensity is reported here as a decimal number. More information can be found at http://earthquake.usgs.gov/learn/topics/mag_vs_int.php
     */
    public Double getMaximumReportedIntensity() {
        return this.maximumReportedIntensity;
    }
    
    /*
     * @param The maximum reported intensity for this earthquake, or null if the data is not available. While typically reported as a roman numeral, intensity is reported here as a decimal number. More information can be found at http://earthquake.usgs.gov/learn/topics/mag_vs_int.php
     * @return Double
     */
    public void setMaximumReportedIntensity(Double maximumReportedIntensity) {
        this.maximumReportedIntensity = maximumReportedIntensity;
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
    
	
	/**
	 * Creates a string based representation of this Earthquake.
	
	 * @return String
	 */
	public String toString() {
		return "Report[" +maximumEstimatedIntensity+", "+distance+", "+alertLevel+", "+feltReports+", "+locationDescription+", "+url+", "+time+", "+rootMeanSquare+", "+eventSource+", "+gap+", "+magnitude+", "+location+", "+significance+", "+maximumReportedIntensity+", "+id+"]";
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
            this.maximumEstimatedIntensity = Double.parseDouble(((Map<String, Object>) raw.get("properties")).get("mmi").toString());
            this.distance = Double.parseDouble(((Map<String, Object>) raw.get("properties")).get("dmin").toString());
            this.alertLevel = ((Map<String, Object>) raw.get("properties")).get("alert").toString();
            this.feltReports = Integer.parseInt(((Map<String, Object>) raw.get("properties")).get("felt").toString());
            this.locationDescription = ((Map<String, Object>) raw.get("properties")).get("place").toString();
            this.url = ((Map<String, Object>) raw.get("properties")).get("url").toString();
            this.time = Long.parseLong(((Map<String, Object>) raw.get("properties")).get("time").toString());
            this.rootMeanSquare = Double.parseDouble(((Map<String, Object>) raw.get("properties")).get("rms").toString());
            this.eventSource = ((Map<String, Object>) raw.get("properties")).get("status").toString();
            this.gap = Double.parseDouble(((Map<String, Object>) raw.get("properties")).get("gap").toString());
            this.magnitude = Double.parseDouble(((Map<String, Object>) raw.get("properties")).get("mag").toString());
            this.location = new Coordinate((List<Object>)((Map<String, Object>) raw.get("geometry")).get("coordinates"));
            this.significance = Integer.parseInt(((Map<String, Object>) raw.get("properties")).get("sig").toString());
            this.maximumReportedIntensity = Double.parseDouble(((Map<String, Object>) raw.get("properties")).get("cdi").toString());
            this.id = raw.get("id").toString();
        } catch (NullPointerException e) {
    		System.err.println("Could not convert the response to a Earthquake; a field was missing.");
    		e.printStackTrace();
    	} catch (ClassCastException e) {
    		System.err.println("Could not convert the response to a Earthquake; a field had the wrong structure.");
    		e.printStackTrace();
        }
    
	}	
}