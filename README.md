# Pipeline as mermaid

[![Coverage report](https://gitlab.com/Nov1kov/pipeline_to_mermaid/badges/master/coverage.svg)](https://nov1kov.gitlab.io/pipeline_to_mermaid/)
[![PyPI version](https://badge.fury.io/py/pipeline-mermaid.svg)](https://badge.fury.io/py/pipeline-mermaid)
[![Pipeline](https://gitlab.com/Nov1kov/pipeline_to_mermaid/badges/master/pipeline.svg)](https://gitlab.com/user/project/pipelines)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


Useful tool to show Gitlab pipeline as mermaid

## install

```commandline
pip install pipeline-mermaid
```

#### required environments

- `GITLAB_API_TOKEN` - gitlab api token

## Using

### in .gitlab-ci.yml

```yml
notify merge request:
  stage: deploy
  only:
    - merge_requests
  script:
    - python -m pipeline_mermaid.gitlab_helper show_current_pipeline
```
Show current pipeline in merge request notes. [Example merge request](https://gitlab.com/Nov1kov/pipeline_to_mermaid/-/merge_requests/4)

## Gitlab pipeline as mermaid

```mermaid
graph LR

classDef failed fill:white,stroke:#db3b21,color:black;
classDef success fill:white,stroke:#1aaa55,color:black;
classDef warning fill:white,stroke:#fc9403,color:black;
classDef skipped fill:white,stroke:#999,color:black;

730991283(android)
730991285(s3)
730991286(firebase)
730991287(slack)

730991283 --> 730991285
730991283 --> 730991286
730991285 --> 730991287
730991286 --> 730991287

class 730991283 success
class 730991285 warning
class 730991286 success
class 730991287 failed
```


```mermaid
gantt

dateFormat  YYYY-MM-DDTHH:mm:ss.SSSZ
axisFormat  %H:%M:%S

section test
unit tests : 730991283, 2020-09-12T12:26:05.370Z, 2020-09-12T12:26:41.665Z

section build
build : 730991284, 2020-09-12T12:26:42.182Z, 2020-09-12T12:27:38.126Z

section deploy
s3 : 730991285, 2020-09-12T12:27:43.757Z, 2020-09-12T12:28:35.406Z
firebase : 730991286, 2020-09-12T12:27:43.757Z, 2020-09-12T12:28:44.406Z
```

```mermaid
journey
section build
  android: -1: running
  ios: -1: running
section deploy
  slack-android: -1: created
  slack-ios: -1: created
```

# todo:

## README
- add .gitlab-ci.yml examples
- using as library

## gitlab 
- try depend on CI_JOB_TOKEN

### mermaid
- interactions https://mermaid-js.github.io/mermaid/diagrams-and-syntax-and-examples/gantt.html#interaction
- state

### documentaion
- https://pdoc3.github.io/pdoc/
- https://pydoc-markdown.readthedocs.io/en/latest/docs/api-documentation/processors/

### ci tools
- https://gitlab.version.fz-juelich.de/vis/jusense-cicd/-/wikis/discussion-on-howto-include-badges-in-gitlab-...
- https://github.com/jongracecox/anybadge
- https://docs.gitlab.com/ee/api/wikis.html
- gitlab release versions
- pylint (show errors in MR)