
def render_template(template_path, file_path, arguments):
    from jinja2 import Environment, PackageLoader
    
    if not 'env' in dir(render_template):
        render_template.env = Environment(
                loader=PackageLoader('fondue', 'static/templates'),
                lstrip_blocks=True,
                trim_blocks=True
                )
    
    template = render_template.env.get_template(template_path)
    with open(file_path, 'w') as outfile:
        outfile.write(template.render(**arguments))
