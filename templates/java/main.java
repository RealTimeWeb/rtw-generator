package realtimeweb.{{ metadata.name | flat_case }};

import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.util.HashMap;

{% if "xml" in formats_required -%}
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathFactory;
{%- endif %}

import realtimeweb.{{ metadata.name | flat_case }}.domain.*;
import realtimeweb.stickyweb.StickyWeb;
import realtimeweb.stickyweb.StickyWebRequest;
import realtimeweb.stickyweb.exceptions.StickyWebException;
import realtimeweb.stickyweb.exceptions.StickyWebDataSourceNotFoundException;
import realtimeweb.stickyweb.exceptions.StickyWebDataSourceParseException;
import realtimeweb.stickyweb.exceptions.StickyWebInternetException;
import realtimeweb.stickyweb.exceptions.StickyWebJsonResponseParseException;
import realtimeweb.stickyweb.exceptions.StickyWebLoadDataSourceException;
import realtimeweb.stickyweb.exceptions.StickyWebNotInCacheException;

/**
 * {{ metadata.description }}
 */
public class {{ metadata.name | camel_case_caps }} {
    {% if metadata.comment %}
    // {{ metadata.comment }}
    {% endif -%}
	private StickyWeb connection;
	private boolean online;
	
    /**
     * Create a new, online connection to the service
     */
	public {{ metadata.name | camel_case_caps }}() {
		this.online = true;
		try {
			this.connection = new StickyWeb(null);
		} catch (StickyWebDataSourceNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (StickyWebDataSourceParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (StickyWebLoadDataSourceException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
    /**
     * Create a new, offline connection to the service.
     * @param cache An InputStream that can serve data for the connection.
     */
	public {{ metadata.name | camel_case_caps }}(InputStream cache) throws StickyWebDataSourceNotFoundException, StickyWebDataSourceParseException, StickyWebLoadDataSourceException {
		this.online = false;
		this.connection = new StickyWeb(cache);
	}
    
    public static void main(String[] args) {
        {{ metadata.name | camel_case_caps }} {{ metadata.name | camel_case }} = new {{ metadata.name | camel_case_caps }}();
    }
    
    {% for function in functions %}
    /**
     * {{ function.description }}
    {% for input in (function.payload_inputs + function.url_inputs) | rejectattr("hidden") %}
     * @param cache {{ input.description }}
    {%- endfor %}
     * @return a {{ function.output }}
     */
	public {{ function.output | to_java_type }} {{ function.name | camel_case }}(
    {%- for input in (function.payload_inputs + function.url_inputs) | rejectattr("hidden") -%}
        {{ input.type | to_java_type }} {{input.name | camel_case }}
        {%- if not loop.last -%}
        , 
        {%- endif -%}
    {%- endfor -%}
    ) {
		final String url = String.format("{{ function.url | convert_url_parameters }}"
        {%- for parameter in function.url_inputs -%}
        {%- if parameter.hidden -%}
            , "{{ parameter.default }}"
        {%- else -%}
            , String.valueOf({{ parameter.name }})
        {%- endif -%}
        {%- endfor -%}
        );
		HashMap<String, String> parameters = new HashMap<String, String>();
        {% for parameter in function.payload_inputs %}
        {%- if parameter.hidden -%}
        parameters.put("{{ parameter.path }}", "{{ parameter.default }}");
        {%- else -%}
        parameters.put("{{ parameter.path }}", String.valueOf({{ parameter.name }}));
        {%- endif -%}
        {% endfor -%}

		try {
			StickyWebRequest request = connection.get(url, parameters).setOnline(online);
            {% if function.format == "xml" -%}
                {%- if function.post == "" -%}
            return new {{ function.output | to_java_type }}(request.execute().asXML());
                {%- else -%}
            XPath xPath =  XPathFactory.newInstance().newXPath();
            return new {{ function.output | to_java_type }}(xPath.compile("{{ function.post }}").evaluate(request.execute().asXML()));
                {%- endif -%}
            {%- elif function.format == "html" -%}
                {%- if function.post == "" -%}
            return new {{ function.output | to_java_type }}(request.execute().asHTML());
                {%- else -%}
            // TODO: Probably want to cast to (org.htmlcleaner.TagNode) and manipulate data
            return new {{ function.output | to_java_type }}(request.execute().asHTML().evaluateXPath("{{ function.post }}"));
                {%- endif -%}
            {%- elif function.format == "json" -%}
            // TODO: Might need to cast some intermediary steps
            {% if function.post == "" -%}
            return new {{ function.output | to_java_type }}(request.execute().asJSON());
            {%- else -%}
            return new {{ function.output | to_java_type }}(request.execute().asJSON(){{ function.post | parse_json_path }});
                {%- endif -%}
            {%- elif function.format == "text" -%}
                return new {{ function.output | to_java_type }}(request.execute().asText());
            {%- elif function.format == "csv" -%}
                {%- if function.post == "" -%}
            return new {{ function.output | to_java_type }}(request.execute().asCSV());
                {%- else -%}
            return new {{ function.output | to_java_type }}(request.execute().asCSV().get({{ function.post }}));
                {%- endif -%}
            {%- endif %}
		} catch (IllegalStateException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (URISyntaxException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (StickyWebException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}
    {% endfor %}
}
