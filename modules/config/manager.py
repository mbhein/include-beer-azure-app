#!/usr/bin/env python3

import os
import io
import sys
import configparser

from modules.utils.dicts import DotNotation as DotNotation
import modules.utils.yaml as yaml

class ConfigManager(object):
    """ Configuration Manager Class

    Reads all configuration files
    - default_defs.yml
    - ~/include-beer.cfg
    - ENV INCLUDE_BEER_CONFIG

    Set configuration values based on order of precedents (lowest to highest)
    - default_defs.yml
    - specified config file (~/beer/include-beer.cfg or ENV INCLUDE_BEER_CONFIG)
    - Environmental overrides

    """

    def __init__(self, cfg_file=None, defaults_file=None):
        self._default_def = {}
        self._base_config_def = {}
        self._option_type_def = {}
        self._config_file = ''
        self._config_file_def = {}
        self._env_config_def = {}
        self._ops_config = {}

        # Load in our default definition yaml file
        self._default_def = yaml.yaml_loader(defaults_file or ('%s/default_defs.yml' % os.path.dirname(__file__)))

        # Set our base configuration definition based on
        self._base_config_def = self._build_base_config(self._default_def)

        # Build our option type dictionary
        self._build_option_type_def()

        # Load a configuration file definition if defined
        # if env INCLUDE_BEER_CONFIG is set, always use that
        # elif try ~/include-beer.cfg
        # else use base config defaults
        _expanded_user_config = os.path.expanduser('~/include-beer.cfg')
        if os.getenv('INCLUDE_BEER_CONFIG', 0):
            _env_config_file = os.environ['INCLUDE_BEER_CONFIG']
            if os.path.exists(_env_config_file):
                self._config_file = _env_config_file
                self._use_config_file = True
        elif os.path.exists(_expanded_user_config):
            self._config_file = _expanded_user_config
            self._use_config_file = True
        else:
            self._use_config_file = False

        if self._use_config_file:
            self._config_file_def = self._ini_to_dict(self._config_file)
            # cast our config file definitions
            self._config_file_def = self._cast_dict_values(self._config_file_def)

        # Build dicts containing env vars set
        self._env_config_def = self._build_env_config(self._default_def)

        # add base config
        self._ops_config = self._base_config_def.copy()
        for _section in self._config_file_def:
            self._ops_config[_section].update(self._config_file_def[_section])
        for _section in self._env_config_def:
            self._ops_config[_section].update(self._env_config_def[_section])
       
        # set operating config sections as attributes of object
        # use dotdict to access dict items using dot notation
        for _k, _v in self._ops_config.items():
            setattr(self, _k, DotNotation(_v))

    def _build_base_config(self, d):
        """Returns dictionaries of sections based on ini value

        Keyword arguments:
        - d(dict): dictionary of default defintions

        [ section1: { key: default, key: default }, section2: { key: default, key: default }]

        """
        _section_dicts = {}
        # loop on each default definition
        for _key in list(d):
            for _s in d[_key]['ini']:
                _section = _s['section']
                _option = _s['key']
                _default = d[_key]['default']
                _type = d[_key]['type']
                _section_dict = {_option: self._cast_value(_default, _type)}
                if _section in _section_dicts:
                    _section_dicts[_section].update(_section_dict)
                else:
                    _section_dicts[_section] = _section_dict
        return _section_dicts

    def _cast_value(self, value, value_type):
        """Return value cast as value_type

        Keyword arguments:
        - value: value to be cast
        - value_type: type to cast
        """
        if value is not None:
            if value_type == 'string':
                cast_value = str(value)

            elif value_type == "int":
                cast_value = int(value)

            elif value_type == "boolean":
                if value in ['True','False']:
                    cast_value = eval(value)
                else:
                    cast_value = value

            else:
                cast_value = value

        return cast_value

    def _ini_to_dict(self, ini_file):
        """Return INI file as dictionary object

        Keyword arguments:
        - ini_file(str): INI file to read and parse
        """
        cp = configparser.ConfigParser()
        cp.read(ini_file)
        _dict = {section: dict(cp.items(section)) for section in cp.sections()}
        return _dict

    def _build_option_type_def(self):
        """Return a dictionary of each option and its associated type

        Keyword arguments
        """
        _option_dict = {}
        _d = self._default_def
        for _key in list(_d):
            for _s in _d[_key]['ini']:
                _option = _s['key']
                _type = _d[_key]['type']
                _option_dict.update({_option: _type})
        self._option_type_def = _option_dict

    def _cast_dict_values(self, d):
        """Return dictionary with properly casted values

        Keyword arguments:
        - d(dict): dictionary to cast values in
        """
        _temp = {}
        for _section, _options in d.items():
            for _option, _value in d[_section].items():
                _type = self._option_type_def[_option]
                _option_dict = {_option: self._cast_value(_value, _type)}
                if _section in _temp:
                    _temp[_section].update(_option_dict)
                else:
                    _temp[_section] = _option_dict
        return _temp

    def _build_env_config(self, d):
        """Return dictionary of set ENV variables

        Keyword arguments:
        - d(dict): dictionary of default defintions
        """
        _env_dicts = {}
        for _s in list(d):
            _env_vars = d[_s]['env']
            _key = d[_s]['ini'][0]['key']
            _section = d[_s]['ini'][0]['section']
            _type = d[_s]['type']
            for _env_var in _env_vars:
                if os.getenv(_env_var['name'], 0):
                    _value = os.environ[_env_var['name']]
                    _entry = ({_key: self._cast_value(_value, _type)})
                    if _section in _env_dicts:
                        _env_dicts[_section].update(_entry)
                    else:
                        _env_dicts[_section] = _entry
        return _env_dicts

