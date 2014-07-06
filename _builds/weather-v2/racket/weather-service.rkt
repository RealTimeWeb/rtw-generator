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
    (struct-out weather)
    (struct-out location)
    (struct-out forecast)
    get-report
    connect-weather-service
    disconnect-weather-service)

; Define the structs

(define-struct report
    ( weather location forecasts))

(define-struct weather
    ( wind-speed windchill dewpoint image-url wind-direction visibility humidity pressure temp description))

(define-struct location
    ( latitude elavation name longitude))

(define-struct forecast
    ( long-description description image-url temperature-label period-name probability-of-precipitation period-time temperature))



(define (json->report jdata)
    (make-report
        (json->weather (hash-ref jdata 'currentobservation))
        (json->location (hash-ref jdata 'location))
        (map json->forecast jdata)
        )

(define (json->weather jdata)
    (make-weather
        (hash-ref jdata 'Winds)
        (hash-ref jdata 'WindChill)
        (hash-ref jdata 'Dewp)
        (json->string (hash-ref jdata 'Weatherimage))
        (hash-ref jdata 'Windd)
        (hash-ref jdata 'Visibility)
        (hash-ref jdata 'Relh)
        (hash-ref jdata 'SLP)
        (hash-ref jdata 'Temp)
        (json->string (hash-ref jdata 'Weather))
        )

(define (json->location jdata)
    (make-location
        (hash-ref jdata 'latitude)
        (hash-ref jdata 'elevation)
        (json->string (hash-ref jdata 'areaDescription))
        (hash-ref jdata 'longitude)
        )

(define (json->forecast jdata)
    (make-forecast
        (json->string (hash-ref (hash-ref jdata 'data) 'text))
        (json->string (hash-ref (hash-ref jdata 'data) 'weather))
        (json->string (hash-ref (hash-ref jdata 'data) 'iconLink))
        (json->string (hash-ref (hash-ref jdata 'time) 'tempLabel))
        (json->string (hash-ref (hash-ref jdata 'time) 'startPeriodName))
        (hash-ref (hash-ref jdata 'data) 'pop)
        (json->string (hash-ref (hash-ref jdata 'time) 'startValidTime))
        (hash-ref (hash-ref jdata 'data) 'temperature)
        )


(define connect-weather-service connect)
(define disconnect-weather-service disconnect)

; Define the services, and their helpers

(define (get-report ) 
    (json->report (get-report/json )))
    
(define (get-report/json )
    (string->jsexpr (get-report/string )))
    
(define (get-report/string )
    (get->string 
        (format "http://forecast.weather.gov/MapClick.php" )
        (list (cons 'latitude latitude) (cons 'fcsttype fcsttype) (cons 'longitude longitude))
        (list (cons 'latitude latitude) (cons 'fcsttype fcsttype) (cons 'longitude longitude))
        ))

