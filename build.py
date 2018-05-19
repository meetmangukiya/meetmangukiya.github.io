#!/usr/bin/env python

import os
import shutil

import jinja2
from jinja2 import Environment, FileSystemLoader
import yaml


CURRENT_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(CURRENT_DIR, 'templates')
DATA_DIR = os.path.join(CURRENT_DIR, 'data')
BUILD_DIR = os.path.join(CURRENT_DIR, 'public')
STATIC_DIR = os.path.join(CURRENT_DIR, 'static')

ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def render_template(template_name):
    try:
        with open(os.path.join(DATA_DIR, template_name.replace('.html', '.yaml'))) as f:
            data = yaml.load(f)
    except FileNotFoundError:
        data = {}
    finally:
        return ENV.get_template(template_name).render(**data)

def build(exclude=[]):
    try:
        os.mkdir(BUILD_DIR)
    except FileExistsError:
        pass

    templates = os.listdir(TEMPLATES_DIR)

    # render templates and write them to the build dir
    for template in filter(lambda x: x not in exclude, templates):
        print('creating page', template, '...')
        content = render_template(template)
        try:
            os.mkdir(os.path.join(BUILD_DIR, template.replace('.html', '')))
        except FileExistsError:
            pass

        with open(
            os.path.join(BUILD_DIR, template.replace('.html', ''), 'index.html'),
            'w',
        ) as f:
            f.write(content)

    # copy the static content to static dir
    print('copying static dir...')
    shutil.copytree(STATIC_DIR, os.path.join(BUILD_DIR, 'static'))

if __name__ == '__main__':
    build(exclude=['base.html'])
