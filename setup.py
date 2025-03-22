from setuptools import setup, find_packages
import os

BASE = os.path.dirname(__file__)

def get_package_data():
    """Function to collect all necessary package data files."""
    data_files = []

    # Include all data files in 'data_tts' directory (e.g., voices, dicts)
    for root, dirs, files in os.walk(f'{BASE}/pyahotts'):
        for file in files:
            data_files.append(os.path.relpath(os.path.join(root, file), 'pyahotts'))

    return data_files


setup(
    name='pyahotts',
    version='0.0.1',
    description='AhoTTS - python Text-to-Speech package',
    author='JarbasAI',
    author_email='jarbasai@mailfence.com',
    url='https://github.com/TigreGotico/pyAhoTTS',
    packages=find_packages(include=['pyahotts', 'pyahotts.*']),
    package_data={
        'pyahotts': get_package_data(),
    },
    install_requires=[
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
