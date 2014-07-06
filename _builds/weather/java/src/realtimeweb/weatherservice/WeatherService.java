package realtimeweb.weatherservice;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Map;

import realtimeweb.weatherservice.domain.*;

import realtimeweb.stickyweb.EditableCache;
import realtimeweb.stickyweb.StickyWeb;
import realtimeweb.stickyweb.StickyWebRequest;
import realtimeweb.stickyweb.StickyWebResponse;
import realtimeweb.stickyweb.exceptions.StickyWebDataSourceNotFoundException;
import realtimeweb.stickyweb.exceptions.StickyWebDataSourceParseException;
import realtimeweb.stickyweb.exceptions.StickyWebInternetException;
import realtimeweb.stickyweb.exceptions.StickyWebInvalidPostArguments;
import realtimeweb.stickyweb.exceptions.StickyWebInvalidQueryString;
import realtimeweb.stickyweb.exceptions.StickyWebJsonResponseParseException;
import realtimeweb.stickyweb.exceptions.StickyWebLoadDataSourceException;
import realtimeweb.stickyweb.exceptions.StickyWebNotInCacheException;

/**
 * Get a report of present weather and forecast data.
 */
public class WeatherService {
    private StickyWeb connection;
	private boolean online;
    
    public static void main(String[] args) {
        WeatherService weatherService = new WeatherService();
        
        // The following pre-generated code demonstrates how you can
		// use StickyWeb's EditableCache to create data files.
		try {
            // First, you create a new EditableCache, possibly passing in an existing cache to add to it
			EditableCache recording = new EditableCache();
			/*
             * // First you get a request object
			 * StickyWebRequest request = WeatherService.getReportRequest(...);
             * // Then you can get the request's hash and value, and add it to the EditableCache
			 * recording.addData(request.getHashedRequest(), request.execute().asText());
			 */
            // Then you can save the expanded cache over the original
			recording.saveToStream(new FileOutputStream("cache.json"));
		} catch (StickyWebDataSourceNotFoundException e) {
			System.err.println("The given FileStream was not able to be found.");
		} catch (StickyWebDataSourceParseException e) {
			System.err.println("The given FileStream could not be parsed; possibly the structure is incorrect.");
		} catch (StickyWebLoadDataSourceException e) {
			System.err.println("The given data source could not be loaded.");
		} catch (FileNotFoundException e) {
			System.err.println("The given cache.json file was not found, or could not be opened.");
		}
        // ** End of how to use the EditableCache
    }
	
    /**
     * Create a new, online connection to the service
     */
	public WeatherService() {
        this.online = true;
		try {
			this.connection = new StickyWeb(null);
		} catch (StickyWebDataSourceNotFoundException e) {
			System.err.println("The given datastream could not be loaded.");
		} catch (StickyWebDataSourceParseException e) {
			System.err.println("The given datastream could not be parsed");
		} catch (StickyWebLoadDataSourceException e) {
			System.err.println("The given data source could not be loaded");
		}
	}
	
    /**
     * Create a new, offline connection to the service.
     * @param cache An InputStream that can serve data for the connection.
     */
	public WeatherService(InputStream cache) {
        try {
            this.online = false;
            this.connection = new StickyWeb(cache);
        } catch (StickyWebDataSourceNotFoundException e) {
			System.err.println("The given data source could not be found.");
		} catch (StickyWebDataSourceParseException e) {
			System.err.println("Could not read the data source. Perhaps its format is incorrect?");
		} catch (StickyWebLoadDataSourceException e) {
			System.err.println("The given data source could not be read.");
		}
	}
    
    
    private StickyWebRequest getReportRequest(Double latitude, Double longitude) {
        try {
            final String url = String.format("http://forecast.weather.gov/MapClick.php");
            HashMap<String, String> parameters = new HashMap<String, String>();
            // TODO: Validate the inputs here
            parameters.put("lat", String.valueOf(latitude));parameters.put("FcstType", "json");
            parameters.put("lon", String.valueOf(longitude));
            ArrayList<String> indexList = new ArrayList<String>();
            indexList.add("lat");
            indexList.add("FcstType");
            indexList.add("lon");
            
            return connection.get(url, parameters)
                            .setOnline(online)
                            .setIndexes(indexList);
        } catch (StickyWebDataSourceNotFoundException e) {
			System.err.println("Could not find the data source.");
		}
        return null;
    }
    
    /**
     * Gets a report on the current weather, forecast, and more detailed information about the location.
    
     * @param cache The latitude (up-down) of the location to get information about.
     * @param cache The longitude (left-right) of the location to get information about.
     * @return a Report
     */
	public Report getReport(Double latitude, Double longitude) {
        try {
			StickyWebRequest request =  getReportRequest(latitude, longitude);
            
            return new Report(request.execute().asJSON());
		} catch (StickyWebNotInCacheException e) {
			System.err.println("There is no query in the cache for the given inputs. Perhaps something was mispelled?");
		} catch (StickyWebInternetException e) {
			System.err.println("Could not connect to the web service. It might be your internet connection, or a problem with the web service.");
		} catch (StickyWebInvalidQueryString e) {
			System.err.println("The given arguments were invalid, and could not be turned into a query.");
		} catch (StickyWebInvalidPostArguments e) {
			System.err.println("The given arguments were invalid, and could not be turned into a query.");
        
        } catch (StickyWebJsonResponseParseException e) {
            System.err.println("The response from the server couldn't be understood.");
        
		}
		return null;
	}
    
}