from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_new_post_email(user, post, post_url, preview):
    subject = post.title

    html = render_to_string('emails/new_post.html', {
        'user': user,
        'post': post,
        'post_url': post_url,
        'preview': preview,
    })
    msg = EmailMultiAlternatives(
        subject=subject,
        body=f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!\n{post_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(html, "text/html")
    msg.send()
