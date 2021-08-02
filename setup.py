from setuptools import setup, find_packages

with open('requirements.txt', 'r') as req_file:
    required_packages = req_file.readlines()

with open('requirements_dev.txt', 'r') as req_dev_file:
    required_dev_packages = req_dev_file.readlines()

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name="Codenotes",
    version="1.0a2",
    author="Gamaliel Garcia",
    author_email="egamagz.dev@outlook.com",
    description='A simple CLI where you can save and view all your created annotations',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EGAMAGZ/codenotes",
    license="MIT",
    keywords="cli cui tui curses command-line note task codenotes",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Topic :: Office/Business :: Scheduling',
        'Typing :: Typed'
    ],
    packages=find_packages(exclude=['tests',]),
    entry_points={
        'console_scripts':['codenotes = codenotes:main',]
    },
    install_requires=required_packages,
    extra_require={
        'dev': required_dev_packages
    },
    python_requires=">=3.9"
)
