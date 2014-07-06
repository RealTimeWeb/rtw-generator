package realtimeweb.magicthegatheringservice.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;



import realtimeweb.magicthegatheringservice.domain.Print;

/**
 * A Magic the Gathering Card
 */
public class Card {
	
    // Actually returns a list of list of strings!
    private ArrayList<String> flavors;
    private String rating;
    private String votes;
    private String set;
    private ArrayList<Print> allSets;
    private String name;
    private String power;
    private String watermark;
    private String artist;
    private String number;
    private String rarity;
    private ArrayList<String> texts;
    private String convertedManaCost;
    private ArrayList<String> manaCost;
    private String id;
    private ArrayList<String> types;
    private String toughness;
    
    
    /*
     * @return Any flavor texts on this card.
     */
    public ArrayList<String> getFlavors() {
        return this.flavors;
    }
    
    /*
     * @param Any flavor texts on this card.
     * @return ArrayList<String>
     */
    public void setFlavors(ArrayList<String> flavors) {
        this.flavors = flavors;
    }
    
    /*
     * @return The card's voted upon rating.
     */
    public String getRating() {
        return this.rating;
    }
    
    /*
     * @param The card's voted upon rating.
     * @return String
     */
    public void setRating(String rating) {
        this.rating = rating;
    }
    
    /*
     * @return The number of times this card has been voted on.
     */
    public String getVotes() {
        return this.votes;
    }
    
    /*
     * @param The number of times this card has been voted on.
     * @return String
     */
    public void setVotes(String votes) {
        this.votes = votes;
    }
    
    /*
     * @return The expansion set that this card belongs to.
     */
    public String getSet() {
        return this.set;
    }
    
    /*
     * @param The expansion set that this card belongs to.
     * @return String
     */
    public void setSet(String set) {
        this.set = set;
    }
    
    /*
     * @return All the expansion sets that this belongs to.
     */
    public ArrayList<Print> getAllSets() {
        return this.allSets;
    }
    
    /*
     * @param All the expansion sets that this belongs to.
     * @return ArrayList<Print>
     */
    public void setAllSets(ArrayList<Print> allSets) {
        this.allSets = allSets;
    }
    
    /*
     * @return The name of this card.
     */
    public String getName() {
        return this.name;
    }
    
    /*
     * @param The name of this card.
     * @return String
     */
    public void setName(String name) {
        this.name = name;
    }
    
    /*
     * @return The power (http://mtg.wikia.com/wiki/Power) of this card
     */
    public String getPower() {
        return this.power;
    }
    
    /*
     * @param The power (http://mtg.wikia.com/wiki/Power) of this card
     * @return String
     */
    public void setPower(String power) {
        this.power = power;
    }
    
    /*
     * @return The watermark of this card
     */
    public String getWatermark() {
        return this.watermark;
    }
    
    /*
     * @param The watermark of this card
     * @return String
     */
    public void setWatermark(String watermark) {
        this.watermark = watermark;
    }
    
    /*
     * @return The name of the artist for the card's artwork.
     */
    public String getArtist() {
        return this.artist;
    }
    
    /*
     * @param The name of the artist for the card's artwork.
     * @return String
     */
    public void setArtist(String artist) {
        this.artist = artist;
    }
    
    /*
     * @return The Card Number.
     */
    public String getNumber() {
        return this.number;
    }
    
    /*
     * @param The Card Number.
     * @return String
     */
    public void setNumber(String number) {
        this.number = number;
    }
    
    /*
     * @return How rare this card is, typically either "uncommon", "common", or "rare".
     */
    public String getRarity() {
        return this.rarity;
    }
    
    /*
     * @param How rare this card is, typically either "uncommon", "common", or "rare".
     * @return String
     */
    public void setRarity(String rarity) {
        this.rarity = rarity;
    }
    
    /*
     * @return Any text blocks on the card.
     */
    public ArrayList<String> getTexts() {
        return this.texts;
    }
    
    /*
     * @param Any text blocks on the card.
     * @return ArrayList<String>
     */
    public void setTexts(ArrayList<String> texts) {
        this.texts = texts;
    }
    
    /*
     * @return The converted mana cost.
     */
    public String getConvertedManaCost() {
        return this.convertedManaCost;
    }
    
    /*
     * @param The converted mana cost.
     * @return String
     */
    public void setConvertedManaCost(String convertedManaCost) {
        this.convertedManaCost = convertedManaCost;
    }
    
