from jinja2 import Template

template = input("Enter template: ")
result = Template(template).render()
print(result)
