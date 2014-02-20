package realtimeweb.earthquakewatcher;

import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.util.HashMap;

import realtimeweb.earthquakewatcher.domain.*;
import realtimeweb.stickyweb.Pattern;
import realtimeweb.stickyweb.StickyWeb;
import realtimeweb.stickyweb.StickyWebRequest;
import realtimeweb.stickyweb.exceptions.StickyWebDataSourceNotFoundException;
import realtimeweb.stickyweb.exceptions.StickyWebDataSourceParseException;
import realtimeweb.stickyweb.exceptions.StickyWebInternetException;
import realtimeweb.stickyweb.exceptions.StickyWebJsonResponseParseException;
import realtimeweb.stickyweb.exceptions.StickyWebLoadDataSourceException;
import realtimeweb.stickyweb.exceptions.StickyWebNotInCacheException;

public class EarthquakeWatcher {
	private StickyWeb connection;
	private boolean online;
	
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
	
	public EarthquakeWatcher(InputStream cache) throws StickyWebDataSourceNotFoundException, StickyWebDataSourceParseException, StickyWebLoadDataSourceException {
		this.online = false;
		this.connection = new StickyWeb(cache);
	}
    
    
	public MyAuthors getSomeBooks() {
		final String url = String.format("http://www.w3schools.com/dom/books.xml");
		HashMap<String, String> parameters = new HashMap<String, String>();
        
		parameters.put("lat", String.valueOf(latitude));
		parameters.put("lon", String.valueOf(longitude));
		parameters.put("FcstType", String.valueOf("json"));
		
		try {
			StickyWebRequest request = connection.get(url, parameters)
					.setOnline(online)
					.setPattern(Pattern.EMPTY);
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
    
    
	public Report getEarthquakes(String time,String threshold) {
		final String url = String.format("http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/%s_%s.geojson", String.valueOf(time), String.valueOf(threshold));
		HashMap<String, String> parameters = new HashMap<String, String>();
        
        parameters.put(secret, String.valueOf(my_secret));
        
		parameters.put("lat", String.valueOf(latitude));
		parameters.put("lon", String.valueOf(longitude));
		parameters.put("FcstType", String.valueOf("json"));
		
		try {
			StickyWebRequest request = connection.get(url, parameters)
					.setOnline(online)
					.setPattern(Pattern.EMPTY);
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
    
    
	
	public static void main(String args[]) {
		Weather weather = new Weather();
		Report saved = weather.getWeather(37, -80);
	}
}