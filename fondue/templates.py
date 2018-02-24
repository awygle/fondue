import os.path
import distutils.dir_util

import jinja2


class Template():
    def __init__(self, repo, jinja_template):
        self._template = jinja_template
        self.parent = None
        self.repo = repo

    def set_parent(self, template):
        self.parent = template

    def render(self, **kwargs):
        return self._template.render(kwargs)


class TemplateRepo():
    def __init__(self, prefix):
        self._env = jinja2.Environment(
            loader=jinja2.PackageLoader('fondue', 'static/templates/'+prefix),
            lstrip_blocks=True,
            trim_blocks=True
        )
        self._prefix = prefix

    def get_templates(self, key):
        def filterfunc(x):
            return x.startswith(os.path.normpath(key)+'/') and x.endswith('j2')

        template_names = self._env.list_templates(filter_func=filterfunc)
        templates = {}
        for name in template_names:
            base_name = name.partition('/')[2]  # remove prefix
            templates[base_name] = Template(self, self._env.get_template(name))
        return templates

    def render_template(self, template, file_path, arguments, base=None):
        if base:
            arguments['base'] = base._template
        distutils.dir_util.mkpath(os.path.dirname(file_path))
        with open(file_path, 'w') as outfile:
            outfile.write(template.render(**arguments))
