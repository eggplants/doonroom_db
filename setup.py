from setuptools import find_packages, setup  # type: ignore

setup(
    name="doonroom_db",
    version="0.9",
    description="同人音声の部屋(http://doonroom.blog.jp/) DB",
    description_content_type="",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/eggplants/doonroom_db",
    author="eggplants",
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        "console_scripts": [
            "ddb=main:main"
        ]
    }
)
