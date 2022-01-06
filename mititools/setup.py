import setuptools

requirements = [
    'pandas==1.3.4',
    'PyYAML==6.0',
    'Jinja2==3.0.1',
    'frictionless==4.23.0',
]

setuptools.setup(
    name='mititools',
    version='0.2',
    description='Tools for working with MITI (Minimum Information about Tissue Imaging) data.',
    packages=[
        'mititools',
        'mititools.serializers',
        'mititools.converters',
    ],
    package_data={
        'mititools': [
            'fd_schema.json.jinja',
        ]},
    python_requires='>=3.7',
    scripts=[
        'scripts/mititools',
    ],
    install_requires=requirements,
)
