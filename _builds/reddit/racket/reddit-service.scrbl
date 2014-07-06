#lang scribble/manual
 
@title{ reddit-service }
@author{+email "Cory Bart" "acbart@vt.edu"}

@section{Structs}
 
Get the Front Page of the internet.


@defproc[(make-comment
    [body string?]
    [created integer?]
    [downs integer?]
    [author string?]
    [subreddit string?]
    [body-html string?]
    [replies (listof comment?]
    [id string?]
    [ups integer?]
    comment]{
        A Comment on either a Post or another Comment.
        @itemlist[
            @item{@racket[body] --- The text of this post, without any markup. }
            @item{@racket[created] --- The date that this Comment was created. }
            @item{@racket[downs] --- The number of downvotes associated with this Comment. }
            @item{@racket[author] --- The username of the author of this Post. }
            @item{@racket[subreddit] --- The subreddit that this Comment was made in. }
            @item{@racket[body-html] --- The HTML text of this post. }
            @item{@racket[replies] --- A list of comments that are in reply to this one. }
            @item{@racket[id] --- A unique ID for this Comment. A combination of letters, numbers, and dashes. }
            @item{@racket[ups] --- The number of upvotes associated with this Comment. }
            
        ]}

@defproc[(make-post
    [permalink string?]
    [author string?]
    [title string?]
    [downs integer?]
    [created integer?]
    [subreddit string?]
    [content string?]
    [is-self boolean?]
    [id string?]
    [ups integer?]
    [is-nsfw boolean?]
    post]{
        A link (or self-text) that has been submitted to Reddit.
        @itemlist[
            @item{@racket[permalink] --- A permanent url that directs to this Post. }
            @item{@racket[author] --- The username of the author of this Post. }
            @item{@racket[title] --- The title of this Post. }
            @item{@racket[downs] --- The number of downvotes associated with this Post. }
            @item{@racket[created] --- The date that this Post was created. }
            @item{@racket[subreddit] --- The subreddit that this Post was made in. }
            @item{@racket[content] --- The text of the post, or a url if it is not a self Post. }
            @item{@racket[is-self] --- Whether or not this Post was text (True), or a URL (False). }
            @item{@racket[id] --- A unique ID for this Post. A combination of letters, numbers, and dashes. }
            @item{@racket[ups] --- The number of upvotes associated with this Post. }
            @item{@racket[is-nsfw] --- Whether or not this Post is Not Safe for Work (NSFW). }
            
        ]}


@section{Functions}

@defproc[(disconnect-reddit-service ) void]{
        Establishes that data will be retrieved locally.
        @itemlist[
            @item{@racket[filename] --- A cache file to use. Defaults to @racket{"cache.json"}.
		]}

@defproc[(disconnect-reddit-service ) void]{
        Establishes that data will be accessed online.
        @itemlist[]}


@defproc[(get-posts  [sort-mode string?] [subreddit string?]) 
    (listof post?)
    ]{
    Retrieves all the top posts
    @itemlist[
    @item{@racket[sort mode] --- The order that the Posts will be sorted by. Options are: "top" (ranked by upvotes minus downvotes), "best" (similar to top, except that it uses a more complicated algorithm to have good posts jump to the top and stay there, and bad comments to work their way down, see http://blog.reddit.com/2009/10/reddits-new-comment-sorting-system.html), "hot" (similar to "top", but weighted by time so that recent, popular posts are put near the top), "new" (posts will be sorted by creation time).}]}
    @item{@racket[subreddit] --- The subreddit that Posts will be returned from (without the "r/" preceeding it). Use "all" to return results from all subreddits.}]}
    ]}

@defproc[(get-comments  [sort-mode string?] [id string?]) 
    (listof comment?)
    ]{
    Retrieves comments for a post
    @itemlist[
    @item{@racket[sort mode] --- The order that the Posts will be sorted by. Options are: "top" (ranked by upvotes minus downvotes), "best" (similar to top, except that it uses a more complicated algorithm to have good posts jump to the top and stay there, and bad comments to work their way down, see http://blog.reddit.com/2009/10/reddits-new-comment-sorting-system.html), "hot" (similar to "top", but weighted by time so that recent, popular posts are put near the top), "new" (posts will be sorted by creation time).}]}
    @item{@racket[id] --- The unique id of a Post from which Comments will be returned.}]}
    ]}
