"""Script to make package for setup."""
import re
from subprocess import check_output

from setuptools import setup


def check_lfs():
    """Check Git LFS available."""
    try:
        out = check_output(['git', 'lfs', 'env'])

        lfs_test = re.compile(
            r'^git config filter\.lfs\.(\S+)\s+=\s+\"([^\"]+)\"',
            re.MULTILINE | re.IGNORECASE
        )

        lfs_setup = {
            k: len(v.strip()) > 0
            for k, v in lfs_test.findall(out.decode())
        }

        # check LFS has correct setup (it has no setup if not installed)
        if not (lfs_setup.get('clean', False) and
                lfs_setup.get('smudge', False) and
                lfs_setup.get('process', False)):
            raise EnvironmentError(
                'Git LFS is not configured. Run "git lfs install".'
            )
    except EnvironmentError:
        raise
    except Exception:
        raise EnvironmentError(
            'Git LFS is required to install this package. '
            'Please install Git LFS (https://git-lfs.github.com/) '
            'and restart package installation.'
        )


setup(
    name='print-server',
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    description='Print server',
    author='alexstaf',
    author_email='alexstaf1@gmail.com',
    packages=['print_server'],
    entry_points={
        'console_scripts': [
            'print-server=print_server.serve:main'
        ]
    },
    python_requires='>=3.8',
    install_requires=[
        'Flask',
        'numpy',
        'opencv-python',
        'Pillow',
        'pywin32'
    ],
    include_package_data=True,
    zip_safe=False
)
