# -*- coding: utf-8 -*-

import os
import Image
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter

def thumbnail(file, size):
    x, y = [int(x) for x in size.split('x')]
    name, format = file.rsplit('.', 1)
    dirname = settings.EXPLORER_THUMBS_PATH + os.path.dirname( file )

    img_url = settings.EXPLORER_FILES_PATH + file
    miniature = name + '_' + size + '.' +  format
    thumb_url = settings.EXPLORER_THUMBS_PATH + miniature

    if not os.path.exists(thumb_url):
        # Create dir if it doesn't exist
        if not os.path.isdir(dirname):
            os.makedirs(dirname, mode=0755)
        # Create and save the thumb
        image = Image.open(img_url)
        image.thumbnail([x, y])
        image.save(thumb_url, image.format)

    return miniature

def get_lexer(path):
    try:
        lexer = get_lexer_for_filename(path)
    except ValueError:
        lexer = None

    return lexer

def get_extension(path):
    return os.path.splitext(path)[1][1:]

def list(request, path=''):
    base, dirs, files = iter(os.walk(settings.EXPLORER_FILES_PATH + path)).next()
    allowed_img = ['jpg', 'png', 'gif', 'jpeg']

    for i, file in enumerate(files):
        file_path = path + '/' + file
        files[i] = {'name': file, 'path': 'explorer/files' + file_path}

        if get_extension(file) in allowed_img:
            miniature = thumbnail(file_path, settings.EXPLORER_THUMBS_SIZE)
            files[i]['thumb_path'] = 'explorer/thumbs' + miniature
        elif get_lexer(file):
            files[i]['lexer_path'] = 'explorer/file@' + file_path

    return render_to_response(
        'explorer/list.html',
        {'files': files, 'dirs': dirs, 'dirname': path},
        RequestContext(request)
    )

def detail(request, path):
    file = open(settings.EXPLORER_FILES_PATH + path)
    content = file.read()
    formater = HtmlFormatter(cssclass='codehilite')

    parsed = highlight(content, get_lexer(path), formater)

    return render_to_response(
        'explorer/detail.html',
        {'content': parsed},
        RequestContext(request)
    )
