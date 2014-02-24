#lang scribble/manual
 
@title{ earthquake-watcher }
@author{+email "Cory Bart" "acbart@vt.edu"}

@section{Structs}
 
A short description


@defproc[(make-my-authors
    [test string?]
    [books (listof string?]
    [other earthquake?]
    [years (listof integer?]
    my-authors]{
        A list of authors.
        @itemlist[
            @item{@racket[test] --- amazing }
            @item{@racket[books] --- All the authors. }
            @item{@racket[other] --- amazing }
            @item{@racket[years] --- All the years. }
            
        ]}

@defproc[(make-report
    [area bounding-box?]
    [earthquakes (listof earthquake?]
    [title string?]
    report]{
        Information about earthquakes matching certain criteria, including the area that they occurred.
        @itemlist[
            @item{@racket[area] --- A region that contains all the earthquakes. }
            @item{@racket[earthquakes] --- A list of the earthquakes. }
            @item{@racket[title] --- A human-readable title that describes this data. }
            
        ]}

@defproc[(make-coordinate
    [latitude float?]
    [depth float?]
    [longitude float?]
    coordinate]{
        The longitudinal, latitudinal, and depth where the earthquake occurred.
        @itemlist[
            @item{@racket[latitude] --- The latitude (South-North) component. }
            @item{@racket[depth] --- The depth (closer or farther from the surface) component. }
            @item{@racket[longitude] --- The longitude (West-North) component. }
            
        ]}

@defproc[(make-earthquake
    [maximum-estimated-intensity float?]
    [distance float?]
    [alert-level string?]
    [felt-reports integer?]
    [location-description string?]
    [url string?]
    [time long?]
    [root-mean-square float?]
    [event-source string?]
    [gap float?]
    [magnitude float?]
    [location coordinate?]
    [significance integer?]
    [maximum-reported-intensity float?]
    [id string?]
    earthquake]{
        Information about a specific earthquake.
        @itemlist[
            @item{@racket[maximum-estimated-intensity] --- The maximum estimated instrumental intensity for the event, or null if the data is not available. While typically reported as a roman numeral, intensity is reported here as the decimal equivalent. More information can be found at http://earthquake.usgs.gov/learn/topics/mag_vs_int.php }
            @item{@racket[distance] --- Horizontal distance from the epicenter to the nearest station (in degrees), or null if the data is not available. 1 degree is approximately 111.2 kilometers. In general, the smaller this number, the more reliable is the calculated depth of the earthquake. }
            @item{@racket[alert-level] --- A color string (one of "green", "yellow", "orange", "red") indicating how dangerous the quake was, or null if the data is not available. More information about this kind of alert is available at http://earthquake.usgs.gov/research/pager/ }
            @item{@racket[felt-reports] --- The total number of "Felt" reports submitted, or null if the data is not available. }
            @item{@racket[location-description] --- A human-readable description of the location. }
            @item{@racket[url] --- A webpage with more information about the earthquake. }
            @item{@racket[time] --- The epoch time (http://en.wikipedia.org/wiki/Unix_time) when this earthquake occurred. }
            @item{@racket[root-mean-square] --- The root-mean-square (RMS) travel time residual, in sec, using all weights. This parameter provides a measure of the fit of the observed arrival times to the predicted arrival times for this location. Smaller numbers reflect a better fit of the data. The value is dependent on the accuracy of the velocity model used to compute the earthquake location, the quality weights assigned to the arrival time data, and the procedure used to locate the earthquake. }
            @item{@racket[event-source] --- Either "AUTOMATIC", "PUBLISHED", or "REVIEWED". Indicates how the earthquake was identified and whether it was reviewed by a human. }
            @item{@racket[gap] --- The largest azimuthal gap between azimuthally adjacent stations (in degrees), or null if the data is not available. In general, the smaller this number, the more reliable is the calculated horizontal position of the earthquake. }
            @item{@racket[magnitude] --- The magnitude of the earthquake on the Richter Scale. }
            @item{@racket[location] --- The location of the earthquake. }
            @item{@racket[significance] --- A number describing how significant the event is. Larger numbers indicate a more significant event. This value is determined on a number of factors, including: magnitude, maximum estimated intensity, felt reports, and estimated impact. }
            @item{@racket[maximum-reported-intensity] --- The maximum reported intensity for this earthquake, or null if the data is not available. While typically reported as a roman numeral, intensity is reported here as a decimal number. More information can be found at http://earthquake.usgs.gov/learn/topics/mag_vs_int.php }
            @item{@racket[id] --- A uniquely identifying id for this earthquake. }
            
        ]}

@defproc[(make-bounding-box
    [maximum-longitude float?]
    [minimum-latitude float?]
    [minimum-depth float?]
    [minimum-longitude float?]
    [maximum-depth float?]
    [maximum-latitude float?]
    bounding-box]{
        The longitudinal, latitudinal, and depth of the region required to display all the earthquakes.
        @itemlist[
            @item{@racket[maximum-longitude] --- The higher longitude (East) component. }
            @item{@racket[minimum-latitude] --- The lower latitude (South) component. }
            @item{@racket[minimum-depth] --- The lower depth (closer or farther from the surface) component. }
            @item{@racket[minimum-longitude] --- The lower longitude (West) component. }
            @item{@racket[maximum-depth] --- The higher depth (closer or farther from the surface) component. }
            @item{@racket[maximum-latitude] --- The higher latitude (North) component. }
            
        ]}


@section{Functions}

@defproc[(disconnect-earthquake-watcher ) void]{
        Establishes that data will be retrieved locally.
        @itemlist[
            @item{@racket[filename] --- A cache file to use. Defaults to @racket{"cache.json"}.
		]}

@defproc[(disconnect-earthquake-watcher ) void]{
        Establishes that data will be accessed online.
        @itemlist[]}


@defproc[(get-some-books ) 
    my-authors?
    ]{
    Connects without any parameters
    @itemlist[
    ]}

@defproc[(get-earthquakes  [threshold integer?] [time string?]) 
    report?
    ]{
    Retrieves information about earthquakes around the world.
    @itemlist[
    @item{@racket[threshold] --- A string indicating what kind of earthquakes to report. Must be either "significant" (only significant earthquakes), "all" (all earthquakes, regardless of significance), "4.5", "2.5", or "1.0". Note that for the last three, all earthquakes at and above that level will be reported.}]}
    @item{@racket[time] --- A string indicating the time range of earthquakes to report. Must be either "hour" (only earthquakes in the past hour), "day" (only earthquakes that happened today), "week" (only earthquakes that happened in the past 7 days), or "month" (only earthquakes that happened in the past 30 days).}]}
    ]}

@defproc[(get-first-year ) 
    integer?
    ]{
    Gets the first books
    @itemlist[
    ]}