    /*
     * @return The Mana cost of this card.
     */
    public ArrayList<String> getManaCost() {
        return this.manaCost;
    }
    
    /*
     * @param The Mana cost of this card.
     * @return ArrayList<String>
     */
    public void setManaCost(ArrayList<String> manaCost) {
        this.manaCost = manaCost;
    }
    
    /*
     * @return A unique id that identifies this card.
     */
    public String getId() {
        return this.id;
    }
    
    /*
     * @param A unique id that identifies this card.
     * @return String
     */
    public void setId(String id) {
        this.id = id;
    }
    
    /*
     * @return Card's types, usually at least one of "artifact", "creature", "enchantment", "instant", "land", "planeswalker", "sorcery", or "tribal". Cards can also have a supertype and/or subtype. 
     */
    public ArrayList<String> getTypes() {
        return this.types;
    }
    
    /*
     * @param Card's types, usually at least one of "artifact", "creature", "enchantment", "instant", "land", "planeswalker", "sorcery", or "tribal". Cards can also have a supertype and/or subtype. 
     * @return ArrayList<String>
     */
    public void setTypes(ArrayList<String> types) {
        this.types = types;
    }
    
    /*
     * @return The toughness (http://mtg.wikia.com/wiki/Toughness) of this card
     */
    public String getToughness() {
        return this.toughness;
    }
    
    /*
     * @param The toughness (http://mtg.wikia.com/wiki/Toughness) of this card
     * @return String
     */
    public void setToughness(String toughness) {
        this.toughness = toughness;
    }
    
	
	/**
	 * Creates a string based representation of this Card.
	
	 * @return String
	 */
	public String toString() {
		return "Card[" +flavors+", "+rating+", "+votes+", "+set+", "+allSets+", "+name+", "+power+", "+watermark+", "+artist+", "+number+", "+rarity+", "+texts+", "+convertedManaCost+", "+manaCost+", "+id+", "+types+", "+toughness+"]";
	}
	
	/**
	 * Internal constructor to create a Card from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    public Card(Map<String, Object> raw) {
        // TODO: Check that the data has the correct schema.
        // NOTE: It's much safer to check the Map for fields than to catch a runtime exception.
        try {
            this.flavors = new ArrayList<String>();
            System.out.println(raw);
            Iterator<Object> flavorsIter = ((List<Object>)raw.get("flavor")).iterator();
            while (flavorsIter.hasNext()) {
                this.flavors.add(new String((String)flavorsIter.next()));
            }
            this.rating = raw.get("rating").toString();
            this.votes = raw.get("votes").toString();
            this.set = raw.get("set").toString();
            this.allSets = new ArrayList<Print>();
            Iterator<Object> allSetsIter = ((List<Object>)raw.get("prints")).iterator();
            while (allSetsIter.hasNext()) {
                this.allSets.add(new Print((Map<String, Object>)allSetsIter.next()));
            }
            this.name = raw.get("name").toString();
            this.power = raw.get("power").toString();
            this.watermark = raw.get("watermark").toString();
            this.artist = raw.get("artist").toString();
            this.number = raw.get("number").toString();
            this.rarity = raw.get("rarity").toString();
            this.texts = new ArrayList<String>();
            Iterator<Object> textsIter = ((List<Object>)raw.get("text")).iterator();
            while (textsIter.hasNext()) {
                this.texts.add(new String((String)textsIter.next()));
            }
            this.convertedManaCost = raw.get("cmc").toString();
            this.manaCost = new ArrayList<String>();
            Iterator<Object> manaCostIter = ((List<Object>)raw.get("mana")).iterator();
            while (manaCostIter.hasNext()) {
                this.manaCost.add(new String((String)manaCostIter.next()));
            }
            this.id = raw.get("id").toString();
            this.types = new ArrayList<String>();
            Iterator<Object> typesIter = ((List<Object>)raw.get("type")).iterator();
            while (typesIter.hasNext()) {
                this.types.add(new String((String)typesIter.next()));
            }
            this.toughness = raw.get("power").toString();
        } catch (NullPointerException e) {
    		System.err.println("Could not convert the response to a Card; a field was missing.");
    		e.printStackTrace();
    	} catch (ClassCastException e) {
    		System.err.println("Could not convert the response to a Card; a field had the wrong structure.");
    		e.printStackTrace();
        }
    
	}	
}