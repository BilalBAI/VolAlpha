from setuptools import setup, find_packages
setup(
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    entry_points={'console_scripts': ['app = app.run:run']}
)
