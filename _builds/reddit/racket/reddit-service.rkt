#lang racket

; Load the internal libraries
(require htdp/error)
(require json)
(require racket/port)
(require net/url)
(require "sticky-web.rkt")

; Provide the external structs
(provide
    (struct-out comment)
    (struct-out post)
    get-posts
    get-comments
    connect-reddit-service
    disconnect-reddit-service)

; Define the structs

(define-struct comment
    ( body created downs author subreddit body-html replies id ups))

(define-struct post
    ( permalink author title downs created subreddit content is-self id ups is-nsfw))



(define (json->comment jdata)
    (make-comment
        (json->string (hash-ref (hash-ref jdata 'data) 'body))
        (hash-ref (hash-ref jdata 'data) 'created)
        (hash-ref (hash-ref jdata 'data) 'downs)
        (json->string (hash-ref (hash-ref jdata 'data) 'author))
        (json->string (hash-ref (hash-ref jdata 'data) 'subreddit))
        (json->string (hash-ref (hash-ref jdata 'data) 'body_html))
        (map json->comment (hash-ref (hash-ref (hash-ref (hash-ref jdata 'data) 'replies) 'data) 'children))
        (json->string (hash-ref (hash-ref jdata 'data) 'id))
        (hash-ref (hash-ref jdata 'data) 'ups)
        )

(define (json->post jdata)
    (make-post
        (json->string (hash-ref (hash-ref jdata 'data) 'permalink))
        (json->string (hash-ref (hash-ref jdata 'data) 'author))
        (json->string (hash-ref (hash-ref jdata 'data) 'title))
        (hash-ref (hash-ref jdata 'data) 'downs)
        (hash-ref (hash-ref jdata 'data) 'created)
        (json->string (hash-ref (hash-ref jdata 'data) 'subreddit))
        (json->string (hash-ref (hash-ref jdata 'data) 'selftext))
        (hash-ref (hash-ref jdata 'data) 'is_self)
        (json->string (hash-ref (hash-ref jdata 'data) 'id))
        (hash-ref (hash-ref jdata 'data) 'ups)
        (hash-ref (hash-ref jdata 'data) 'over_18)
        )


(define connect-reddit-service connect)
(define disconnect-reddit-service disconnect)

; Define the services, and their helpers

(define (get-posts ) 
    (json->post[] (get-posts/json )))
    
(define (get-posts/json )
    (string->jsexpr (get-posts/string )))
    
(define (get-posts/string )
    (get->string 
        (format "http://www.reddit.com/r/~s/~s.json"  subreddit sort-mode)
        (list)
        (list)
        ))


(define (get-comments ) 
    (json->comment[] (get-comments/json )))
    
(define (get-comments/json )
    (string->jsexpr (get-comments/string )))
    
(define (get-comments/string )
    (get->string 
        (format "http://www.reddit.com/r/comments/~s/~s.json"  id sort-mode)
        (list)
        (list)
        ))

