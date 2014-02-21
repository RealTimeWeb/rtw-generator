package realtimeweb.weatherservice;

import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.util.HashMap;



import realtimeweb.weatherservice.domain.*;
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
 * Get a report of present weather and forecast data.
 */
public class WeatherService {
    private StickyWeb connection;
	private boolean online;
	
    /**
     * Create a new, online connection to the service
     */
	public WeatherService() {
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
	public WeatherService(InputStream cache) throws StickyWebDataSourceNotFoundException, StickyWebDataSourceParseException, StickyWebLoadDataSourceException {
		this.online = false;
		this.connection = new StickyWeb(cache);
	}
    
    public static void main(String[] args) {
        WeatherService weatherService = new WeatherService();
    }
    
    
    /**
     * Gets a report on the current weather, forecast, and more detailed information about the location.
    
     * @param cache The latitude (up-down) of the location to get information about.
     * @param cache The longitude (left-right) of the location to get information about.
     * @return a Report
     */
	public Report getReport(Double latitude,Double longitude) {
		final String url = String.format("http://forecast.weather.gov/MapClick.php");
		HashMap<String, String> parameters = new HashMap<String, String>();
        parameters.put("lat", String.valueOf(latitude));parameters.put("FcstType", "json");parameters.put("lon", String.valueOf(longitude));try {
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