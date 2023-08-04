import http
from traceback import format_exception_only
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

from my_platform.audiowatermarking.spectrum_ import embed_sound, move_sound_dep
from my_platform.mysql_connector import open_db_conn, close_db_conn
from my_platform.image_watermark_embed import watermark_embed
from my_platform.image_watermark_extract import watermark_extract
from my_platform.pdf_watermark_embed import pdf_embed_watermark
from my_platform.pdf_watermark_extract import pdf_extract_watermark
from .forms import Embed_Ownership_Image_Form, Embed_Enforcement_Sound_Form, Embed_Enforcement_Text_Form, Embed_Enforcement_Image_Form, Embed_Ownership_Sound_Form, Embed_Ownership_Text_Form, CreateUserForm, UserForm, Extract_Embedded_Text_Form, Extract_Embedded_Sound_Form, Extract_Embedded_Image_Form
from .models import Embed_Ownership_Text, Embed_Ownership_Image, Embed_Enforcement_Sound, Embed_Enforcement_Text, Embed_Enforcement_Image, Embed_Ownership_Sound, User_Info, Embedded_Files, Extract_Embedded_Text, Extract_Embedded_Sound, Extract_Embedded_Image
from pathlib import Path
from itertools import chain
import hashlib
from PIL import Image
from my_platform.hash import get_hash
import datetime
import io
import sys
from app.settings import MEDIA_ROOT, AUDIO_ROOT
from django.urls import reverse

def my_view(request):
    reversed_urls = {
        'index': reverse(''),
        'menu_embed': reverse('menu_embed'),
        'menu_extraction': reverse('menu_extraction'),
        'embedded_files': reverse('embedded_files'),
        'about_us': reverse('about_us'),
        'services': reverse('services'),
        'account_profile': reverse('account_profile'),
        'logout': reverse('logout/'),
        '/how_it_works/': reverse('how_it_works'),
        'login': reverse('login/'),
    }
    
    return render(request, 'base.html', {'reversed_urls': reversed_urls})

def index(request):
    return render(request, 'home.html')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            #breakpoint()
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                messages.success(
                    request, 'Account was created for ' + username)
                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def loginPage(request):
    
    if request.user.is_authenticated:
        return redirect('index')
    else:

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')

            else:
                messages.info(request, "USERNAME OR PASSWORD IS INCORRECT")
                return render(request, 'login.html')

        return render(request, 'login.html')


