from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Case, When
from django.conf import settings
from django.utils import timezone
from .utils import connect_to_web3, send_ether
from .serializers import TransactionSerializer
from .models import Transaction


class FundView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            wallet_address = serializer.validated_data['wallet_address']
            ip_address = request.META.get(
                'HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
            transaction = Transaction.objects.filter(
                ip_address=ip_address, wallet_address=wallet_address).order_by('-timestamp').first()
            if transaction and transaction.timestamp >= timezone.now() - timezone.timedelta(minutes=1):
                Transaction.objects.update_or_create(
                    wallet_address=wallet_address, ip_address=ip_address, status=Transaction.Status.FAILED, defaults={'timestamp': timezone.now()})
                return Response('Limit exceeded, try again later', status=status.HTTP_400_BAD_REQUEST)
            try:
                web3 = connect_to_web3(settings.ETH_TESTNET_RPC_URL)
                tx_hash = send_ether(
                    web3, settings.WALLET_ADDRESS, settings.PRIVATE_KEY, wallet_address, 0.0001)
                Transaction.objects.update_or_create(wallet_address=wallet_address, tx_hash=tx_hash, ip_address=ip_address,
                                                     status=Transaction.Status.SUCCESS, defaults={'timestamp': timezone.now()})
                return Response({'transaction_id': tx_hash}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatsView(APIView):
    def get(self, request):
        """
        Retrieves statistics for successful and failed transactions within the last 24 hours.
        """
        last_24_hours = timezone.now() - timezone.timedelta(hours=24)
        successful_transactions = Transaction.objects.filter(
            timestamp__gte=last_24_hours
        ).aggregate(
            successful_count=Count(Case(When(status='success', then=1)))
        )['successful_count']

        failed_transactions = Transaction.objects.filter(
            timestamp__gte=last_24_hours
        ).aggregate(
            failed_count=Count(Case(When(status='failed', then=1)))
        )['failed_count']

        return Response({
            'successful_transactions': successful_transactions,
            'failed_transactions': failed_transactions
        }, status=status.HTTP_200_OK)
