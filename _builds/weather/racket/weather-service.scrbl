#lang scribble/manual
 
@title{ weather-service }
@author{+email "Austin Cory Bart" "acbart@vt.edu"}

@section{Structs}
 
Get a report of present weather and forecast data.


@defproc[(make-report
    [weather weather?]
    [location location?]
    [forecasts (listof forecast?]
    report]{
        A container for the weather, forecasts, and location information.
        @itemlist[
            @item{@racket[weather] --- The current weather for this location. }
            @item{@racket[location] --- More detailed information on this location. }
            @item{@racket[forecasts] --- The forecast for the next 7 days and 7 nights. }
            
        ]}

@defproc[(make-weather
    [wind-speed integer?]
    [windchill integer?]
    [dewpoint integer?]
    [image-url string?]
    [wind-direction integer?]
    [visibility float?]
    [humidity integer?]
    [pressure float?]
    [temp integer?]
    [description string?]
    weather]{
        A structured representation the current weather.
        @itemlist[
            @item{@racket[wind-speed] --- The current wind speed (in miles-per-hour). }
            @item{@racket[windchill] --- The perceived temperature (in Fahrenheit). }
            @item{@racket[dewpoint] --- The current dewpoint temperature (in Fahrenheit). }
            @item{@racket[image-url] --- A url pointing to a picture that describes the weather. }
            @item{@racket[wind-direction] --- The current wind direction (in degrees). }
            @item{@racket[visibility] --- How far you can see (in miles). }
            @item{@racket[humidity] --- The current relative humidity (as a percentage). }
            @item{@racket[pressure] --- The barometric pressure (in inches). }
            @item{@racket[temp] --- The current temperature (in Fahrenheit). }
            @item{@racket[description] --- A human-readable description of the current weather. }
            
        ]}

@defproc[(make-location
    [latitude float?]
    [elavation integer?]
    [name string?]
    [longitude float?]
    location]{
        A detailed description of a location
        @itemlist[
            @item{@racket[latitude] --- The latitude (up-down) of this location. }
            @item{@racket[elavation] --- The height above sea-level (in feet). }
            @item{@racket[name] --- The city and state that this location is in. }
            @item{@racket[longitude] --- The longitude (left-right) of this location. }
            
        ]}

@defproc[(make-forecast
    [long-description string?]
    [description string?]
    [image-url string?]
    [temperature-label string?]
    [period-name string?]
    [probability-of-precipitation integer?]
    [period-time string?]
    [temperature integer?]
    forecast]{
        A prediction for future weather.
        @itemlist[
            @item{@racket[long-description] --- A more-detailed, human-readable description of the predicted weather for this period. }
            @item{@racket[description] --- A human-readable description of the predicted weather for this period. }
            @item{@racket[image-url] --- A url pointing to a picture that describes the predicted weather for this period. }
            @item{@racket[temperature-label] --- Either 'High' or 'Low', depending on whether or not the predicted temperature is a daily high or a daily low. }
            @item{@racket[period-name] --- A human-readable name for this time period (e.g. Tonight or Saturday). }
            @item{@racket[probability-of-precipitation] --- The probability of precipitation for this period (as a percentage). }
            @item{@racket[period-time] --- A string representing the time that this period starts. Encoded as YYYY-MM-DDTHH:MM:SS, where the T is not a number, but a always present character (e.g. 2013-07-30T18:00:00). }
            @item{@racket[temperature] --- The predicted temperature for this period (in Fahrenheit). }
            
        ]}


@section{Functions}

@defproc[(disconnect-weather-service ) void]{
        Establishes that data will be retrieved locally.
        @itemlist[
            @item{@racket[filename] --- A cache file to use. Defaults to @racket{"cache.json"}.
		]}

@defproc[(disconnect-weather-service ) void]{
        Establishes that data will be accessed online.
        @itemlist[]}


@defproc[(get-report  [latitude float?] [longitude float?]) 
    report?
    ]{
    Gets a report on the current weather, forecast, and more detailed information about the location.
    @itemlist[
    @item{@racket[latitude] --- The latitude (up-down) of the location to get information about.}]}
    @item{@racket[longitude] --- The longitude (left-right) of the location to get information about.}]}
    ]}
