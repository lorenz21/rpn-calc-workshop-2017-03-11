from setuptools import setup

setup(
    name='rpn-calc-engine',
    version='0.0.1',
    author='jeffrey k eliasen',
    author_email='jeff+rpn-calc-engine@jke.net',
    description = 'an RPN calculator engine for use in workshops',
    license='MIT',
    keywords='calculator',
    url='',
    packages=['rpncalculator'],
    long_description=open('README.md').read(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    install_requires=[
    ],
)
