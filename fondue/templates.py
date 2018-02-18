import os.path
from jinja2 import Environment, PackageLoader


class TemplateRepo():
    def __init__(self, prefix):
        self.template_env = Environment(
            loader=PackageLoader('fondue', 'static/templates/' + prefix),
            lstrip_blocks=True,
            trim_blocks=True
        )

    def get_templates(self, key):
        def filterfunc(x): return x.startswith(key)

        return self.template_env.list_templates(filter_func=filterfunc)

    def render_template(self, template_name, file_path, arguments):
        template = self.template_env.get_template(template_name)
        with open(file_path, 'w') as outfile:
            outfile.write(template.render(**arguments))
