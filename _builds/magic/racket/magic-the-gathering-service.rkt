#lang racket

; Load the internal libraries
(require htdp/error)
(require json)
(require racket/port)
(require net/url)
(require "sticky-web.rkt")

; Provide the external structs
(provide
    (struct-out print)
    (struct-out card-result)
    (struct-out card)
    search-cards
    get-card
    connect-magic-the-gathering-service
    disconnect-magic-the-gathering-service)

; Define the structs

(define-struct print
    ( set id))

(define-struct card-result
    ( id name))

(define-struct card
    ( flavors rating votes set all-sets name power watermark artist number rarity texts converted-mana-cost mana-cost id types toughness))



(define (json->print jdata)
    (make-print
        (json->string (hash-ref jdata 'set))
        (hash-ref jdata 'id)
        )

(define (json->card-result jdata)
    (make-card-result
        (hash-ref jdata 'id)
        (json->string (hash-ref jdata 'name))
        )

(define (json->card jdata)
    (make-card
        (map json->string (hash-ref jdata 'flavor))
        (json->string (hash-ref jdata 'rating))
        (json->string (hash-ref jdata 'votes))
        (json->string (hash-ref jdata 'set))
        (map json->print (hash-ref jdata 'prints))
        (json->string (hash-ref jdata 'name))
        (json->string (hash-ref jdata 'power))
        (json->string (hash-ref jdata 'watermark))
        (json->string (hash-ref jdata 'artist))
        (json->string (hash-ref jdata 'number))
        (json->string (hash-ref jdata 'rarity))
        (map json->string (hash-ref jdata 'text))
        (json->string (hash-ref jdata 'cmc))
        (map json->string (hash-ref jdata 'mana))
        (json->string (hash-ref jdata 'id))
        (map json->string (hash-ref jdata 'type))
        (json->string (hash-ref jdata 'power))
        )


(define connect-magic-the-gathering-service connect)
(define disconnect-magic-the-gathering-service disconnect)

; Define the services, and their helpers

(define (search-cards ) 
    (json->card-result[] (search-cards/json )))
    
(define (search-cards/json )
    (string->jsexpr (search-cards/string )))
    
(define (search-cards/string )
    (get->string 
        (format "http://api.mtgapi.com/v1/card/name/~s"  keyword)
        (list)
        (list)
        ))


(define (get-card ) 
    (json->card (get-card/json )))
    
(define (get-card/json )
    (string->jsexpr (get-card/string )))
    
(define (get-card/string )
    (get->string 
        (format "http://api.mtgapi.com/v1/card/id/~s"  (number->string id))
        (list)
        (list)
        ))

