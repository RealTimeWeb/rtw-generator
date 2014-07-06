package realtimeweb.redditservice;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Map;

import realtimeweb.redditservice.domain.*;

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
 * Get the Front Page of the internet.
 */
public class RedditService {
    private StickyWeb connection;
	private boolean online;
    
    public static void main(String[] args) {
        RedditService redditService = new RedditService();
        
        // The following pre-generated code demonstrates how you can
		// use StickyWeb's EditableCache to create data files.
		try {
            // First, you create a new EditableCache, possibly passing in an existing cache to add to it
			EditableCache recording = new EditableCache();
			/*
             * // First you get a request object
			 * StickyWebRequest request = RedditService.getPostsRequest(...);
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
	public RedditService() {
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
	public RedditService(InputStream cache) {
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
    
    
    private StickyWebRequest getPostsRequest(String sortMode, String subreddit) {
        try {
            final String url = String.format("http://www.reddit.com/r/%s/%s.json", String.valueOf(subreddit), String.valueOf(sort mode));
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
     * Retrieves all the top posts
    
     * @param cache The order that the Posts will be sorted by. Options are: "top" (ranked by upvotes minus downvotes), "best" (similar to top, except that it uses a more complicated algorithm to have good posts jump to the top and stay there, and bad comments to work their way down, see http://blog.reddit.com/2009/10/reddits-new-comment-sorting-system.html), "hot" (similar to "top", but weighted by time so that recent, popular posts are put near the top), "new" (posts will be sorted by creation time).
     * @param cache The subreddit that Posts will be returned from (without the "r/" preceeding it). Use "all" to return results from all subreddits.
     * @return a Post[]
     */
	public ArrayList<Post> getPosts(String sortMode, String subreddit) {
        
        // Need to filter by data->children
        try {
			StickyWebRequest request =  getPostsRequest(sortMode, subreddit);
            
            ArrayList<Post> result = new ArrayList<Post>();
            StickyWebResponse response = request.execute();
            // TODO: Validate the output here using response.isNull, response.asText, etc.
            if (response.isNull())
                return result;
            Iterator<Object> resultIter = ((ArrayList<Object>) response.asJSONArray()).iterator();
            while (resultIter.hasNext()) {
                result.add(new Post((List<Object>)resultIter.next()));
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
    
    private StickyWebRequest getCommentsRequest(String sortMode, String id) {
        try {
            final String url = String.format("http://www.reddit.com/r/comments/%s/%s.json", String.valueOf(id), String.valueOf(sort mode));
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
     * Retrieves comments for a post
    
     * @param cache The order that the Posts will be sorted by. Options are: "top" (ranked by upvotes minus downvotes), "best" (similar to top, except that it uses a more complicated algorithm to have good posts jump to the top and stay there, and bad comments to work their way down, see http://blog.reddit.com/2009/10/reddits-new-comment-sorting-system.html), "hot" (similar to "top", but weighted by time so that recent, popular posts are put near the top), "new" (posts will be sorted by creation time).
     * @param cache The unique id of a Post from which Comments will be returned.
     * @return a Comment[]
     */
	public ArrayList<Comment> getComments(String sortMode, String id) {
        
        // Need to filter by data->children. Also, skip the first element, and the last element.
        try {
			StickyWebRequest request =  getCommentsRequest(sortMode, id);
            
            ArrayList<Comment> result = new ArrayList<Comment>();
            StickyWebResponse response = request.execute();
            // TODO: Validate the output here using response.isNull, response.asText, etc.
            if (response.isNull())
                return result;
            Iterator<Object> resultIter = ((ArrayList<Object>) response.asJSONArray()).iterator();
            while (resultIter.hasNext()) {
                result.add(new Comment((List<Object>)resultIter.next()));
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
    
}