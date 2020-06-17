import base64
import binascii
import os

from django import template
from django.contrib.staticfiles.finders import find as find_static_file
from django.conf import settings
from django.utils.encoding import smart_str

from ieltsclasses.settings import MEDIA_URL, BASE_DIR

register = template.Library()


@register.simple_tag
def encode_dynmic_image(path, encoding='base64', file_type='image'):
    """
    a template tag that returns a encoded string representation of a staticfile
    Usage::
        {% encode_static path [encoding] %}
    Examples::
        <img src="{% encode_static 'path/to/img.png' %}">
    """
    print(path)
    print('------------------------')
    file_path = path
    # file_path = find_static_file(path)
    ext = file_path.split('.')[-1]

    file_str= image_to_data_url(file_path)
    # file_str = base64.urlsafe_b64encode(get_file_data(file_path))
    return "data:{0}/{1};{2},{3}".format(file_type, ext, encoding, file_str)



@register.simple_tag
def encode_dynmic_pdf(path, encoding='base64', file_type='application'):
    """
    a template tag that returns a encoded string representation of a staticfile
    Usage::
        {% encode_static path [encoding] %}
    Examples::
        <img src="{% encode_static 'path/to/img.png' %}">
    """
    print(path)
    print('------------------------')
    file_path = path
    print(file_path,"-path")
    # file_path = find_static_file(path)
    ext = file_path.split('.')[-1]
    file_str= image_to_data_url(file_path)
    # file_type=""
    print(file_str)
    # file_str = base64.urlsafe_b64encode(get_file_data(file_path))
    print("data:{0}/{1};{2},{3}".format(file_type, ext, encoding, file_str))
    return "data:{0}/{1};{2},{3}".format(file_type, ext, encoding, file_str)
    # return file_str

#
# @register.simple_tag
# def encode_dynmic_pdf(path_1):
#     print(path_1)
#
#     aaa =smart_str(path_1.replace(BASE_DIR,' '))
#     print(aaa)
#     print('---------------------------')
#     street = aaa
#     file_path =street.casefold()
#     # print(path)
#     # file_path = base64.urlsafe_b64encode(aaa)
#     # import urllib.parse
#     # file_path = urllib.parse.quote_plus(aaa)
#     print(file_path)
#     print('xxxxxxxxxxxxxxxxxxxxx')
#     #
#     # file_path = find_static_file(path)
#
#
#
#     # file_str = base64.urlsafe_b64encode(get_file_data(file_path))
#
#     return file_path
    # return file_str




@register.simple_tag
def encode_dynmic_video(path, encoding='base64', file_type='video'):
    """
    a template tag that returns a encoded string representation of a staticfile
    Usage::
        {% encode_static path [encoding] %}
    Examples::
        <img src="{% encode_static 'path/to/img.png' %}">
    """
    print(path)
    print('------------------------')
    file_path = path
    # file_path = find_static_file(path)
    ext = file_path.split('.')[-1]
    file_str= image_to_data_url(file_path)
    # file_str = base64.urlsafe_b64encode(get_file_data(file_path))
    return "data:{0}/{1};{2},{3}".format(file_type, ext, encoding, file_str)




@register.simple_tag
def video_encode_static(path, encoding='base64', file_type='video'):
    """
    a template tag that returns a encoded string representation of a staticfile
    Usage::
        {% encode_static path [encoding] %}
    Examples::
        <img src="{% encode_static 'path/to/img.png' %}">
    """
    print(path)
    print('------------------------')
    # file_path = path
    file_path = find_static_file(path)
    print(file_path)

    ext = file_path.split('.')[-1]
    print(ext)
    file_str= image_to_data_url(file_path)
    # file_str = base64.urlsafe_b64encode(get_file_data(file_path))
    return "data:{0}/{1};{2},{3}".format(file_type, ext, encoding, file_str)


@register.simple_tag
def image_encode_static(path, encoding='base64', file_type='image'):
    """
    a template tag that returns a encoded string representation of a staticfile
    Usage::
        {% encode_static path [encoding] %}
    Examples::
        <img src="{% encode_static 'path/to/img.png' %}">
    """
    print(path)
    print('------------------------')
    # file_path = path
    file_path = find_static_file(path)
    ext = file_path.split('.')[-1]
    file_str= image_to_data_url(file_path)
    # file_str = base64.urlsafe_b64encode(get_file_data(file_path))
    return "data:{0}/{1};{2},{3}".format(file_type, ext, encoding, file_str)




@register.simple_tag
def raw_static(path):
    """
    a template tag that returns a raw staticfile
    Usage::
        {% raw_static path %}
    Examples::
        <style>{% raw_static path/to/style.css %}</style>
    """
    if path.startswith(settings.STATIC_URL):
        # remove static_url if its included in the path
        path = path.replace(settings.STATIC_URL, '')
    file_path = find_static_file(path)
    return get_file_data(file_path)








def get_file_data(file_path):
    with open(file_path, 'rb') as f:
        data =f.read()
        print(type(data))
        f.close()
        return data


import base64

def image_to_data_url(filename):
    ext = filename.split('.')[-1]
    # prefix = f'data:image/{ext};base64,'
    with open(filename, 'rb') as f:
        img = f.read()
    return  base64.b64encode(img).decode('utf-8')

#
'''
data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUA
AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO
    9TXL0Y4OHwAAAABJRU5ErkJggg==


'''

# @register.simple_tag
# def image_as_base64(image_file, format='jpeg'):
#     """
#     :param `image_file` for the complete path of image.
#     :param `format` is format for image, eg: `png` or `jpg`.
#     """
#     if not os.path.isfile(image_file):
#         return None
#
#     encoded_string = ''
#     with open(image_file, 'rb') as img_f:
#         encoded_string = base64.b64encode(img_f.read())
#     return 'data:image/%s;base64,%s' % (format, encoded_string)
#
