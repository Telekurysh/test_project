from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import UserProfile, Order, OrderItem


# Сигналы для автоматического создания профиля пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# Сигналы для обновления общей стоимости заказа
@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_total_price(sender, instance, **kwargs):
    order = instance.order
    order.total_price = sum(item.product.price * item.quantity for item in order.orderitem_set.all())
    order.save()


# Сигналы для отправки уведомлений администратору о новых заказах
@receiver(post_save, sender=Order)
def send_admin_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New Order Created'
        message = f'A new order with ID {instance.id} has been created.'
        send_mail(subject, message, 'from@example.com', ['admin@example.com'])
