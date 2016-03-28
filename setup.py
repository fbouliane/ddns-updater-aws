from distutils.core import setup
from setuptools import find_packages
setup(name='ddns_updater_aws',
      version='0.1',
      author='Felix Bouliane',
      license='MIT',
      py_modules=[],
      packages=find_packages(exclude=['contrib', 'docs', 'test']),
      url='https://github.com/fbouliane/ddns-updater-aws',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Internet :: Name Service (DNS)'
      ],
      keywords='DNS, Dynamic DNS, fixed ip, route53, AWS, Amazon Web Services',
      install_requires=[
        'dnspython>=1.12.0,<2.0',
        'ipaddress>=1.0.16,<2.0',
        'route53>=1.0,<2.0',
        'configparser>=3.3,<4.0'
      ],
      entry_points={
        'console_scripts': [
            'ddns-updater-aws = ddns_updater_aws.__main__:main',
        ]
      }
      )