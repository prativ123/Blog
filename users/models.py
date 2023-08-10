from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    
    def __str__(self):
        return f'{self.user.username} Profile'
    

    # def save(self):
    #     super().save()

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)

        # When image height is greater than its width
        if img.height > img.width:
            # make square by cutting off equal amounts top and bottom
            left = 0
            right = img.width
            top = (img.height - img.width)/2
            bottom = (img.height + img.width)/2
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 300 or img.width >300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

        # When image width is greater than its height
        elif img.width > img.height:
            # make square by cutting off equal amounts left and right
            left = (img.width - img.height)/2
            right = (img.width + img.height)/2
            top = 0
            bottom = img.height
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 300 or img.width >300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)