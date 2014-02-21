package realtimeweb.weatherservice.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;



import realtimeweb.weatherservice.domain.Weather;
import realtimeweb.weatherservice.domain.Location;
import realtimeweb.weatherservice.domain.Forecast;

/**
 * A container for the weather, forecasts, and location information.
 */
public class Report {
	
    private Weather weather;
    private Location location;
    private ArrayList<Forecast> forecasts;
    
    
    /*
     * @return The current weather for this location.
     */
    public Weather getWeather() {
        return this.weather;
    }
    
    /*
     * @param The current weather for this location.
     * @return Weather
     */
    public void setWeather(Weather weather) {
        this.weather = weather;
    }
    
    /*
     * @return More detailed information on this location.
     */
    public Location getLocation() {
        return this.location;
    }
    
    /*
     * @param More detailed information on this location.
     * @return Location
     */
    public void setLocation(Location location) {
        this.location = location;
    }
    
    /*
     * @return The forecast for the next 7 days and 7 nights.
     */
    public ArrayList<Forecast> getForecasts() {
        return this.forecasts;
    }
    
    /*
     * @param The forecast for the next 7 days and 7 nights.
     * @return ArrayList<Forecast>
     */
    public void setForecasts(ArrayList<Forecast> forecasts) {
        this.forecasts = forecasts;
    }
    
	
	/**
	 * Creates a string based representation of this Report.
	
	 * @return String
	 */
	public String toString() {
		return "Report[" +weather+", "+location+", "+forecasts+"]";
	}
	
	/**
	 * Internal constructor to create a Report from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    
    public Report(Map<String, Object> raw) {
        
        this.weather = new Weather((Map<String, Object>)raw.get("currentobservation"));
        this.location = new Location((Map<String, Object>)raw.get("location"));
        this.forecasts = new ArrayList<Forecast>();
        Iterator<Forecast> forecastsIter = ((List<Forecast>)raw).iterator();
        while (forecastsIter.hasNext()) {
            this.forecasts.add(new Forecast((Map<String, Object>)forecastsIter.next()));
        }
    
	}	
}