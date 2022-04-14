from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User_Info,Embedded_Files,Embed_Ownership_Image
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        User_Info.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )
        print('Profile created')

# post_save.connect(create_profile,sender=User)


@receiver(post_save, sender=User)
def update_profiles(sender, instance, created, **kwargs):
    if created == False:
        # breakpoint()
        instance.user_info.save()
        print('Profile updated')

# post_save.connect(update_profiles,sender=User)

