#lang scribble/manual
 
@title{ stock-service }
@author{+email "Cory Bart" "acbart@vt.edu"}

@section{Structs}
 
Get the latest information about stocks.


@defproc[(make-stock
    [last-trade-date string?]
    [last-trade-time string?]
    [exchange string?]
    [percent-price-change float?]
    [last-sale-price float?]
    [id integer?]
    [ticker string?]
    [price-change float?]
    stock]{
        A structured representation of stock information, including ticker symbol, latest sale price, and price change since yesterday.
        @itemlist[
            @item{@racket[last-trade-date] --- The entire date of the last trade. }
            @item{@racket[last-trade-time] --- The time of the last trade. }
            @item{@racket[exchange] --- The name of the exchange (e.g. NASDAQ) }
            @item{@racket[percent-price-change] --- The percent price change since yesterday. }
            @item{@racket[last-sale-price] --- The latest sale price for this stock. }
            @item{@racket[id] --- The unique ID number for this ticker symbol }
            @item{@racket[ticker] --- The Ticker Symbol (e.g. AAPL) }
            @item{@racket[price-change] --- The price change since yesterday. }
            
        ]}


@section{Functions}

@defproc[(disconnect-stock-service ) void]{
        Establishes that data will be retrieved locally.
        @itemlist[
            @item{@racket[filename] --- A cache file to use. Defaults to @racket{"cache.json"}.
		]}

@defproc[(disconnect-stock-service ) void]{
        Establishes that data will be accessed online.
        @itemlist[]}


@defproc[(get-stock-information  [ticker string?]) 
    (listof stock?)
    ]{
    Retrieves current stock information.
    @itemlist[
    @item{@racket[ticker] --- A comma separated list of ticker symbols (e.g. "AAPL, MSFT, CSCO").}]}
    ]}
