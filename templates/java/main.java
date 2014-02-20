package realtimeweb.{{ metadata.name | flat_case }};

import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.util.HashMap;

import realtimeweb.{{ metadata.name | flat_case }}.domain.*;
import realtimeweb.stickyweb.Pattern;
import realtimeweb.stickyweb.StickyWeb;
import realtimeweb.stickyweb.StickyWebRequest;
import realtimeweb.stickyweb.exceptions.StickyWebDataSourceNotFoundException;
import realtimeweb.stickyweb.exceptions.StickyWebDataSourceParseException;
import realtimeweb.stickyweb.exceptions.StickyWebInternetException;
import realtimeweb.stickyweb.exceptions.StickyWebJsonResponseParseException;
import realtimeweb.stickyweb.exceptions.StickyWebLoadDataSourceException;
import realtimeweb.stickyweb.exceptions.StickyWebNotInCacheException;

public class {{ metadata.name | camel_case_caps }} {
	private StickyWeb connection;
	private boolean online;
	
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
	
	public {{ metadata.name | camel_case_caps }}(InputStream cache) throws StickyWebDataSourceNotFoundException, StickyWebDataSourceParseException, StickyWebLoadDataSourceException {
		this.online = false;
		this.connection = new StickyWeb(cache);
	}
    
    {% for function in functions %}
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
            , String.valueOf({{ parameter.name }})
        {%- endfor -%}
        );
		HashMap<String, String> parameters = new HashMap<String, String>();
        {% for parameter in function.payload_inputs %}
        parameters.put({{ parameter.name }}, String.valueOf({{ parameter.path }}));
        {% endfor %}
		parameters.put("lat", String.valueOf(latitude));
		parameters.put("lon", String.valueOf(longitude));
		parameters.put("FcstType", String.valueOf("json"));
		
		try {
			StickyWebRequest request = connection.get(url, parameters)
					.setOnline(online)
					.setPattern(Pattern.EMPTY);
			return new Report(request.execute().asJSON());
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
	
	public static void main(String args[]) {
		Weather weather = new Weather();
		Report saved = weather.getWeather(37, -80);
	}
}
