from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings

class Ad(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")],
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    text = models.TextField()
    
    picture = models.BinaryField(null=True, blank=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, blank=True,
                                    help_text='The MIMEType of the file')
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='fav_ad_owner')
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
                            through='Comment', related_name='comments_owned')

    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Fav', 
                                        related_name='favorite_ads')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self) -> str:
        if len(self.text) < 15: return self.text
        return f'{self.text[:11]} ...'

class Fav(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='favs_users')
    
    # https://docs.djangoproject.com/en/5.1/ref/models/options/#unique-together
    class Meta:
        unique_together = ('ad', 'user')
    
    def __str__(self):
        return f"{self.user.username} likes {self.ad.title[:10]}"
