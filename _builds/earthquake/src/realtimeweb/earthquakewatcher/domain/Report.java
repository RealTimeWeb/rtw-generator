package realtimeweb.earthquakewatcher.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;



import realtimeweb.earthquakewatcher.domain.Earthquake;
import realtimeweb.earthquakewatcher.domain.BoundingBox;

/**
 * Information about earthquakes matching certain criteria, including the area that they occurred.
 */
public class Report {
	
    private BoundingBox area;
    private ArrayList<Earthquake> earthquakes;
    private String title;
    
    
    /*
     * @return A region that contains all the earthquakes.
     */
    public BoundingBox getArea() {
        return this.area;
    }
    
    /*
     * @param A region that contains all the earthquakes.
     * @return BoundingBox
     */
    public void setArea(BoundingBox area) {
        this.area = area;
    }
    
    /*
     * @return A list of the earthquakes.
     */
    public ArrayList<Earthquake> getEarthquakes() {
        return this.earthquakes;
    }
    
    /*
     * @param A list of the earthquakes.
     * @return ArrayList<Earthquake>
     */
    public void setEarthquakes(ArrayList<Earthquake> earthquakes) {
        this.earthquakes = earthquakes;
    }
    
    /*
     * @return A human-readable title that describes this data.
     */
    public String getTitle() {
        return this.title;
    }
    
    /*
     * @param A human-readable title that describes this data.
     * @return String
     */
    public void setTitle(String title) {
        this.title = title;
    }
    
	
	/**
	 * Creates a string based representation of this Report.
	
	 * @return String
	 */
	public String toString() {
		return "Report[" +area+", "+earthquakes+", "+title+"]";
	}
	
	/**
	 * Internal constructor to create a Report from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    
    public Report(Map<String, Object> raw) {
        
        this.area = new BoundingBox(raw.get("bbox"));
        this.earthquakes = new ArrayList<Earthquake>();
        Iterator earthquakesIter = raw.get("features").iterator();
        while (earthquakesIter.hasNext()) {
            this.earthquakes.add(new Earthquake(earthquakesIter.next()));
        }
        this.title = ((Map<String, Object>) raw.get("metadata")).get("title").toString();
    
	}	
}