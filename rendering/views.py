import json

from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST

from .models import EmailTemplate


# TODO: http://jeremydorn.com/json-editor/
# https://github.com/jdorn/json-editor
# https://github.com/json-schema-faker/json-schema-faker
# https://github.com/marak/Faker.js/
# https://ariesfath.wordpress.com/2015/08/30/creating-a-json-editor-for-django-admin/
# https://github.com/glasslion/django-json-editor/blob/master/djjsoneditor/widgets.py
# http://schematic-ipsum.herokuapp.com

# https://spacetelescope.github.io/understanding-json-schema/reference/object.html


@require_POST
def render_template_endpoint(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        return HttpResponseBadRequest(
            'invalid JSON body: {}'.format(e))

    try:
        template_id = data['template_id']
        context = data['context']
    except KeyError:
        return HttpResponseBadRequest(data)

    # TODO: make this resource path '/templates/<id>/render/'
    # and remove 'template_id' from the data
    try:
        template = EmailTemplate.objects.get(id=template_id)
    except EmailTemplate.DoesNotExist:
        return HttpResponseBadRequest(
            'Template not found: {}'.format(template_id))

    try:
        result = template.render(context)
    except ValidationError as e:
        return HttpResponseBadRequest(
            'Invalid context schema: {}'.format(e))
    except Exception as e:
        return HttpResponseBadRequest(
            'Error rendering template: {}'.format(e))

    return JsonResponse(result)
