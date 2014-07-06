#lang racket

; Load the internal libraries
(require htdp/error)
(require json)
(require racket/port)
(require net/url)
(require "sticky-web.rkt")

; Provide the external structs
(provide
    (struct-out business)
    search
    connect-simple-business
    disconnect-simple-business)

; Define the structs

(define-struct business
    ( rating description phone location id name))



(define (json->business jdata)
    (make-business
        (hash-ref jdata 'rating)
        (json->string (hash-ref jdata 'snippet_text))
        (json->string (hash-ref jdata 'display_phone))
        (json->string (hash-ref (hash-ref jdata 'location) 'display_address))
        (json->string (hash-ref jdata 'id))
        (json->string (hash-ref jdata 'name))
        )


(define connect-simple-business connect)
(define disconnect-simple-business disconnect)

; Define the services, and their helpers

(define (search ) 
    (json->business[] (search/json )))
    
(define (search/json )
    (string->jsexpr (search/string )))
    
(define (search/string )
    (get->string 
        (format "http://api.yelp.com/v2/search" )
        (list (cons 'term term) (cons 'location location))
        (list (cons 'term term) (cons 'location location))
        ))

