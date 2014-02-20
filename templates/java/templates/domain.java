package realtimeweb.{{package.name}}.domain;

{% for requirement in requirements %}
import {{requirement}};
{% endfor %}


/**
 * {{ object.description }}
 */
public class {{object.name}} {
    {% if object.comment %}
    //{{object.comment}}
    {% endif %}
	
	{% for field in object.fields %}
    {% if field.comment %}
    //{{field.comment}}
    {% endif %}
    private {{field.type}} {{field.name}};
    {% endfor %}
	
    {% for field in object.fields %}
    /**
     * {{field.description}}
     * @return {{field.type}}
     */
    public {{field.type}} {{field.getter}}() {
        return this.{{field.name}};
    }
    
    /**
     * @param {{field.name}} {{field.description}}
     */
    public void {{field.setter}}({{field.type}} {{field.name}}) {
        this.{{field.name}} = {{field.name}};
    }
    {% endfor %}
	
	/**
	 * A string representation of this object.
	
	 * @return String
	 */
	public String toString() {
		return "{{object.name}}[" + {{ object.fields|join(" + ") }} + "]";
	}
	
	/**
	 * Internal constructor to create a BoundingBox from a Json representation.
	 * @param json The raw json data that will be parsed.
	 * @param gson The Gson parser. See <a href='https://code.google.com/p/google-gson/'>https://code.google.com/p/google-gson/</a> for more information.
	 * @return 
	 */
	public  BoundingBox(JsonArray json, Gson gson) {
		this.minimumLongitude = json.get(0).getAsDouble();
		this.minimumLatitude = json.get(1).getAsDouble();
		this.minimumDepth = json.get(2).getAsDouble();
		this.maximumLongitude = json.get(3).getAsDouble();
		this.maximumLatitude = json.get(4).getAsDouble();
		this.maximumDepth = json.get(5).getAsDouble();
	}
	
	public BoundingBox(ArrayList<Object> data) {
		this.minimumLongitude = Double.parseDouble(data.get(0).toString());
		this.minimumLatitude = Double.parseDouble(data.get(1).toString());
		this.minimumDepth = Double.parseDouble(data.get(2).toString());
		this.maximumLongitude = Double.parseDouble(data.get(3).toString());
		this.maximumLatitude = Double.parseDouble(data.get(4).toString());
		this.maximumDepth = Double.parseDouble(data.get(5).toString());
	}
	
	/**
	 * Regular constructor to create a BoundingBox.
	 * @param minimumLongitude The lower longitude (West) component.
	 * @param minimumLatitude The lower latitude (South) component.
	 * @param minimumDepth The lower depth (closer or farther from the surface) component.
	 * @param maximumLongitude The higher longitude (East) component.
	 * @param maximumLatitude The higher latitude (North) component.
	 * @param maximumDepth The higher depth (closer or farther from the surface) component.
	 * @return 
	 */
	public  BoundingBox(double minimumLongitude, double minimumLatitude, double minimumDepth, double maximumLongitude, double maximumLatitude, double maximumDepth) {
		this.minimumLongitude = minimumLongitude;
		this.minimumLatitude = minimumLatitude;
		this.minimumDepth = minimumDepth;
		this.maximumLongitude = maximumLongitude;
		this.maximumLatitude = maximumLatitude;
		this.maximumDepth = maximumDepth;
	}
	
}
