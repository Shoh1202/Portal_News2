from celery import shared_task
from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


from .models import Post, Category

@shared_task
def send_news_to_subscribers(news_id: int):
    news = Post.objects.select_related("category").get(id=news_id)


    subscribers = Post.categories.subscribers.all()

    if not subscribers.exists():
        return "No subscribers"

    preview = Post.text[:50]
    subject = Post.title
    link = f"{settings.SITE_URL}/news/{news.id}/"

    sent_count = 0

    for user in subscribers:
        if not user.email:
            continue

        html_body = render_to_string(
            "emails/new_article.html",
            {"user": user, "news": Post, "preview": preview, "link": link},
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()

        sent_count += 1

    return f"Sent {sent_count} emails"

@shared_task
def send_weekly_digest():

    now = timezone.now()
    week_ago = now - timedelta(days=7)


    weekly_news = (
        Post.objects
        .select_related("category")
        .filter(created_at__gte=week_ago, created_at__lt=now)
        .order_by("-created_at")
    )

    if not weekly_news.exists():
        return "No news for the last week"


    news_by_category = {}
    for item in weekly_news:
        news_by_category.setdefault(item.category_id, []).append(item)


    categories = (
        Category.objects
        .prefetch_related("subscribers")
        .filter(id__in=news_by_category.keys())
    )


    sent_to = set()


    user_news = {}

    for cat in categories:
        cat_news = news_by_category.get(cat.id, [])
        for user in cat.subscribers.all():
            if not user.email:
                continue
            user_news.setdefault(user.id, {"user": user, "items": []})
            user_news[user.id]["items"].extend(cat_news)


    total_sent = 0

    for data in user_news.values():
        user = data["user"]


        unique_items = {n.id: n for n in data["items"]}.values()
        items_sorted = sorted(unique_items, key=lambda n: n.created_at, reverse=True)

        subject = "Еженедельный дайджест новостей"


        site = getattr(settings, "SITE_URL", "http://127.0.0.1:8000")

        html_body = render_to_string(
            "emails/weekly_digest.html",
            {
                "user": user,
                "items": items_sorted,
                "site": site,
                "week_ago": week_ago,
                "now": now,
            },
        )

        text_body = f"Привет, {user.username}! Новости за неделю: {site}"

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()
        total_sent += 1

    return f"Sent weekly digest to {total_sent} users"