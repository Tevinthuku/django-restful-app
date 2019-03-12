import json
from django.views.generic import View
from django.http import HttpResponse

from updates.models import Update as UpdatesModel
from updates.forms import UpdateModelForm

from cfeapi.utils import resolve_response, CSRFExemptMixin, is_json


class UpdateModelDetailApiView(CSRFExemptMixin, View):
    def get_object(self, id):
        try:
            obj = UpdatesModel.objects.get(id=id)
        except UpdatesModel.DoesNotExist:
            obj = None

        return obj

    def get(self, request, id, *args, **kwargs):
        obj = self.get_object(id)
        if obj:
            json_data = obj.serialize()
            return resolve_response(json_data)
        return resolve_response(json.dumps({"message": "Not found"}), status=404)

    def post(self, request, *args, **kwargs):
        json_data = json.dumps(
            {"message": "Not allowed, use the /api/updates endpoint"})
        return resolve_response(json_data, status=405)

    def put(self, request, id, *args, **kwargs):
        obj = self.get_object(id)
        if obj is None:
            return resolve_response(json.dumps({"message": "Not found"}), status=404)

        if not is_json(request.body):
            return resolve_response(json.dumps({"message": "Not valid json"}), status=400)

        data = json.loads(obj.serialize())
        passed_data = json.loads(request.body)
        for key, value in passed_data.items():
            data[key] = value
        form = UpdateModelForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            json_data = json.dumps(data)
            return resolve_response(json_data, status=200)
        return resolve_response(json.dumps(form.errors), status=400)

    def delete(self, request, id, *args, **kwargs):
        obj = self.get_object(id)
        if obj:
            obj.delete()
            message = json.dumps({"message": "Successfully deleted object"})
            return resolve_response(message)
        return resolve_response(json.dumps({"message": "Not found"}), status=404)

class UpdateModelListApiView(CSRFExemptMixin, View):
    def get(self, request, *args, **kwargs):
        json_data = UpdatesModel.objects.all().serialize()
        return resolve_response(json_data)

    def post(self, request, *args, **kwargs):
        if not is_json(request.body):
            return resolve_response(json.dumps({"message": "Not valid json"}), status=400)
        form = UpdateModelForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=True)
            json_data = obj.serialize()
            return resolve_response(json_data, status=201)
        return resolve_response(json.dumps(form.errors), status=400)

    def delete(self, request, *args, **kwargs):
        json_data = json.dumps({"message": "You cannot delete an entire list"})
        return resolve_response(json_data)
