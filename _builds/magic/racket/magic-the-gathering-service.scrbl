#lang scribble/manual
 
@title{ magic-the-gathering-service }
@author{+email "Cory Bart" "acbart@vt.edu"}

@section{Structs}
 
Access information about Magic the Gathering Cards.


@defproc[(make-print
    [set string?]
    [id integer?]
    print]{
        The print expansion this belongs to.
        @itemlist[
            @item{@racket[set] --- The ID code of this set. }
            @item{@racket[id] --- The unique id number of this set. }
            
        ]}

@defproc[(make-card-result
    [id integer?]
    [name string?]
    card-result]{
        The result of a card search, only having the ID and card name. You can look up the card by its ID for more complete information.
        @itemlist[
            @item{@racket[id] --- The unique id number of this card }
            @item{@racket[name] --- The name of this card. }
            
        ]}

@defproc[(make-card
    [flavors (listof string?]
    [rating string?]
    [votes string?]
    [set string?]
    [all-sets (listof print?]
    [name string?]
    [power string?]
    [watermark string?]
    [artist string?]
    [number string?]
    [rarity string?]
    [texts (listof string?]
    [converted-mana-cost string?]
    [mana-cost (listof string?]
    [id string?]
    [types (listof string?]
    [toughness string?]
    card]{
        A Magic the Gathering Card
        @itemlist[
            @item{@racket[flavors] --- Any flavor texts on this card. }
            @item{@racket[rating] --- The card's voted upon rating. }
            @item{@racket[votes] --- The number of times this card has been voted on. }
            @item{@racket[set] --- The expansion set that this card belongs to. }
            @item{@racket[all-sets] --- All the expansion sets that this belongs to. }
            @item{@racket[name] --- The name of this card. }
            @item{@racket[power] --- The power (http://mtg.wikia.com/wiki/Power) of this card }
            @item{@racket[watermark] --- The watermark of this card }
            @item{@racket[artist] --- The name of the artist for the card's artwork. }
            @item{@racket[number] --- The Card Number. }
            @item{@racket[rarity] --- How rare this card is, typically either "uncommon", "common", or "rare". }
            @item{@racket[texts] --- Any text blocks on the card. }
            @item{@racket[converted-mana-cost] --- The converted mana cost. }
            @item{@racket[mana-cost] --- The Mana cost of this card. }
            @item{@racket[id] --- A unique id that identifies this card. }
            @item{@racket[types] --- Card's types, usually at least one of "artifact", "creature", "enchantment", "instant", "land", "planeswalker", "sorcery", or "tribal". Cards can also have a supertype and/or subtype.  }
            @item{@racket[toughness] --- The toughness (http://mtg.wikia.com/wiki/Toughness) of this card }
            
        ]}


@section{Functions}

@defproc[(disconnect-magic-the-gathering-service ) void]{
        Establishes that data will be retrieved locally.
        @itemlist[
            @item{@racket[filename] --- A cache file to use. Defaults to @racket{"cache.json"}.
		]}

@defproc[(disconnect-magic-the-gathering-service ) void]{
        Establishes that data will be accessed online.
        @itemlist[]}


@defproc[(search-cards  [keyword string?]) 
    (listof card-result?)
    ]{
    Searches the database for cards with the keyword in the card's name.
    @itemlist[
    @item{@racket[keyword] --- The keyword to match against card's names}]}
    ]}

@defproc[(get-card  [id integer?]) 
    card?
    ]{
    Retrieves a card by looking up its ID.
    @itemlist[
    @item{@racket[id] --- The unique id number of the card.}]}
    ]}
