from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Post
User= get_user_model()
def send_weekly_digest():
    week_ago = timezone.now() - timedelta(days=7)
    recent_posts = Post.objects.filter(time_add=week_ago)
    users = User.objects.exclude(email="").exclude(email__isnull=True)
    for user in users:
        categories = user.subscribed_categories.all()
        if not categories.exists():
            continue
        user_posts = recent_posts.filter(category__in=categories).distinct()

        subject = "Новые статьи за неделю"
        html = render_to_string("emails/weekly_digest.html", {
            "user": user,
            "posts": user_posts,
            "site_url": settings.SITE_URL,  # например http://127.0.0.1:8000
        })
        msg = EmailMultiAlternatives(
            subject=subject,
            body="Новые статьи за неделю (откройте HTML-версию письма).",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
