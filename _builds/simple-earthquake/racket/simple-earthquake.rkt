#lang racket

; Load the internal libraries
(require htdp/error)
(require json)
(require racket/port)
(require net/url)
(require "sticky-web.rkt")

; Provide the external structs
(provide
    (struct-out coordinate)
    (struct-out earthquake)
    get-earthquakes
    connect-simple-earthquake
    disconnect-simple-earthquake)

; Define the structs

(define-struct coordinate
    ( longitude latitude depth))

(define-struct earthquake
    ( location magnitude location-description id time))



(define (json->coordinate jdata)
    (make-coordinate
        (list-ref jdata 0)
        (list-ref jdata 1)
        (list-ref jdata 2)
        )

(define (json->earthquake jdata)
    (make-earthquake
        (json->coordinate (hash-ref (hash-ref jdata 'geometry) 'coordinates))
        (hash-ref (hash-ref jdata 'properties) 'mag)
        (json->string (hash-ref (hash-ref jdata 'properties) 'place))
        (json->string (hash-ref jdata 'id))
        (hash-ref (hash-ref jdata 'properties) 'time)
        )


(define connect-simple-earthquake connect)
(define disconnect-simple-earthquake disconnect)

; Define the services, and their helpers

(define (get-earthquakes ) 
    (json->earthquake[] (get-earthquakes/json )))
    
(define (get-earthquakes/json )
    (string->jsexpr (get-earthquakes/string )))
    
(define (get-earthquakes/string )
    (get->string 
        (format "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/~s_~s.geojson"  threshold time)
        (list)
        (list)
        ))

