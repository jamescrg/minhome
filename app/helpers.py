
from datetime import datetime, date, time, timezone
from django.db.models import Model
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from django.http import JsonResponse
import pytz


def dump_model(instance):
    instance = model_to_dict(instance)
    return instance


def dump_set(queryset):
    qDict = []
    for instance in queryset:
        instance = model_to_dict(instance)
        qDict.append(instance)
    return qDict


def dump(result):
    if issubclass(type(result), Model):
        result = dump_model(result)
    elif isinstance(result, QuerySet):
        result = dump_set(result)
    elif type(result) is dict or list or str or float or int:
        result = result
    else:
        result = 'Input must be a a model instance, queryset, dict, string, int, list, or float.'
    return JsonResponse(result, safe=False)


def timestamp_to_eastern(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    dt = dt.replace(tzinfo=timezone.utc)
    tz = pytz.timezone('US/Eastern')
    dt = dt.astimezone(tz)
    return dt
