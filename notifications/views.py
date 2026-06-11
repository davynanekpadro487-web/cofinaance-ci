from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Lister mes notifications"
    )
    def get_queryset(self):
        return Notification.objects.filter(
            destinataire=self.request.user
        )

class MarquerLuView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Marquer une notification comme lue",
        responses={200: NotificationSerializer}
    )
    def patch(self, request, pk):
        try:
            notif = Notification.objects.get(
                pk=pk, destinataire=request.user
            )
        except Notification.DoesNotExist:
            return Response(
                {"error": "Notification introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )
        notif.est_lu = True
        notif.save()
        return Response(NotificationSerializer(notif).data)

class MarquerToutLuView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Marquer toutes les notifications comme lues",
        responses={200: {"description": "Succès"}}
    )
    def patch(self, request):
        Notification.objects.filter(
            destinataire=request.user, est_lu=False
        ).update(est_lu=True)
        return Response(
            {"message": "Toutes les notifications marquées comme lues."}
        )
