from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .authentication import APISessionAuthentication, JSONSingleTokenAuthentication

from .parsers import JSONParser
from .permissions import IsSecure


class overtimeAPIView(APIView):
    permission_classes = (IsSecure,)
    authentication_classes = (JSONSingleTokenAuthentication,)

    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    logging_key = None


class SessionAPIView(overtimeAPIView):

    authentication_classes = (JSONSingleTokenAuthentication, APISessionAuthentication)
