#lang racket

; Load the internal libraries
(require htdp/error)
(require json)
(require racket/port)
(require net/url)
(require "sticky-web.rkt")

; Provide the external structs
(provide
    (struct-out stock)
    get-stock-information
    connect-stock-service
    disconnect-stock-service)

; Define the structs

(define-struct stock
    ( last-trade-date last-trade-time exchange percent-price-change last-sale-price id ticker price-change))



(define (json->stock jdata)
    (make-stock
        (json->string (hash-ref jdata 'lt))
        (json->string (hash-ref jdata 'ltt))
        (json->string (hash-ref jdata 'e))
        (hash-ref jdata 'cp)
        (hash-ref jdata 'l)
        (hash-ref jdata 'id)
        (json->string (hash-ref jdata 't))
        (hash-ref jdata 'c)
        )


(define connect-stock-service connect)
(define disconnect-stock-service disconnect)

; Define the services, and their helpers

(define (get-stock-information ) 
    (json->stock[] (get-stock-information/json )))
    
(define (get-stock-information/json )
    (string->jsexpr (get-stock-information/string )))
    
(define (get-stock-information/string )
    (get->string 
        (format "http://www.google.com/finance/info" )
        (list (cons 'client client) (cons 'ticker ticker))
        (list (cons 'client client) (cons 'ticker ticker))
        ))

