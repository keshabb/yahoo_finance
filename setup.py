from setuptools import setup, find_packages
setup(
    name = 'yahoo_finance',
    description = 'Python script to get stock info from yahoo using web scraping',
    version = '1.0',
    py_modules = ['yahoo_finance'],
    author = 'Keshab Budhathoky',
    author_email = 'kb4it.professional@hotmail.com',
    license = 'MIT',
    packages = find_packages(),
    install_requires = [
        'bs4',
        'click',
        'requests',
        'gdata',
        'pandas',
        'jinja2',
        'Yahoo-ticker-downloader',
        ],
    entry_points = {
        'console_scripts': [
            'stock_info_yahoo=yahoo_finance:get_info_yahoo',
        ]
    },
)
