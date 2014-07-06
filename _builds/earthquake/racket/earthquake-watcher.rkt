#lang racket

; Load the internal libraries
(require htdp/error)
(require json)
(require racket/port)
(require net/url)
(require "sticky-web.rkt")

; Provide the external structs
(provide
    (struct-out report)
    (struct-out coordinate)
    (struct-out earthquake)
    (struct-out bounding-box)
    get-earthquakes
    connect-earthquake-watcher
    disconnect-earthquake-watcher)

; Define the structs

(define-struct report
    ( area earthquakes title))

(define-struct coordinate
    ( longitude latitude depth))

(define-struct earthquake
    ( maximum-estimated-intensity distance alert-level felt-reports location-description url time root-mean-square event-source gap magnitude location significance maximum-reported-intensity id))

(define-struct bounding-box
    ( minimum-longitude minimum-latitude minimum-depth maximum-longitude maximum-latitude maximum-depth))



(define (json->report jdata)
    (make-report
        (json->bounding-box (hash-ref jdata 'bbox))
        (map json->earthquake (hash-ref jdata 'features))
        (json->string (hash-ref (hash-ref jdata 'metadata) 'title))
        )

(define (json->coordinate jdata)
    (make-coordinate
        (list-ref jdata 0)
        (list-ref jdata 1)
        (list-ref jdata 2)
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
        (list-ref jdata 3)
        (list-ref jdata 4)
        (list-ref jdata 5)
        )


(define connect-earthquake-watcher connect)
(define disconnect-earthquake-watcher disconnect)

; Define the services, and their helpers

(define (get-earthquakes ) 
    (json->report (get-earthquakes/json )))
    
(define (get-earthquakes/json )
    (string->jsexpr (get-earthquakes/string )))
    
(define (get-earthquakes/string )
    (get->string 
        (format "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/~s_~s.geojson"  threshold time)
        (list)
        (list)
        ))

