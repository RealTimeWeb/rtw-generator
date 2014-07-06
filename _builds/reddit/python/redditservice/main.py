import requests
import json

def _recursively_convert_unicode_to_str(input):
    if isinstance(input, dict):
        return {_recursively_convert_unicode_to_str(key): _recursively_convert_unicode_to_str(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [_recursively_convert_unicode_to_str(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def _from_json(data):
    return _recursively_convert_unicode_to_str(json.loads(data))
        
_CACHE = {}
_CACHE_COUNTER = {}
_CONNECTED = False
def connect():
    """
    Connect to the online data source in order to get up-to-date information.
    :returns: void
    """
    _CONNECTED = True
def disconnect(filename="cache.json"):
    """
    Connect to the local cache, so no internet connection is required.
    :returns: void
    """
    _CACHE = _recursively_convert_unicode_to_str(json.load(open(filename, r)))
    for key in CACHE.keys():
        _CACHE_COUNTER[key] = 0
        _CACHE_PATTERN[key] = _CACHE[key][0]
        _CACHE_DATA[key] = _CACHE[key][1:]
    _CONNECTED = False
def lookup(key):
    """
    Internal method that looks up a key in the local cache.
    :param key: Get the value based on the key from the cache.
    :type key: string
    :returns: void
    """
    if _CACHE_COUNTER[key] >= len(_CACHE[key][1:]):
        if _CACHE[key][0] == "empty":
            return ""
        elif _CACHE[key][0] == "repeat" and _CACHE[key][1:]:
            return _CACHE[key][-1]
        elif _CACHE[key][0] == "repeat":
            return ""
        else:
            _CACHE_COUNTER[key] = 0
    else:
        _CACHE_COUNTER[key] += 1
    if _CACHE[key]:
        return _CACHE[key][1+_CACHE_COUNTER]
    else:
        return ""
    
def _save_cache(filename="cache.json"):
    json.dump(_CACHE, filename)
    

class Comment(object):
	"""
	A Comment on either a Post or another Comment.
	"""
	def __init__(self, body, created, downs, author, subreddit, body_html, replies, id, ups):
		"""
		Creates a new Comment.
        
        :param self: This object
        :type self: Comment
        :param body: The text of this post, without any markup.
        :type body: str
        :param created: The date that this Comment was created.
        :type created: int
        :param downs: The number of downvotes associated with this Comment.
        :type downs: int
        :param author: The username of the author of this Post.
        :type author: str
        :param subreddit: The subreddit that this Comment was made in.
        :type subreddit: str
        :param body_html: The HTML text of this post.
        :type body_html: str
        :param replies: A list of comments that are in reply to this one.
        :type replies: list of Comment
        :param id: A unique ID for this Comment. A combination of letters, numbers, and dashes.
        :type id: str
        :param ups: The number of upvotes associated with this Comment.
        :type ups: int
        :returns: Comment
		"""
        self.body = body
        self.created = created
        self.downs = downs
        self.author = author
        self.subreddit = subreddit
        self.body_html = body_html
        self.replies = replies
        self.id = id
        self.ups = ups
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Comment from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Comment
		"""
		return Comment(json_data['data']['body'],
                       json_data['data']['created'],
                       json_data['data']['downs'],
                       json_data['data']['author'],
                       json_data['data']['subreddit'],
                       json_data['data']['body_html'],
                       map(Comment._from_json, json_data['data']['replies']['data']['children']),
                       json_data['data']['id'],
                       json_data['data']['ups'])

class Post(object):
	"""
	A link (or self-text) that has been submitted to Reddit.
	"""
	def __init__(self, permalink, author, title, downs, created, subreddit, content, is_self, id, ups, is_nsfw):
		"""
		Creates a new Post.
        
        :param self: This object
        :type self: Post
        :param permalink: A permanent url that directs to this Post.
        :type permalink: str
        :param author: The username of the author of this Post.
        :type author: str
        :param title: The title of this Post.
        :type title: str
        :param downs: The number of downvotes associated with this Post.
        :type downs: int
        :param created: The date that this Post was created.
        :type created: int
        :param subreddit: The subreddit that this Post was made in.
        :type subreddit: str
        :param content: The text of the post, or a url if it is not a self Post.
        :type content: str
        :param is_self: Whether or not this Post was text (True), or a URL (False).
        :type is_self: boolean
        :param id: A unique ID for this Post. A combination of letters, numbers, and dashes.
        :type id: str
        :param ups: The number of upvotes associated with this Post.
        :type ups: int
        :param is_nsfw: Whether or not this Post is Not Safe for Work (NSFW).
        :type is_nsfw: boolean
        :returns: Post
		"""
        self.permalink = permalink
        self.author = author
        self.title = title
        self.downs = downs
        self.created = created
        self.subreddit = subreddit
        self.content = content
        self.is_self = is_self
        self.id = id
        self.ups = ups
        self.is_nsfw = is_nsfw
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Post from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Post
		"""
		return Post(json_data['data']['permalink'],
                       json_data['data']['author'],
                       json_data['data']['title'],
                       json_data['data']['downs'],
                       json_data['data']['created'],
                       json_data['data']['subreddit'],
                       json_data['data']['selftext'],
                       json_data['data']['is_self'],
                       json_data['data']['id'],
                       json_data['data']['ups'],
                       json_data['data']['over_18'])

    

def _get_posts_request(sort_mode,subreddit):
    """
    Used to build the request string used by :func:`get_posts`.
    
    
    :param sort_mode: The order that the Posts will be sorted by. Options are: "top" (ranked by upvotes minus downvotes), "best" (similar to top, except that it uses a more complicated algorithm to have good posts jump to the top and stay there, and bad comments to work their way down, see http://blog.reddit.com/2009/10/reddits-new-comment-sorting-system.html), "hot" (similar to "top", but weighted by time so that recent, popular posts are put near the top), "new" (posts will be sorted by creation time).
    :type sort_mode: str
    
    :param subreddit: The subreddit that Posts will be returned from (without the "r/" preceeding it). Use "all" to return results from all subreddits.
    :type subreddit: str
    :returns: str
    """
    key = "http://www.reddit.com/r/{}/{}.json".format(subreddit,sort_mode)
    key += "?" + "".join([])
    return key

def _get_posts_string(sort_mode,subreddit):
    """
    Like :func:`get_posts` except returns the raw data instead.
    
    
    :param sort_mode: The order that the Posts will be sorted by. Options are: "top" (ranked by upvotes minus downvotes), "best" (similar to top, except that it uses a more complicated algorithm to have good posts jump to the top and stay there, and bad comments to work their way down, see http://blog.reddit.com/2009/10/reddits-new-comment-sorting-system.html), "hot" (similar to "top", but weighted by time so that recent, popular posts are put near the top), "new" (posts will be sorted by creation time).
    :type sort_mode: str
    
    :param subreddit: The subreddit that Posts will be returned from (without the "r/" preceeding it). Use "all" to return results from all subreddits.
    :type subreddit: str
    :returns: str
    """
    if _CONNECTED:
        key = "http://www.reddit.com/r/{}/{}.json".format(subreddit,sort_mode)
        result = requests.get(key, params = { ) }).text
    else:
        key = _get_posts_request(sort_mode,subreddit)
        result = lookup(key)
    return result

def get_posts(sort_mode,subreddit):
    """
    Retrieves all the top posts
    
    
    :param sort_mode: The order that the Posts will be sorted by. Options are: "top" (ranked by upvotes minus downvotes), "best" (similar to top, except that it uses a more complicated algorithm to have good posts jump to the top and stay there, and bad comments to work their way down, see http://blog.reddit.com/2009/10/reddits-new-comment-sorting-system.html), "hot" (similar to "top", but weighted by time so that recent, popular posts are put near the top), "new" (posts will be sorted by creation time).
    :type sort_mode: str
    
    :param subreddit: The subreddit that Posts will be returned from (without the "r/" preceeding it). Use "all" to return results from all subreddits.
    :type subreddit: str
    :returns: list of Post
    """
    result = _get_posts_string(sort_mode,subreddit)
    
    return map(list of Post._from_json, _from_json(result))
    

def _get_comments_request(sort_mode,id):
    """
    Used to build the request string used by :func:`get_comments`.
    
    
    :param sort_mode: The order that the Posts will be sorted by. Options are: "top" (ranked by upvotes minus downvotes), "best" (similar to top, except that it uses a more complicated algorithm to have good posts jump to the top and stay there, and bad comments to work their way down, see http://blog.reddit.com/2009/10/reddits-new-comment-sorting-system.html), "hot" (similar to "top", but weighted by time so that recent, popular posts are put near the top), "new" (posts will be sorted by creation time).
    :type sort_mode: str
    
    :param id: The unique id of a Post from which Comments will be returned.
    :type id: str
    :returns: str
    """
    key = "http://www.reddit.com/r/comments/{}/{}.json".format(id,sort_mode)
    key += "?" + "".join([])
    return key

def _get_comments_string(sort_mode,id):
    """
    Like :func:`get_comments` except returns the raw data instead.
    
    
    :param sort_mode: The order that the Posts will be sorted by. Options are: "top" (ranked by upvotes minus downvotes), "best" (similar to top, except that it uses a more complicated algorithm to have good posts jump to the top and stay there, and bad comments to work their way down, see http://blog.reddit.com/2009/10/reddits-new-comment-sorting-system.html), "hot" (similar to "top", but weighted by time so that recent, popular posts are put near the top), "new" (posts will be sorted by creation time).
    :type sort_mode: str
    
    :param id: The unique id of a Post from which Comments will be returned.
    :type id: str
    :returns: str
    """
    if _CONNECTED:
        key = "http://www.reddit.com/r/comments/{}/{}.json".format(id,sort_mode)
        result = requests.get(key, params = { ) }).text
    else:
        key = _get_comments_request(sort_mode,id)
        result = lookup(key)
    return result

def get_comments(sort_mode,id):
    """
    Retrieves comments for a post
    
    
    :param sort_mode: The order that the Posts will be sorted by. Options are: "top" (ranked by upvotes minus downvotes), "best" (similar to top, except that it uses a more complicated algorithm to have good posts jump to the top and stay there, and bad comments to work their way down, see http://blog.reddit.com/2009/10/reddits-new-comment-sorting-system.html), "hot" (similar to "top", but weighted by time so that recent, popular posts are put near the top), "new" (posts will be sorted by creation time).
    :type sort_mode: str
    
    :param id: The unique id of a Post from which Comments will be returned.
    :type id: str
    :returns: list of Comment
    """
    result = _get_comments_string(sort_mode,id)
    
    return map(list of Comment._from_json, _from_json(result))
    
