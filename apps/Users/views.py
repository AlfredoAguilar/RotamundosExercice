from rest_framework.views import APIView
from rest_framework.response import Response

from .Ejercicio import score


class ExerciceView(APIView):
    def get(self, request, name):
        result = score(name)
        return Response({"Resultado:": result}, 200)
