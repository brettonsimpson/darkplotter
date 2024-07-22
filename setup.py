from setuptools import setup

setup(
    name='darkplotter',
    version='1.0.1',
    description='A plotting library for dark-themed visualizations',
    author='Test User',
    url='https://github.com/rathorevedant99/darkplotter',
    packages=['darkplotter'],
    install_requires=[
    "matplotlib",
    "numpy",
    "scipy",
    "plotly",
    "astropy"
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    )