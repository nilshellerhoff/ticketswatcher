import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter

def variable(value, name):
    json_str = json.dumps(value)
    # second encoding encodes quotes
    js_str = json.dumps(json_str)
    result = f"""
<script>
    var {name} = JSON.parse({js_str});
</script>"""
    return mark_safe(result)