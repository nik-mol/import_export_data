from rest_framework.response import Response


def celery_response(id):
    return Response({"task_id": id})
