package realtimeweb.earthquakewatcher;

import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.util.HashMap;

import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathFactory;

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
 * A short description
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
    }
    
    
    /**
     * Connects without any parameters
    
     * @return a My authors
     */
	public MyAuthors getSomeBooks() {
		final String url = String.format("http://www.w3schools.com/dom/books.xml");
		HashMap<String, String> parameters = new HashMap<String, String>();
        try {
			StickyWebRequest request = connection.get(url, parameters).setOnline(online);
            XPath xPath =  XPathFactory.newInstance().newXPath();
            return new MyAuthors(xPath.compile("/book/").evaluate(request.execute().asXML()));
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
    
    /**
     * Retrieves information about earthquakes around the world.
    
     * @param cache A string indicating the time range of earthquakes to report. Must be either "hour" (only earthquakes in the past hour), "day" (only earthquakes that happened today), "week" (only earthquakes that happened in the past 7 days), or "month" (only earthquakes that happened in the past 30 days).
     * @param cache A string indicating what kind of earthquakes to report. Must be either "significant" (only significant earthquakes), "all" (all earthquakes, regardless of significance), "4.5", "2.5", or "1.0". Note that for the last three, all earthquakes at and above that level will be reported.
     * @return a Report
     */
	public Report getEarthquakes(String time,String threshold) {
		final String url = String.format("http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/%s_%s.geojson", String.valueOf(time), String.valueOf(threshold));
		HashMap<String, String> parameters = new HashMap<String, String>();
        parameters.put("my_secret", "aaesfdiosjdfojkdfjl");try {
			StickyWebRequest request = connection.get(url, parameters).setOnline(online);
            // TODO: Might need to cast some intermediary steps
            return new Report(request.execute().asJSON()((Map<String, Object>) ((List<Object>) ((Map<String, Object>) ((Map<String, Object>) raw.get("book")).get("test")).get(3)).get("children")).get("data"));
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
    
    /**
     * Gets the first books
    
     * @return a integer
     */
	public Integer getFirstYear() {
		final String url = String.format("http://www.w3schools.com/dom/books.xml");
		HashMap<String, String> parameters = new HashMap<String, String>();
        try {
			StickyWebRequest request = connection.get(url, parameters).setOnline(online);
            XPath xPath =  XPathFactory.newInstance().newXPath();
            return new Integer(xPath.compile("/bookstore/book[0]/year").evaluate(request.execute().asXML()));
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