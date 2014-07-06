package realtimeweb.stockservice.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;




/**
 * A structured representation of stock information, including ticker symbol, latest sale price, and price change since yesterday.
 */
public class Stock {
	
    private String lastTradeDate;
    private String lastTradeTime;
    private String exchange;
    private Double percentPriceChange;
    private Double lastSalePrice;
    private Integer id;
    private String ticker;
    private Double priceChange;
    
    
    /*
     * @return The entire date of the last trade.
     */
    public String getLastTradeDate() {
        return this.lastTradeDate;
    }
    
    /*
     * @param The entire date of the last trade.
     * @return String
     */
    public void setLastTradeDate(String lastTradeDate) {
        this.lastTradeDate = lastTradeDate;
    }
    
    /*
     * @return The time of the last trade.
     */
    public String getLastTradeTime() {
        return this.lastTradeTime;
    }
    
    /*
     * @param The time of the last trade.
     * @return String
     */
    public void setLastTradeTime(String lastTradeTime) {
        this.lastTradeTime = lastTradeTime;
    }
    
    /*
     * @return The name of the exchange (e.g. NASDAQ)
     */
    public String getExchange() {
        return this.exchange;
    }
    
    /*
     * @param The name of the exchange (e.g. NASDAQ)
     * @return String
     */
    public void setExchange(String exchange) {
        this.exchange = exchange;
    }
    
    /*
     * @return The percent price change since yesterday.
     */
    public Double getPercentPriceChange() {
        return this.percentPriceChange;
    }
    
    /*
     * @param The percent price change since yesterday.
     * @return Double
     */
    public void setPercentPriceChange(Double percentPriceChange) {
        this.percentPriceChange = percentPriceChange;
    }
    
    /*
     * @return The latest sale price for this stock.
     */
    public Double getLastSalePrice() {
        return this.lastSalePrice;
    }
    
    /*
     * @param The latest sale price for this stock.
     * @return Double
     */
    public void setLastSalePrice(Double lastSalePrice) {
        this.lastSalePrice = lastSalePrice;
    }
    
    /*
     * @return The unique ID number for this ticker symbol
     */
    public Integer getId() {
        return this.id;
    }
    
    /*
     * @param The unique ID number for this ticker symbol
     * @return Integer
     */
    public void setId(Integer id) {
        this.id = id;
    }
    
    /*
     * @return The Ticker Symbol (e.g. AAPL)
     */
    public String getTicker() {
        return this.ticker;
    }
    
    /*
     * @param The Ticker Symbol (e.g. AAPL)
     * @return String
     */
    public void setTicker(String ticker) {
        this.ticker = ticker;
    }
    
    /*
     * @return The price change since yesterday.
     */
    public Double getPriceChange() {
        return this.priceChange;
    }
    
    /*
     * @param The price change since yesterday.
     * @return Double
     */
    public void setPriceChange(Double priceChange) {
        this.priceChange = priceChange;
    }
    
	
	/**
	 * Creates a string based representation of this Stock.
	
	 * @return String
	 */
	public String toString() {
		return "Report[" +lastTradeDate+", "+lastTradeTime+", "+exchange+", "+percentPriceChange+", "+lastSalePrice+", "+id+", "+ticker+", "+priceChange+"]";
	}
	
	/**
	 * Internal constructor to create a Stock from a json representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    public Stock(Map<String, Object> raw) {
        // TODO: Check that the data has the correct schema.
        // NOTE: It's much safer to check the Map for fields than to catch a runtime exception.
        try {
            this.lastTradeDate = raw.get("lt").toString();
            this.lastTradeTime = raw.get("ltt").toString();
            this.exchange = raw.get("e").toString();
            this.percentPriceChange = Double.parseDouble(raw.get("cp").toString());
            this.lastSalePrice = Double.parseDouble(raw.get("l").toString());
            this.id = Integer.parseInt(raw.get("id").toString());
            this.ticker = raw.get("t").toString();
            this.priceChange = Double.parseDouble(raw.get("c").toString());
        } catch (NullPointerException e) {
    		System.err.println("Could not convert the response to a Stock; a field was missing.");
    		e.printStackTrace();
    	} catch (ClassCastException e) {
    		System.err.println("Could not convert the response to a Stock; a field had the wrong structure.");
    		e.printStackTrace();
        }
    
	}	
}