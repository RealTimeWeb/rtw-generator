#lang scribble/manual
 
@title{ simple-business }
@author{+email "Cory Bart" "acbart@vt.edu"}

@section{Structs}
 
Get information about businesses in America.


@defproc[(make-business
    [rating float?]
    [description string?]
    [phone string?]
    [location string?]
    [id string?]
    [name string?]
    business]{
        Information about a specific earthquake.
        @itemlist[
            @item{@racket[rating] --- Rating for this business (value ranges from 1, 1.5, ... 4.5, 5) }
            @item{@racket[description] --- Snippet text associated with this business }
            @item{@racket[phone] --- Phone number for this business formatted for display }
            @item{@racket[location] --- Address for this business formatted for display. Includes all address fields, cross streets and city, state_code, etc. }
            @item{@racket[id] --- A uniquely identifying id for this business. }
            @item{@racket[name] --- Name of this business. }
            
        ]}


@section{Functions}

@defproc[(disconnect-simple-business ) void]{
        Establishes that data will be retrieved locally.
        @itemlist[
            @item{@racket[filename] --- A cache file to use. Defaults to @racket{"cache.json"}.
		]}

@defproc[(disconnect-simple-business ) void]{
        Establishes that data will be accessed online.
        @itemlist[]}


@defproc[(search  [term string?] [location string?]) 
    (listof business?)
    ]{
    Retrieves information about the businesses that include the given term for the given area
    @itemlist[
    @item{@racket[term] --- Search term (e.g. "food", "restaurants").}]}
    @item{@racket[location] --- Specifies the combination of "address, neighborhood, city, state or zip, optional country" to be used when searching for businesses.}]}
    ]}