def account_profile(request):

    current_user = request.user.user_info
    form = UserForm(instance=current_user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()

        context = {'form': form}
        messages.success(
            request, 'Your profile information was successfully updated ' + current_user.name)

        return render(request, 'account_profile.html', context)

    else:
        context = {'form': form}
        return render(request, 'account_profile.html', context)


def about_us(request):
    return render(request, 'about_us.html')

def how_it_works(request):
    return render(request, 'how_it_works.html')

def services(request):
    return render(request, 'services.html')


def error(request):
    return render(request, 'error.html')


@login_required(login_url='login')
def menu_embed(request):
    if request.user.is_authenticated:
        return render(request, 'menu_embed.html')
    else:
        messages.info(request, "Please login or create an account")
        return render(request, 'login.html')


@login_required(login_url='login')
def menu_extraction(request):
    if request.user.is_authenticated:
        return render(request, 'menu_extraction.html')
    else:
        messages.info(request, "Please login or create an account")
        return render(request, 'login.html')


@login_required(login_url='login')
def embed_ownership(request):
    return render(request, 'embed_ownership.html')


@login_required(login_url='login')
def embed_enforcement(request):
    return render(request, 'embed_enforcement.html')


@login_required(login_url='login')
def embed_ownership_text(request):
    current_user_info = request.user.user_info
    current_user_email = request.user.email

    if request.method == 'POST':
        form = Embed_Ownership_Text_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            last_object = Embed_Ownership_Text.objects.all().last()
            # last_object_location = Path.cwd()/"media"/f"{last_object.file}"
            last_object_location = MEDIA_ROOT + f"{last_object.file}"
            embed_info_1 = "Owner: " + f"{last_object.owner}"
            embed_info_2 = "Timestamp: " + str(datetime.datetime.now())
            watermarkInfo = embed_info_1 + "_" + embed_info_2

            try:
                """if it passes it will be an embedded file, almost have a double security system"""
                pdf_embed_watermark(last_object_location,
                                    watermarkInfo, last_object_location)
                last_object.hash = get_hash(last_object_location)
                """write information to myAdmin Sql"""
                #mydb, mycursor = open_db_conn()
                #sql = "INSERT INTO digital_ownership_tbl (user_contact,file,embedded_watermark,hash,owner) VALUES(%s,%s,%s,%s,%s)"#
    ##
                #user_contact = str(current_user_email)
                #file = str(last_object.file)
                #embedded_watermark = 'no_watermark_info'
                #hash = last_object.hash
                #owner = last_object.owner
    #
                #val = (user_contact, file, embedded_watermark, hash, owner)
                #mycursor.execute(sql, val)
                # mydb.commit()

                messages.success(request, 'File has been embedded  ' +
                                 current_user_info.name + '. Go to Embedded Files to download document. ')
                return render(request, 'embed_ownership_text.html', {'last_object': last_object, 'form': form, 'watermarkInfo': watermarkInfo})

            except:
                """if it doesnt pass the hash of the file will be stored in the historic database and the person is the owner"""

                last_object.hash = get_hash(last_object_location)

                """write information to myAdmin Sql"""
                #mydb, mycursor = open_db_conn()
                #sql = "INSERT INTO digital_ownership_tbl (user_contact,file,embedded_watermark,hash,owner) VALUES(%s,%s,%s,%s,%s)"#
    ##
                #user_contact = str(current_user_email)
                #file = str(last_object.file)
                #embedded_watermark = watermarkInfo
                #hash = last_object.hash
                #owner = last_object.owner
    #
                #val = (user_contact, file, embedded_watermark, hash, owner)
                #mycursor.execute(sql, val)
                # mydb.commit()

                messages.error(request, 'FileType Error: File embedding failed. Hash of original file stored as record for ' +
                               current_user_info.name + '. Go to Embedded Files to download document. ')
                return render(request, 'embed_ownership_text.html', {'last_object': last_object, 'form': form, 'watermarkInfo': last_object.hash})

    else:
        #
        form = Embed_Ownership_Image_Form(
            initial={'user_info': current_user_info})
        form.fields['user_info']._queryset = current_user_info

    return render(request, 'embed_ownership_text.html', {'form': form})


@login_required(login_url='login')
def embed_ownership_image(request):

    # information regarding the current user
    current_user_info = request.user.user_info
    current_user_email = request.user.email

    if request.method == 'POST':

        form = Embed_Ownership_Image_Form(request.POST, request.FILES,)
        if form.is_valid():
            form.save()

            last_object = Embed_Ownership_Image.objects.all().last()
            # last_object_location = Path.cwd()/"media"/f"{last_object.file}"
            last_object_location = MEDIA_ROOT + f"{last_object.file}"
            embed_info_1 = "Owner: " + f"{last_object.owner}"
            embed_info_2 = "Timestamp: " + str(datetime.datetime.now())
            watermarkInfo = embed_info_1 + "_" + embed_info_2

            try:
                watermark_embed(last_object_location,
                                watermarkInfo, last_object_location)
                last_object.hash = get_hash(last_object_location)

                """write information to myAdmin Sql"""
                mydb, mycursor = open_db_conn()
                sql = "INSERT INTO digital_ownership_tbl (user_contact,file,embedded_watermark,hash,owner) VALUES(%s,%s,%s,%s,%s)"

                user_contact = str(current_user_email)
                file = str(last_object.file)
                embedded_watermark = watermarkInfo
                hash = last_object.hash
                owner = last_object.owner

                val = (user_contact, file, embedded_watermark, hash, owner)
                mycursor.execute(sql, val)
                mydb.commit()

                close_db_conn(mydb, mycursor)

                messages.success(request, 'File has been embedded  ' +
                                 current_user_info.name + '. Go to Embedded Files to download document. ')
                return render(request, 'embed_ownership_image.html', {'last_object': last_object, 'form': form, 'watermarkInfo': watermarkInfo})

            except:
                last_object.hash = get_hash(last_object_location)

                """write information to myAdmin Sql"""
                mydb, mycursor = open_db_conn()
                sql = "INSERT INTO digital_ownership_tbl (user_contact,file,embedded_watermark,hash,owner) VALUES(%s,%s,%s,%s,%s)"

                user_contact = str(current_user_email)
                file = str(last_object.file)
                embedded_watermark = 'no_watermark_info'
                hash = last_object.hash
                owner = last_object.owner

                val = (user_contact, file, embedded_watermark, hash, owner)
                mycursor.execute(sql, val)
                mydb.commit()

                close_db_conn(mydb, mycursor)

                messages.success(request, 'FileType Error: File embedding failed. Hash of original file stored as record for ' +
                                 current_user_info.name + '. Go to Embedded Files to download document. ')
                return render(request, 'embed_ownership_image.html', {'last_object': last_object, 'form': form, 'watermarkInfo': last_object.hash})

    else:
        #
        form = Embed_Ownership_Image_Form(
            initial={'user_info': current_user_info})
        form.fields['user_info']._queryset = current_user_info

    return render(request, 'embed_ownership_image.html', {'form': form})


@login_required(login_url='login')
def embed_ownership_sound(request):
    # information regarding the current user
    current_user_info = request.user.user_info
    current_user_email = request.user.email

    if request.method == 'POST':

        form = Embed_Ownership_Sound_Form(request.POST, request.FILES,)
        if form.is_valid():
            form.save()

            try:

                # We dont do the normal embedding this side, we use the hash
                last_object = Embed_Ownership_Sound.objects.all().last()
                last_object_location = MEDIA_ROOT + f"{last_object.file}"
                embed_sound(last_object_location, 'host1.wav')
                raw__file = f"{last_object.file}".split('/')[-1]
                file_name = "encoded" + raw__file

                # move file to relevant folder
                move_sound_dep(raw__file, file_name)
                embedded_sound_location = 'sound/' + 'encoded' + raw__file
                last_object.hash = get_hash(
                    MEDIA_ROOT + embedded_sound_location)

                """write information to myAdmin Sql"""
                mydb, mycursor = open_db_conn()
                sql = "INSERT INTO digital_ownership_tbl (user_contact,file,embedded_watermark,hash,owner) VALUES(%s,%s,%s,%s,%s)"
#
                user_contact = str(current_user_email)
                file = raw__file
                embedded_watermark = last_object.owner
                hash = last_object.hash
                owner = last_object.owner

                val = (user_contact, file, embedded_watermark, hash, owner)
                mycursor.execute(sql, val)
                mydb.commit()

                close_db_conn(mydb, mycursor)

                messages.success(request, 'File has been embedded  ' +
                                 current_user_info.name + '. Go to Embedded Files to download document. ')
                return render(request, 'embed_ownership_sound.html', {'last_object': last_object, 'form': form})

            except:
                return HttpResponse("File failure to upload")

    else:
        # return HttpResponse("Something up with the form")
        form = Embed_Ownership_Image_Form(
            initial={'user_info': current_user_info})
        form.fields['user_info']._queryset = current_user_info

        return render(request, 'embed_ownership_sound.html', {'form': form})


@login_required(login_url='login')
def embed_enforcement_text(request):
    current_user_info = request.user.user_info
    current_user_email = request.user.email

    if request.method == 'POST':
        form = Embed_Enforcement_Text_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            last_object = Embed_Enforcement_Text.objects.all().last()
            last_object_location = MEDIA_ROOT + f"{last_object.file}"
            embed_info_1 = "Owner: " + f"{last_object.owner}"
            embed_info_2 = "Timestamp: " + str(datetime.datetime.now())
            embed_info_3 = "Reciever: " + f"{last_object.receiver}"
            watermarkInfo = embed_info_1 + "-" + embed_info_3 + "_" + embed_info_2

            try:

                """If it passes it will be an embedded file, almost have a double security system
                    Potential Point of failer is only the Hash at this point
                """

                pdf_embed_watermark(last_object_location,
                                    watermarkInfo, last_object_location)

                last_object.hash = get_hash(last_object_location)

                """write information to myAdmin Sql"""
                mydb, mycursor = open_db_conn()
                sql = "INSERT INTO digital_enforcement_tbl (user_contact,file,embedded_watermark,hash,owner,receiver) VALUES(%s,%s,%s,%s,%s,%s)"
    #
                user_contact = str(current_user_email)
                file = str(last_object.file)
                embedded_watermark = watermarkInfo
                hash = last_object.hash
                owner = last_object.owner
                receiver = last_object.receiver

                val = (user_contact, file, embedded_watermark,
                       hash, owner, receiver)
                mycursor.execute(sql, val)
                mydb.commit()

                close_db_conn(mydb, mycursor)

                messages.success(request, 'File has been embedded  ' +
                                 current_user_info.name + '. Go to Embedded Files to download document. ')
                return render(request, 'embed_enforcement_text.html', {'last_object': last_object, 'form': form, 'watermarkInfo': watermarkInfo})

            except:

                """if it doesnt pass the hash of the file will be stored in the historic database and the person is the owner
                    Potential Point of failer is only the Hash at this point
                    """

                """write information to myAdmin Sql"""
                mydb, mycursor = open_db_conn()
                sql = "INSERT INTO digitalenforcement_tbl (user_contact,file,embedded_watermark,hash,owner,receiver) VALUES(%s,%s,%s,%s,%s,%s)"
    #
                user_contact = str(current_user_email)
                file = str(last_object.file)
                embedded_watermark = 'no_watermark_info'
                hash = last_object.hash
                owner = last_object.owner
                receiver = last_object.receiver

                val = (user_contact, file, embedded_watermark,
                       hash, owner, receiver)
                mycursor.execute(sql, val)
                mydb.commit()
                close_db_conn(mydb, mycursor)

                last_object.hash = get_hash(last_object_location)

                messages.error(request, 'File embedding failed. Hash of original file stored as record for ' +
                               current_user_info.name + '. Go to Embedded Files to download document. ')
                return render(request, 'embed_ownership_text.html', {'last_object': last_object, 'form': form, 'watermarkInfo': last_object.hash})

    else:
        form = Embed_Enforcement_Text_Form(
            initial={'user_info': current_user_info})
        form.fields['user_info']._queryset = current_user_info

    return render(request, 'embed_enforcement_text.html', {'form': form})


@login_required(login_url='login')
def embed_enforcement_image(request):
    # information regarding the current user
    current_user_info = request.user.user_info
    current_user_email = request.user.email

    if request.method == 'POST':
        form = Embed_Enforcement_Image_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            last_object = Embed_Enforcement_Image.objects.all().last()
            last_object_location = MEDIA_ROOT + f"{last_object.file}"
            embed_info_1 = "Owner: " + f"{last_object.owner}"
            embed_info_2 = "Timestamp: " + str(datetime.datetime.now())
            embed_info_3 = "Receiver: " + f"{last_object.receiver}"
            watermarkInfo = embed_info_1 + "-" + embed_info_3 + "_" + embed_info_2
            print(last_object_location, f"{last_object.file}")

            try:
                watermark_embed(last_object_location,
                                watermarkInfo, last_object_location)
                last_object.hash = get_hash(last_object_location)

                """write information to myAdmin Sql"""
                mydb, mycursor = open_db_conn()
                sql = "INSERT INTO digital_enforcement_tbl (user_contact,file,embedded_watermark,hash,owner,receiver) VALUES(%s,%s,%s,%s,%s,%s)"

                user_contact = str(current_user_email)
                file = str(last_object.file)
                embedded_watermark = watermarkInfo
                hash = last_object.hash
                owner = last_object.owner
                receiver = last_object.receiver

                val = (user_contact, file, embedded_watermark,
                       hash, owner, receiver)
                mycursor.execute(sql, val)
                mydb.commit()
                close_db_conn(mydb, mycursor)

                messages.success(request, 'File has been embedded  ' +
                                 current_user_info.name + '. Go to Embedded Files to download document. ')
                return render(request, 'embed_enforcement_image.html', {'last_object': last_object, 'form': form, 'watermarkInfo': watermarkInfo})
            except:

                last_object.hash = get_hash(last_object_location)

                """write information to myAdmin Sql"""
                mydb, mycursor = open_db_conn()
                sql = "INSERT INTO digital_enforcement_tbl (user_contact,file,embedded_watermark,hash,owner,receiver) VALUES(%s,%s,%s,%s,%s,%s)"

                user_contact = str(current_user_email)
                file = str(last_object.file)
                embedded_watermark = 'no_watermark_info'
                hash = last_object.hash
                owner = last_object.owner
                receiver = last_object.receiver

                val = (user_contact, file, embedded_watermark,
                       hash, owner, receiver)
                mycursor.execute(sql, val)
                mydb.commit()
                close_db_conn(mydb, mycursor)

                messages.success(request, 'File has been embedded  ' +
                                 current_user_info.name + '. Go to Embedded Files to download document. ')
                return render(request, 'embed_enforcement_image.html', {'last_object': last_object, 'form': form, 'watermarkInfo': watermarkInfo})
    else:
        form = Embed_Enforcement_Image_Form(
            initial={'user_info': current_user_info})
        form.fields['user_info']._queryset = current_user_info

    return render(request, 'embed_enforcement_image.html', {'form': form})


@login_required(login_url='login')
def embed_enforcement_sound(request):
    # information regarding the current user
    current_user_info = request.user.user_info
    current_user_email = request.user.email

    if request.method == 'POST':

        form = Embed_Enforcement_Sound_Form(request.POST, request.FILES,)
        if form.is_valid():
            form.save()

            try:

                # We dont do the normal embedding this side, we use the hash
                last_object = Embed_Enforcement_Sound.objects.all().last()
                last_object_location = MEDIA_ROOT + f"{last_object.file}"
                embed_sound(last_object_location, 'host1.wav')
                raw__file = f"{last_object.file}".split('/')[-1]
                file_name = "encoded" + raw__file

                # move file to relevant folder
                move_sound_dep(raw__file, file_name)
                embedded_sound_location = 'sound/' + 'encoded' + raw__file
                last_object.hash = get_hash(
                    MEDIA_ROOT + embedded_sound_location)

                """write information to myAdmin Sql"""
                mydb, mycursor = open_db_conn()
                sql = "INSERT INTO digital_enforcement_tbl (user_contact,file,embedded_watermark,hash,owner,receiver) VALUES(%s,%s,%s,%s,%s,%s)"

                user_contact = str(current_user_email)
                file = raw__file
                embedded_watermark = last_object.owner
                hash = last_object.hash
                owner = last_object.owner
                receiver = last_object.receiver

                val = (user_contact, file, embedded_watermark,
                       hash, owner, receiver)
                mycursor.execute(sql, val)
                mydb.commit()

                messages.success(request, 'File has been embedded  ' +
                                 current_user_info.name + '. Go to Embedded Files to download document. ')
                return render(request, 'embed_enforcement_sound.html', {'last_object': last_object, 'form': form})

            except:
                return HttpResponse("File failure to upload, please check your internet connection")

    else:
        # return HttpResponse("Something up with the form")
        form = Embed_Enforcement_Image_Form(
            initial={'user_info': current_user_info})
        form.fields['user_info']._queryset = current_user_info

        return render(request, 'embed_enforcement_sound.html', {'form': form})


def embedded_files(request):
    if request.user.is_authenticated:

        try:
            current_user_info = request.user.user_info
            current_user_id = request.user.user_info.id

            embed_ownership_image = Embed_Ownership_Image.objects.all()
            embed_enforcement_image = Embed_Enforcement_Image.objects.all()
            uploaded_files_list = list(
                chain(embed_ownership_image, embed_enforcement_image))

            uploaded_files = []

            for uploaded_file in uploaded_files_list:
                if uploaded_file.user_info_id == current_user_id:
                    try:
                        uploaded_file.info = watermark_extract(
                            MEDIA_ROOT + f"{uploaded_file.file}")
                    except:
                        uploaded_file.info = "no_watermark_info"
                    try:
                        uploaded_file.hash = get_hash(
                            MEDIA_ROOT + f"{uploaded_file.file}")
                    except:
                        uploaded_file.hash = 'hash error'

                    uploaded_files.append(uploaded_file)
            print("EndImage")
            """ PDF embedding """
            embed_ownership_text = Embed_Ownership_Text.objects.all()
            embed_enforcement_text = Embed_Enforcement_Text.objects.all()
            uploaded_texts_list = list(
                chain(embed_ownership_text, embed_enforcement_text))

            uploaded_texts = []

            for uploaded_file in uploaded_texts_list:
                if uploaded_file.user_info_id == current_user_id:
                    try:
                        uploaded_file.info = pdf_extract_watermark(
                            MEDIA_ROOT + f"{uploaded_file.file}")
                    except:
                        uploaded_file.info = "no_watermark_info"
                    try:
                        uploaded_file.hash = get_hash(
                            MEDIA_ROOT + f"{uploaded_file.file}")
                    except:
                        uploaded_file.hash = 'hash error'

                    uploaded_texts.append(uploaded_file)

            print("EndText")
            """ Sound embedding """

            embed_ownership_sound = Embed_Ownership_Sound.objects.all()
            embed_enforcement_sound = Embed_Enforcement_Sound.objects.all()
            uploaded_sounds_list = list(
                chain(embed_ownership_sound, embed_enforcement_sound))

            """Stored file for the sound is abit different so need to create the name"""
            uploaded_sounds = []

            for uploaded_file in uploaded_sounds_list:
                if uploaded_file.user_info_id == current_user_id:

                    embedded_sound_file = f"{uploaded_file.file}".split(
                        '/')[-1]
                    embedded_sound_location = 'sound/' + 'encoded' + embedded_sound_file
                    print(embedded_sound_location)

                    try:
                        uploaded_file.hash = get_hash(
                            MEDIA_ROOT + embedded_sound_location)
                    except:
                        uploaded_file.hash = "hash error"
                    print(uploaded_file.hash)

                    uploaded_sounds.append(uploaded_file)

                    print(uploaded_file.owner)
                    print(embedded_sound_location)

            return render(request, 'embedded_files.html', {'uploaded_files': uploaded_files,
                                                           'uploaded_texts': uploaded_texts,
                                                           'uploaded_sounds': uploaded_sounds})

        except:
            print(
                'WHAT THE ACTUAL FUCKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK')
            uploaded_files = []
            return render(request, 'embedded_files.html', {'uploaded_files': uploaded_files})
    else:
        messages.info(request, "Please login or create an account")
        return render(request, 'login.html')

def delete_file(request, hash_url):
    try:
        file_to_delete = Embed_Ownership_Image.objects.get(hash_url=hash_url)
    except:
        pass
    try:
        file_to_delete = Embed_Enforcement_Image.objects.get(hash_url=hash_url)
    except:
        pass
    try:
        file_to_delete = Embed_Ownership_Text.objects.get(hash_url=hash_url)
    except:
        pass
    try:
        file_to_delete = Embed_Enforcement_Text.objects.get(hash_url=hash_url)
    except:
        pass
    try:
        file_to_delete = Embed_Enforcement_Sound.objects.get(hash_url=hash_url)
    except:
        pass
    try:
        file_to_delete = Embed_Ownership_Sound.objects.get(hash_url=hash_url)
    except:
        pass

    if request.method == 'POST':

        file_to_delete.delete()
        return redirect('/embedded_files')

    return render(request, 'delete_file.html', {'file_to_delete': file_to_delete})


def extract_text_info(request):

    if request.method == 'POST':
        form = Extract_Embedded_Text_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            last_object = Extract_Embedded_Text.objects.all().last()
            last_object_location = MEDIA_ROOT + f"{last_object.file}"
            last_object.uploaded_filename = str(
                last_object.file).split('/')[-1]
            last_object.hash = get_hash(last_object_location)
            hash = (last_object.hash,)
            
            
            try:
                """if it passes it will be an embedded file, almost have a double security system"""
                watermarkInfo = pdf_extract_watermark(last_object_location)
                last_object.info = watermarkInfo

                """write information to myAdmin Sql"""
                mydb, mycursor = open_db_conn()

                sql_ownership = " SELECT * FROM digital_ownership_tbl WHERE hash = %s"
                mycursor.execute(sql_ownership, hash)
                queryresult = mycursor.fetchall()

                if queryresult == []:
                    sql_enforcement = " SELECT * FROM digital_enforcement_tbl WHERE hash = %s"
                    mycursor.execute(sql_enforcement, hash)
                    queryresult = mycursor.fetchall()
                print(1111111111111111111111111)
                close_db_conn(mydb, mycursor)
                last_object.occurence_number = len(queryresult)
                last_object.id = queryresult[0][0]
                last_object.Timestamp = str(queryresult[0][1])
                last_object.email = queryresult[0][2]
                last_object.filename = queryresult[0][3]
                last_object.embedded_watermark = queryresult[0][4]
                last_object.owner = queryresult[0][6]

                try:
                    last_object.receiver = queryresult[0][7]
                except:
                    pass
                print(1111111111111111111111111)
                messages.success(request, 'Information extracted for file ' +
                                 last_object.uploaded_filename + '. Verify owner below. ')
                return render(request, 'extract_text_info.html', {'last_object': last_object, 'form': form})

            except:
                """if it doesnt pass the hash of the file will be stored in the historic database and the person is the owner"""

                last_object.info = last_object.owner

                messages.error(request, 'File embedding was not found for ' +
                               f"{last_object.file}" + '. Go to Embedded Files to download document. ')
                return render(request, 'extract_text_info.html', {'last_object': last_object, 'form': form, 'watermarkInfo': last_object.hash})

    else:
        form = Extract_Embedded_Text_Form()

    return render(request, 'extract_text_info.html', {'form': form})


def extract_image_info(request):

    if request.method == 'POST':
        form = Extract_Embedded_Image_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            last_object = Extract_Embedded_Image.objects.all().last()
            last_object_location = MEDIA_ROOT + f"{last_object.file}"
            last_object.uploaded_filename = str(
                last_object.file).split('/')[-1]
            last_object.hash = get_hash(last_object_location)
            hash = (last_object.hash,)

            try:
                """if it passes it will be an embedded file, almost have a double security system"""
                watermarkInfo = watermark_extract(last_object_location)
                last_object.info = watermarkInfo

                """write information to myAdmin Sql"""
                mydb, mycursor = open_db_conn()

                sql_ownership = " SELECT * FROM digital_ownership_tbl WHERE hash = %s"
                mycursor.execute(sql_ownership, hash)
                queryresult = mycursor.fetchall()

                if queryresult == []:
                    sql_enforcement = " SELECT * FROM digital_enforcement_tbl WHERE hash = %s"
                    mycursor.execute(sql_enforcement, hash)
                    queryresult = mycursor.fetchall()

                close_db_conn(mydb, mycursor)
                last_object.occurence_number = len(queryresult)
                last_object.id = queryresult[0][0]
                last_object.Timestamp = str(queryresult[0][1])
                last_object.email = queryresult[0][2]
                last_object.filename = queryresult[0][3]
                last_object.embedded_watermark = queryresult[0][4]
                last_object.owner = queryresult[0][6]

                try:
                    last_object.receiver = queryresult[0][7]
                except:
                    pass

                messages.success(request, 'Information extracted for file ' +
                                 last_object.uploaded_filename + '. Verify owner below. ')

                return render(request, 'extract_image_info.html', {'last_object': last_object, 'form': form})

            except:
                """if it doesnt pass the hash of the file will be stored in the historic database and the person is the owner"""
                last_object.info = last_object.owner

                messages.error(request, 'File ' + last_object.uploaded_filename +
                               'hash was not found in the database')
                return render(request, 'extract_image_info.html', {'last_object': last_object, 'form': form})

    else:
        form = Extract_Embedded_Image_Form()

    return render(request, 'extract_image_info.html', {'form': form})


def extract_sound_info(request):

    if request.method == 'POST':
        form = Extract_Embedded_Sound_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            last_object = Extract_Embedded_Sound.objects.all().last()
            # last_object_location = Path.cwd()/"media"/f"{last_object.file}"
            last_object_location = MEDIA_ROOT + f"{last_object.file}"

            """for sound what needs to happen is that I search the database for the owner, directly from the
             the server one time in that way everything is kept sort"""

            """if it passes it will be an embedded file, almost have a double security system"""
            last_object.hash = get_hash(last_object_location)
            last_object.uploaded_filename = str(
                last_object.file).split('/')[-1]
            hash = (last_object.hash,)

            try:
                """write information to myAdmin Sql"""
                mydb, mycursor = open_db_conn()

                sql_ownership = " SELECT * FROM digital_ownership_tbl WHERE hash = %s"
                mycursor.execute(sql_ownership, hash)
                queryresult = mycursor.fetchall()

                if queryresult == []:
                    sql_enforcement = " SELECT * FROM digital_enforcement_tbl WHERE hash = %s"
                    mycursor.execute(sql_enforcement, hash)
                    queryresult = mycursor.fetchall()

                close_db_conn(mydb, mycursor)
                last_object.occurence_number = len(queryresult)
                last_object.id = queryresult[0][0]
                last_object.Timestamp = str(queryresult[0][1])
                last_object.email = queryresult[0][2]
                last_object.filename = queryresult[0][3]
                last_object.owner = queryresult[0][6]

                try:
                    last_object.receiver = queryresult[0][7]
                except:
                    pass

                messages.success(request, 'Information extracted for file ' +
                                 last_object.uploaded_filename + '. Verify owner below. ')

                return render(request, 'extract_sound_info.html', {'last_object': last_object, 'form': form})
            except:
                messages.error(request, 'File ' + last_object.uploaded_filename +
                               'hash was not found in the database')
                return render(request, 'extract_sound_info.html', {'form': form})
    else:
        #
        form = Extract_Embedded_Sound_Form()

    return render(request, 'extract_sound_info.html', {'form': form})
