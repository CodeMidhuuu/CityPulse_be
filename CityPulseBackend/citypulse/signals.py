from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CivicIssue
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


# For sending email notification when a CivicIssue is created

@receiver(post_save, sender=CivicIssue)
def send_issue_notification(sender, instance, created, **kwargs):
    if created:  
        try:
            # Generate direct admin URL to the specific issue
            admin_url = reverse('admin:citypulse_civicissue_change', args=[instance.id])
            full_admin_url = f"{settings.SITE_URL}{admin_url}"

            # Generate Google Maps link if coordinates are available
            google_maps_link = ""
            if instance.latitude and instance.longitude:
                google_maps_link = f"https://www.google.com/maps?q={instance.latitude},{instance.longitude}"
            elif instance.location:
                google_maps_link = f"Manual location: {instance.location}"
            else:
                google_maps_link = "(Location not provided)"


            subject = f"🚨 New Civic Issue: {instance.subject}"
            message = f"""
            A new civic issue has been reported:

            Category: {instance.get_category_display()}
            Title: {instance.subject}
            Description: {instance.description}
            Reported At: {instance.reported_at.strftime('%Y-%m-%d %H:%M')}

            View on Map: {google_maps_link}
            Take action: {full_admin_url}
            """

            send_mail(
                subject,
                message.strip(),
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=not settings.DEBUG,
            )

        except Exception as e:
            if settings.DEBUG:
                raise