package realtimeweb.magicthegatheringservice;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Map;

import realtimeweb.magicthegatheringservice.domain.*;

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
 * Access information about Magic the Gathering Cards.
 */
public class MagicTheGatheringService {
    private StickyWeb connection;
	private boolean online;
    
    public static void main(String[] args) {
        MagicTheGatheringService magicTheGatheringService = new MagicTheGatheringService();
        System.out.println(magicTheGatheringService.getCard(1));
        
        // The following pre-generated code demonstrates how you can
		// use StickyWeb's EditableCache to create data files.
		try {
            // First, you create a new EditableCache, possibly passing in an existing cache to add to it
			EditableCache recording = new EditableCache();
			/*
             * // First you get a request object
			 * StickyWebRequest request = MagicTheGatheringService.searchCardsRequest(...);
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
	public MagicTheGatheringService() {
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
     * @param cache The filename of the cache to be used.
     */
	public MagicTheGatheringService(String cache) {
        // TODO: You might consider putting the cache directly into the jar file,
        // and not even exposing filenames!
        try {
            this.online = false;
            this.connection = new StickyWeb(new FileInputStream(cache));
        } catch (StickyWebDataSourceNotFoundException e) {
			System.err.println("The given data source could not be found.");
            System.exit(1);
		} catch (StickyWebDataSourceParseException e) {
			System.err.println("Could not read the data source. Perhaps its format is incorrect?");
            System.exit(1);
		} catch (StickyWebLoadDataSourceException e) {
			System.err.println("The given data source could not be read.");
			System.exit(1);
		} catch (FileNotFoundException e) {
			System.err.println("The given cache file could not be found. Make sure it is in the right folder.");
			System.exit(1);
		}
	}
    
    
    private StickyWebRequest searchCardsRequest(String keyword) {
        try {
            final String url = String.format("http://api.mtgapi.com/v1/card/name/%s", String.valueOf(keyword));
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
     * Searches the database for cards with the keyword in the card's name.
    
     * @param cache The keyword to match against card's names
     * @return a card result[]
     */
	public ArrayList<CardResult> searchCards(String keyword) {
        
        // If it doesn't work, then returns the JSON response{"code":404,"message":"This page does not exist."}
        try {
			StickyWebRequest request =  searchCardsRequest(keyword);
            
            ArrayList<CardResult> result = new ArrayList<CardResult>();
            StickyWebResponse response = request.execute();
            // TODO: Validate the output here using response.isNull, response.asText, etc.
            if (response.isNull())
                return result;
            Iterator<Object> resultIter = ((ArrayList<Object>) response.asJSONArray()).iterator();
            while (resultIter.hasNext()) {
                result.add(new CardResult((Map<String, Object>)resultIter.next()));
            }
            return result;
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
    
    private StickyWebRequest getCardRequest(Integer id) {
        try {
            final String url = String.format("http://api.mtgapi.com/v1/card/id/%s", String.valueOf(id));
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
     * Retrieves a card by looking up its ID.
    
     * @param cache The unique id number of the card.
     * @return a card
     */
	public Card getCard(Integer id) {
        
        // If the ID doesn't exist, it returns the json response{"code":404,"message":"This page does not exist."}
        try {
			StickyWebRequest request =  getCardRequest(id);
            return new Card((Map<String, Object>)request.execute().asJSONArray().get(0));
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