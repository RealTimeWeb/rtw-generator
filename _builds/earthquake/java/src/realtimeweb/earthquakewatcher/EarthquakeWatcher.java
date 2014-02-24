package realtimeweb.earthquakewatcher;

import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.util.HashMap;



import realtimeweb.earthquakewatcher.domain.*;
import realtimeweb.stickyweb.StickyWeb;
import realtimeweb.stickyweb.StickyWebRequest;
import realtimeweb.stickyweb.exceptions.StickyWebException;
import realtimeweb.stickyweb.exceptions.StickyWebDataSourceNotFoundException;
import realtimeweb.stickyweb.exceptions.StickyWebDataSourceParseException;
import realtimeweb.stickyweb.exceptions.StickyWebInternetException;
import realtimeweb.stickyweb.exceptions.StickyWebJsonResponseParseException;
import realtimeweb.stickyweb.exceptions.StickyWebLoadDataSourceException;
import realtimeweb.stickyweb.exceptions.StickyWebNotInCacheException;

/**
 * Get the latest information about earthquakes around the world.
 */
public class EarthquakeWatcher {
    private StickyWeb connection;
	private boolean online;
	
    /**
     * Create a new, online connection to the service
     */
	public EarthquakeWatcher() {
		this.online = true;
		try {
			this.connection = new StickyWeb(null);
		} catch (StickyWebDataSourceNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (StickyWebDataSourceParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (StickyWebLoadDataSourceException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
    /**
     * Create a new, offline connection to the service.
     * @param cache An InputStream that can serve data for the connection.
     */
	public EarthquakeWatcher(InputStream cache) throws StickyWebDataSourceNotFoundException, StickyWebDataSourceParseException, StickyWebLoadDataSourceException {
		this.online = false;
		this.connection = new StickyWeb(cache);
	}
    
    public static void main(String[] args) {
        EarthquakeWatcher earthquakeWatcher = new EarthquakeWatcher();
        System.out.println(earthquakeWatcher.getEarthquakes("all", "hour"));
    }
    
    
    /**
     * Retrieves information about earthquakes around the world.
    
     * @param cache A string indicating what kind of earthquakes to report. Must be either "significant" (only significant earthquakes), "all" (all earthquakes, regardless of significance), "4.5", "2.5", or "1.0". Note that for the last three, all earthquakes at and above that level will be reported.
     * @param cache A string indicating the time range of earthquakes to report. Must be either "hour" (only earthquakes in the past hour), "day" (only earthquakes that happened today), "week" (only earthquakes that happened in the past 7 days), or "month" (only earthquakes that happened in the past 30 days).
     * @return a Report
     */
	public Report getEarthquakes(String threshold,String time) {
		final String url = String.format("http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/%s_%s.geojson", String.valueOf(threshold), String.valueOf(time));
		HashMap<String, String> parameters = new HashMap<String, String>();
        try {
			StickyWebRequest request = connection.get(url, parameters).setOnline(online);
            // TODO: Might need to cast some intermediary steps
            return new Report(request.execute().asJSON());
		} catch (IllegalStateException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (URISyntaxException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (StickyWebException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}
    
}