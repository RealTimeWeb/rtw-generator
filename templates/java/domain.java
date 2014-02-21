package realtimeweb.{{ metadata.name | flat_case }}.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

{% if object.format == "xml" %}
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Document;
import com.sun.org.apache.xpath.internal.NodeSet;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathFactory;
{% elif object.format == "html" %}
import org.htmlcleaner.TagNode;
{% endif %}

{% for dependency in object.dependencies if not (dependency | is_builtin) -%}
import realtimeweb.{{ metadata.name | flat_case }}.domain.{{dependency | camel_case_caps}};
{% endfor %}
/**
 * {{ object.description }}
 */
public class {{ object.name | camel_case_caps }} {
	{% if object.comment %}
    // {{ object.comment }}
    {% endif -%}
	{% for field in object.fields %}
    {% if field.comment -%}
    // {{ field.comment }}
    {% endif -%}
    private {{field.type | to_java_type}} {{field.name | camel_case }};
    {%- endfor %}
    
    {% for field in object.fields %}
    /*
     * @return {{ field.description }}
     */
    public {{field.type | to_java_type}} get{{field.name | camel_case_caps }}() {
        return this.{{field.name | camel_case }};
    }
    
    /*
     * @param {{ field.description }}
     * @return {{field.type | to_java_type}}
     */
    public void set{{field.name | camel_case_caps }}({{field.type | to_java_type}} {{field.name | camel_case }}) {
        this.{{field.name | camel_case }} = {{field.name | camel_case }};
    }
    {% endfor %}
	
	/**
	 * Creates a string based representation of this {{ object.name | camel_case_caps }}.
	
	 * @return String
	 */
	public String toString() {
		return "Report[" + 
        {%- for field in object.fields -%}
        {{field.name | camel_case }}+ 
        {%- if not loop.last -%}
        ", "+
        {%- endif -%}
        {%- endfor -%}
        "]";
	}
	
	/**
	 * Internal constructor to create a {{ object.name | camel_case_caps }} from a {{ object.format }} representation.
	 * @param map The raw json data that will be parsed.
	 * @return 
	 */
    {% if object.format == "json" %}
    public {{ object.name | camel_case_caps }}(Map<String, Object> raw) {
        {% for field in object.fields -%}
        {% if field.type | is_list %}
        this.{{ field.name | camel_case }} = new {{ field.type | to_java_type }}();
        Iterator<{{ field.type | strip_list | to_java_type }}> {{ field.name | camel_case }}Iter = ((List<{{ field.type | strip_list | to_java_type }}>){{ field.path | parse_json_path}}).iterator();
        while ({{ field.name | camel_case }}Iter.hasNext()) {
            this.{{ field.name | camel_case }}.add(new {{ field.type | strip_list | to_java_type }}((Map<String, Object>){{ field.name | camel_case }}Iter.next()));
        }
        {%- else %}
        this.{{ field.name | camel_case }} = {{ field.path | parse_json_path | create_json_conversion(field.type)}};
        {%- endif %}
        {%- endfor %}
    {% elif object.format == "xml" %}
    public {{ object.name | camel_case_caps }}(Node raw) {
        XPath xPath =  XPathFactory.newInstance().newXPath();
        {% for field in object.fields -%}
        {% if field.type | is_list %}
        NodeList {{ field.name | camel_case}}Items = (NodeList) xPath.evaluate("{{ field.path }}", raw, XPathConstants.NODESET);
        this.{{ field.name | camel_case }} = new {{ field.type | to_java_type }}();
        for (int i = 0; i < {{ field.name | camel_case}}Items.getLength(); i++) {
            Node aNode = {{ field.name | camel_case}}Items.get(i);
            {%- if field.type | is_builtin %}
            this.{{ field.name | camel_case }}.add({{ field.type | strip_list | convert_builtin}}(aNode.toString()));
            {%- else %}
            this.{{ field.name | camel_case }}.add(new {{ field.type | strip_list | to_java_type }}(aNode));
            {% endif %}
        }
        {%- elif field.type | is_builtin %}
        this.{{ field.name | camel_case }} = xPath.evaluate("{{ field.path }}", raw, {{ field.type | create_xml_conversion }});
        {%- else %}
        this.{{ field.name | camel_case }} = new {{ field.type | camel_case_caps }}(xPath.evaluate("{{ field.path }}", raw, XPathConstants.NODE));
        {%- endif %}
        {%- endfor %}
    {% elif object.format == "html" %}
    public {{ object.name | camel_case_caps }}(TagNode raw) {
        {% for field in object.fields -%}
        {% if field.type | is_list %}
        Object[] {{ field.name | camel_case}}Items = raw.evaluateXPath("{{ field.path }}");
        this.{{ field.name | camel_case }} = new {{ field.type | to_java_type }}();
        for (int i = 0; i < {{ field.name | camel_case}}Items.length; i++) {
            TagNode aNode = (TagNode){{ field.name | camel_case}}Items[i];
            {%- if field.type | strip_list | is_builtin %}
            this.{{ field.name | camel_case }}.add({{ field.type | strip_list | convert_builtin}}(aNode.toString()));
            {%- else %}
            this.{{ field.name | camel_case }}.add(new {{ field.type | strip_list | to_java_type }}(aNode));
            {% endif %}
        }
        {%- elif field.type | is_builtin %}
        this.{{ field.name | camel_case }} = {{ ('raw.evaluateXPath("' + field.path + '")') | create_json_conversion(field.type) }};
        {%- else %}
        this.{{ field.name | camel_case }} = new {{ field.type | camel_case_caps }}((TagNode) raw.evaluateXPath("{{ field.path }}"));
        {%- endif %}
        {%- endfor %}
    {% endif %}
	}	
}
