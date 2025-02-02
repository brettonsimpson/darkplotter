from setuptools import setup

setup(
    name='darkplotter',
    version='1.0.1',
    description='Dark Plotter is a Python package for visualizing velocity as a function of radius for the Milky Way galaxy in an interactive way.',
    author='Test User',
    url='https://github.com/brettonsimpson/darkplotter',
    packages=['darkplotter'],
    package_data={'': ['MW_Vc.txt','MWay.dat']},
    include_package_data=True,
    install_requires=[
    "matplotlib",
    "numpy",
    "scipy",
    "plotly",
    "astropy",
    "setuptools",
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