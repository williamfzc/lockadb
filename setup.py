from setuptools import setup, find_packages


setup(
    name='lockadb',
    version='0.1.0',
    description='lockable android debug bridge, for managing devices precisely and safely',
    author='williamfzc',
    author_email='fengzc@vip.qq.com',
    url='https://github.com/williamfzc/lockadb',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'whenconnect',
        'loguru',
        'requests',
    ],
    entry_points={
        "console_scripts": [
            "ladb = lockadb.client:main",
        ],
    },
)
