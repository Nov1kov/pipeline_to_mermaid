from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='pipeline_mermaid',
    version='0.3',
    description='Useful tool to show Gitlab pipeline as mermaid',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Ivan Novikov',
    author_email='spellh1@gmail.com',
    keywords=['pipeline', 'mermaid', 'Gitlab'],
    url='https://github.com/Nov1kov/pipeline_to_mermaid',
    download_url='https://pypi.org/project/pipeline-mermaid/'
)

install_requires = [
    'python-gitlab',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)