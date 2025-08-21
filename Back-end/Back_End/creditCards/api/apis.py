
from orders.models import Order
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from creditCards.models import CreditCards
from users.models import User
import stripe
from rest_framework import status
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentProcessViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        token_id = request.data.get('token', {}).get('id')
        amount = request.data.get('total')

        try:
            if not token_id:
                raise ValueError("No se proporcionó un token de tarjeta")
            
            if not amount:
                raise ValueError("No se proporcionó un monto")
            
            usuario = request.user
            charge = stripe.Charge.create(
                amount=int(amount) * 100,
                currency='EUR',
                description='Compra en línea',
                source=token_id,
            )
            CreditCards.objects.create(
                user=usuario,
                token=token_id,
                last_four_digits=request.data.get('token', {}).get('card', {}).get('last4'),
                mark=request.data.get('token', {}).get('card', {}).get('brand'),
            )
            
            pedido = Order.objects.filter(user=usuario, is_paid=False).last()
            if pedido:
                pedido.is_paid = True
                pedido.save()
            return Response({'success': True, 'message': 'Pago procesado exitosamente'})

        except ValueError as ve:
            return Response({'success': False, 'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.CardError as e:
            return Response({'success': False, 'error': e.error.message}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)