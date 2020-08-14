# -*- coding: utf-8 -*-
# @Time        : 2020/7/9 20:08
# @Author      : Pan
# @Description : 
import abc


class CommandMetadata(object):
    def __init__(self, desc, method_name, param_metadata):
        self._desc = desc
        self._method_name = method_name
        self._param_metadata = param_metadata

    @property
    def desc(self):
        return self._desc

    @property
    def method_name(self):
        return self._method_name

    def new_command_model(self):
        param_models = []
        for pmd in self._param_metadata:
            param_models.append(pmd.new_param_model())
        return CommandModel(self, param_models)


class CommandModel(object):
    def __init__(self, metadata, param_models):
        self.metadata = metadata
        self._param_models = param_models

    @property
    def param_models(self):
        return self._param_models

    def run(self, commander):
        args = []
        for p in self._param_models:
            args.append(p.value)
        getattr(commander, self.metadata.method_name)(*args)


class ParamMetadata(object):
    def __init__(self, desc, param_name, view_clazz, default_value=None):
        self._desc = desc
        self._param_name = param_name
        self._view_clazz = view_clazz
        self._default_value = default_value

    @property
    def desc(self):
        return self._desc

    @property
    def param_name(self):
        return self._param_name

    @property
    def view_clazz(self):
        return self._view_clazz

    def new_param_model(self):
        pm = ParamModel(self)
        if self._default_value is not None:
            pm.value = self._default_value
        return pm


class ParamModel(object):
    def __init__(self, metadata, value=None):
        self.metadata = metadata
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def get_view(self, view_parent):
        view = self.metadata.view_clazz(view_parent, self)
        view.init_ui(self.metadata.desc, self._value)
        return view




