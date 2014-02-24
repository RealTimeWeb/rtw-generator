#lang racket

; Load the internal libraries
(require htdp/error)
(require json)
(require racket/port)
(require net/url)
(require "sticky-web.rkt")

; Provide the external structs
(provide
    (struct-out my-authors)
    (struct-out report)
    (struct-out coordinate)
    (struct-out earthquake)
    (struct-out bounding-box)
    get-some-books
    get-earthquakes
    get-first-year
    connect-earthquake-watcher
    disconnect-earthquake-watcher)

; Define the structs

(define-struct my-authors
    ( test books other years))

(define-struct report
    ( area earthquakes title))

(define-struct coordinate
    ( latitude depth longitude))

(define-struct earthquake
    ( maximum-estimated-intensity distance alert-level felt-reports location-description url time root-mean-square event-source gap magnitude location significance maximum-reported-intensity id))

(define-struct bounding-box
    ( maximum-longitude minimum-latitude minimum-depth minimum-longitude maximum-depth maximum-latitude))



(define (json->my-authors jdata)
    (make-my-authors
        /bookstore/
        /bookstore/book/author
        /bookstore/
        /bookstore/book/year
        )

(define (json->report jdata)
    (make-report
        (json->bounding-box (hash-ref jdata 'bbox))
        (map json->earthquake (hash-ref jdata 'features))
        (json->string (hash-ref (hash-ref jdata 'metadata) 'title))
        )

(define (json->coordinate jdata)
    (make-coordinate
        (list-ref jdata 1)
        (list-ref jdata 2)
        (list-ref jdata 0)
        )

(define (json->earthquake jdata)
    (make-earthquake
        (hash-ref (hash-ref jdata 'properties) 'mmi)
        (hash-ref (hash-ref jdata 'properties) 'dmin)
        (json->string (hash-ref (hash-ref jdata 'properties) 'alert))
        (hash-ref (hash-ref jdata 'properties) 'felt)
        (json->string (hash-ref (hash-ref jdata 'properties) 'place))
        (json->string (hash-ref (hash-ref jdata 'properties) 'url))
        (hash-ref (hash-ref jdata 'properties) 'time)
        (hash-ref (hash-ref jdata 'properties) 'rms)
        (json->string (hash-ref (hash-ref jdata 'properties) 'status))
        (hash-ref (hash-ref jdata 'properties) 'gap)
        (hash-ref (hash-ref jdata 'properties) 'mag)
        (json->coordinate (hash-ref (hash-ref jdata 'geometry) 'coordinates))
        (hash-ref (hash-ref jdata 'properties) 'sig)
        (hash-ref (hash-ref jdata 'properties) 'cdi)
        (json->string (hash-ref jdata 'id))
        )

(define (json->bounding-box jdata)
    (make-bounding-box
        (list-ref jdata 0)
        (list-ref jdata 1)
        (list-ref jdata 2)
        (list-ref jdata 0)
        (list-ref jdata 2)
        (list-ref jdata 1)
        )


(define connect-earthquake-watcher connect)
(define disconnect-earthquake-watcher disconnect)

; Define the services, and their helpers

(define (get-some-books ) 
    (json->my-authors (get-some-books/json )))
    
(define (get-some-books/json )
    (string->jsexpr (get-some-books/string )))
    
(define (get-some-books/string )
    (post->string 
        (format "http://www.w3schools.com/dom/books.xml" )
        (list)
        (list)
        ))


(define (get-earthquakes ) 
    (json->report (get-earthquakes/json )))
    
(define (get-earthquakes/json )
    (string->jsexpr (get-earthquakes/string )))
    
(define (get-earthquakes/string )
    (get->string 
        (format "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/~s_~s.geojson"  time (number->string threshold))
        (list (cons 'secret secret))
        (list (cons 'threshold threshold) (cons 'secret secret) (cons 'time time))
        ))


(define (get-first-year ) 
    (json->integer (get-first-year/json )))
    
(define (get-first-year/json )
    (string->jsexpr (get-first-year/string )))
    
(define (get-first-year/string )
    (get->string 
        (format "http://www.w3schools.com/dom/books.xml" )
        (list)
        (list)
        ))

