# -*- coding: utf-8 -*-
# @Time        : 2020/7/19 10:17
# @Author      : Pan
# @Description :
import base64
import logging
from io import BytesIO
from PIL import Image, ImageTk


class ImageWrapper(object):

    def __init__(self):
        self._image = None
        self._file_path = None

    def load_from_bytes(self, data):
        self._image = Image.open(BytesIO(base64.b64decode(data)))
        return self

    def load_from_file(self, file_path):
        try:
            if file_path is not None and file_path != '':
                self._image = Image.open(file_path)
        except Exception as e:
            logging.getLogger(__name__).exception(e)
        return self

    def _get_new_scale_image(self, w, h=None):
        if self._image is None:
            return None
        s_w, s_h = self._image.size
        w = int(w)
        if h is None:
            h = int(s_h * (w / s_w))
        return self._image.resize((w, h), Image.ANTIALIAS)

    def resize(self, w, h=None):
        self._image = self._get_new_scale_image(w, h)
        return self

    def get_tk_image(self, scale_to_w, scale_to_h=None):
        if self._image is None:
            return None
        return ImageTk.PhotoImage(self._get_new_scale_image(scale_to_w, scale_to_h))

    def persistent(self, file_path):
        pass

    @property
    def file_path(self):
        return self._file_path

    def show(self):
        if self._image is None:
            return None
        self._image.show()


