#lang scribble/manual
 
@title{ simple-earthquake }
@author{+email "Cory Bart" "acbart@vt.edu"}

@section{Structs}
 
Get the latest information about earthquakes around the world.


@defproc[(make-coordinate
    [longitude float?]
    [latitude float?]
    [depth float?]
    coordinate]{
        The longitudinal, latitudinal, and depth where the earthquake occurred.
        @itemlist[
            @item{@racket[longitude] --- The longitude (West-North) component. }
            @item{@racket[latitude] --- The latitude (South-North) component. }
            @item{@racket[depth] --- The depth (closer or farther from the surface) component. }
            
        ]}

@defproc[(make-earthquake
    [location coordinate?]
    [magnitude float?]
    [location-description string?]
    [id string?]
    [time long?]
    earthquake]{
        Information about a specific earthquake.
        @itemlist[
            @item{@racket[location] --- The location of the earthquake. }
            @item{@racket[magnitude] --- The magnitude of the earthquake on the Richter Scale. }
            @item{@racket[location-description] --- A human-readable description of the location. }
            @item{@racket[id] --- A uniquely identifying id for this earthquake. }
            @item{@racket[time] --- The epoch time (http://en.wikipedia.org/wiki/Unix_time) when this earthquake occurred. }
            
        ]}


@section{Functions}

@defproc[(disconnect-simple-earthquake ) void]{
        Establishes that data will be retrieved locally.
        @itemlist[
            @item{@racket[filename] --- A cache file to use. Defaults to @racket{"cache.json"}.
		]}

@defproc[(disconnect-simple-earthquake ) void]{
        Establishes that data will be accessed online.
        @itemlist[]}


@defproc[(get-earthquakes  [threshold string?] [time string?]) 
    (listof earthquake?)
    ]{
    Retrieves information about earthquakes around the world.
    @itemlist[
    @item{@racket[threshold] --- A string indicating what kind of earthquakes to report. Must be either "significant" (only significant earthquakes), "all" (all earthquakes, regardless of significance), "4.5", "2.5", or "1.0". Note that for the last three, all earthquakes at and above that level will be reported.}]}
    @item{@racket[time] --- A string indicating the time range of earthquakes to report. Must be either "hour" (only earthquakes in the past hour), "day" (only earthquakes that happened today), "week" (only earthquakes that happened in the past 7 days), or "month" (only earthquakes that happened in the past 30 days).}]}
    ]}
