package realtimeweb.earthquakewatcher;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Map;

import realtimeweb.earthquakewatcher.domain.*;

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
 * Get the latest information about earthquakes around the world.
 */
public class EarthquakeWatcher {
    private StickyWeb connection;
	private boolean online;
    
    public static void main(String[] args) {
        EarthquakeWatcher earthquakeWatcher = new EarthquakeWatcher();
        
        // The following pre-generated code demonstrates how you can
		// use StickyWeb's EditableCache to create data files.
		try {
            // First, you create a new EditableCache, possibly passing in an existing cache to add to it
			EditableCache recording = new EditableCache();
			/*
             * // First you get a request object
			 * StickyWebRequest request = EarthquakeWatcher.getEarthquakesRequest(...);
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
	public EarthquakeWatcher() {
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
	public EarthquakeWatcher(InputStream cache) {
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
    
    
    private StickyWebRequest getEarthquakesRequest(String threshold, String time) {
        try {
            final String url = String.format("http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/%s_%s.geojson", String.valueOf(threshold), String.valueOf(time));
            HashMap<String, String> parameters = new HashMap<String, String>();
            // TODO: Validate the inputs here
            ArrayList<String> indexList = new ArrayList<String>();
            
            return connection.get(url, parameters)
                            .setOnline(online)
                            .setIndexes(indexList);
        } catch (StickyWebDataSourceNotFoundException e) {
			System.err.println("Could not find the data source.");
		}
        return null;
    }
    
    /**
     * Retrieves information about earthquakes around the world.
    
     * @param cache A string indicating what kind of earthquakes to report. Must be either "significant" (only significant earthquakes), "all" (all earthquakes, regardless of significance), "4.5", "2.5", or "1.0". Note that for the last three, all earthquakes at and above that level will be reported.
     * @param cache A string indicating the time range of earthquakes to report. Must be either "hour" (only earthquakes in the past hour), "day" (only earthquakes that happened today), "week" (only earthquakes that happened in the past 7 days), or "month" (only earthquakes that happened in the past 30 days).
     * @return a Report
     */
	public Report getEarthquakes(String threshold, String time) {
        
        // Should really make these enums
        try {
			StickyWebRequest request =  getEarthquakesRequest(threshold, time);
            
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