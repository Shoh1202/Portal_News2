from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post
from .utils import send_new_post_email

@receiver(post_save, sender=Post)
def notify_subscribers_on_new_post(sender, instance: Post, created, **kwargs):
    if not created:
        return  # письмо только при создании, не при каждом редактировании

    # ссылка
    post_url = settings.SITE_URL + instance.get_absolute_url()

    # первые 50 символов (можешь поменять число)
    text = getattr(instance, 'text', '') or ''
    preview = text[:50]

    category = instance.category  # если ForeignKey: Post.category
    subscribers = category.subscribers.exclude(email='').exclude(email__isnull=True)

    for user in subscribers:
        send_new_post_email(user, instance, post_url, preview)

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать!'
        message = f'''
        Здравствуйте, {instance.username}!

        Спасибо за регистрацию в нашем приложении.
        '''

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )