from distutils.command.upload import upload
from pickle import TRUE
from django.db import models
from django.dispatch import receiver
import os
#from uuid import uuid4
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import User
import hashlib
import random

# Create your models here.
#@deconstructible



def UploadToPathAndRename(instance, filename):

    upload_to = 'photos'
    name = filename.split('.')[0]
    ext = "png"
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(name, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def _createHash():
        """This function generate 10 character long hash"""
        hash = random.getrandbits(128)

        return("%032x" % hash)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='books/pdfs/')
    cover = models.ImageField(upload_to = 'books/covers',null=True,blank=True)

    def __str__(self):
        return self.title

class User_Info(models.Model):
    user = models.OneToOneField(User,null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    organisation = models.CharField(max_length=200, null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.user)

class Embed_Ownership_Text(models.Model):
    user_info =  models.ForeignKey(User_Info, null=True, on_delete= models.SET_NULL,max_length=1)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=100)
    file = models.FileField(upload_to='text/',null=False,blank=False)
    hash_url = models.CharField(max_length=50,default=_createHash,editable=False)

class Embed_Ownership_Image(models.Model):
    user_info =  models.ForeignKey(User_Info, null=True, on_delete= models.SET_NULL,max_length=1)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=100)
    file = models.ImageField(upload_to = UploadToPathAndRename,null=False,blank=False)
    hash_url = models.CharField(max_length=50,default=_createHash,editable=False)
    
    def __str__(self):
        return str(self.file)

class Embed_Ownership_Sound(models.Model):
    user_info =  models.ForeignKey(User_Info, null=True, on_delete= models.SET_NULL,max_length=1)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=100)
    file = models.FileField(upload_to = 'sound/',null=False,blank=False)
    hash_url = models.CharField(max_length=50,default=_createHash,editable=False)


class Embed_Enforcement_Text(models.Model):
    user_info =  models.ForeignKey(User_Info, null=True, on_delete= models.SET_NULL,max_length=1)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    file = models.FileField(upload_to='text/',null=False,blank=False)
    hash_url = models.CharField(max_length=50,default=_createHash,editable=False)

class Embed_Enforcement_Image(models.Model):
    user_info =  models.ForeignKey(User_Info, null=True, on_delete= models.SET_NULL,max_length=1)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    file = models.ImageField(upload_to = UploadToPathAndRename,null=False,blank=False)
    hash_url = models.CharField(max_length=50,default=_createHash,editable=False)

class Embed_Enforcement_Sound(models.Model):
    user_info =  models.ForeignKey(User_Info, null=True, on_delete= models.SET_NULL,max_length=1)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    file = models.FileField(upload_to = 'sound/',null=False,blank=False)
    hash_url = models.CharField(max_length=50,default=_createHash,editable=False)

class Extract_Embedded_Info(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    source_file = models.CharField(max_length=100,default="Extraction File")
    file = models.FileField(upload_to='extraction_files/',null=False,blank=False)
#querySet1.union(querySet2, querySet3, etc) #Minimum 1 argument

class Embedded_Files(models.Model):
    user_info =  models.ForeignKey(User_Info, null=True, on_delete= models.SET_NULL)
    #text_o_1 = models.ForeignKey(Embed_Ownership_Text, null=True, on_delete= models.SET_NULL)
    image_o_1 = models.ForeignKey(Embed_Ownership_Image, null=True, on_delete= models.SET_NULL)
    #sound_o_1 = models.ForeignKey(Embed_Ownership_Sound, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    #@property
    #def embedded_files(self):
    #    return self.text_o_1 + self.image_o_1 + self.sound_o_1