## Pipeline as mermaid

[![Coverage report](https://gitlab.com/Nov1kov/pipeline_to_mermaid/badges/master/coverage.svg)](https://nov1kov.gitlab.io/pipeline_to_mermaid/)
[![PyPI version](https://badge.fury.io/py/pipeline-mermaid.svg)](https://badge.fury.io/py/pipeline-mermaid)
[![Pipeline](https://gitlab.com/Nov1kov/pipeline_to_mermaid/badges/master/pipeline.svg)](https://gitlab.com/user/project/pipelines)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


Useful tool to show Gitlab pipeline as mermaid

#### required environments

- `GITLAB_API_TOKEN` - gitlab api token


## Gitlab pipeline as graph LR

```mermaid
graph LR

classDef failed fill:white,stroke:#db3b21,color:black;
classDef success fill:white,stroke:#1aaa55,color:black;
classDef classWarn fill:white,stroke:#fc9403,color:black
classDef canceled fill:white,stroke:#999

730991283(unit tests)
730991284(build)
730991285(s3)
730991286(firebase)

730991283 --> 730991284
730991284 --> 730991285
730991284 --> 730991286

class 730991283 success
class 730991284 success
class 730991285 success
class 730991286 success
```

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
graph LR

classDef failed fill:white,stroke:#db3b21,color:black;
classDef success fill:white,stroke:#1aaa55,color:black;
classDef warning fill:white,stroke:#fc9403,color:black;
classDef skipped fill:white,stroke:#999,color:black;

730991283(android)
730991284(ios)
730991285(s3)
730991286(firebase)
730991287(firebase)

730991283 --> 730991285
730991284 --> 730991285
730991283 --> 730991286
730991284 --> 730991286
730991283 --> 730991287
730991284 --> 730991287

class 730991283 failed
class 730991284 success
class 730991285 skipped
class 730991286 skipped
class 730991287 skipped
```

```mermaid
graph LR

classDef failed fill:white,stroke:#db3b21,color:black;
classDef success fill:white,stroke:#1aaa55,color:black;
classDef warning fill:white,stroke:#fc9403,color:black;
classDef skipped fill:white,stroke:#999,color:black;
classDef running fill:white,stroke:#1f75cb,color:black;

730991283(android)
730991284(ios)
730991285(slack:android)
730991286(slack:ios)

730991283 --> 730991285
730991284 --> 730991285
730991283 --> 730991286
730991284 --> 730991286

class 730991283 running
class 730991284 running
class 730991285 skipped
class 730991286 skipped
```

## Gitlab pipeline as gantt

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
gantt

dateFormat  YYYY-MM-DDTHH:mm:ss.SSSZ
axisFormat  %H:%M:%S

section build
android : 730991283, 2020-09-12T12:26:05.370Z, 2020-09-12T12:26:41.665Z

section deploy
s3 :crit, active, 730991285, 2020-09-12T12:26:42.182Z, 2020-09-12T12:27:38.126Z
firebase : 730991286, 2020-09-12T12:26:42.346Z, 2020-09-12T12:27:41.991Z

section notify
slack :crit, 730991287, 2020-09-12T12:27:43.757Z, 2020-09-12T12:28:35.406Z
```

```mermaid
gantt

dateFormat  YYYY-MM-DDTHH:mm:ss.SSSZ
axisFormat  %H:%M:%S

section build
android :crit, 730991283, 2020-09-12T12:26:05.370Z, 2020-09-12T12:26:41.665Z
ios : 730991284, 2020-09-12T12:26:05.370Z, 2020-09-12T12:26:47.665Z

section deploy
s3 :done, 730991285, after 730991284, 15s
firebase :done, 730991286, after 730991284, 15s
firebase :done, 730991287, after 730991284, 15s
```

```mermaid
gantt

dateFormat  YYYY-MM-DDTHH:mm:ss.SSSZ
axisFormat  %H:%M:%S

section build
android :active, 730991283, 2020-09-12T21:45:02.379Z, 15s
ios :active, 730991284, 2020-09-12T21:45:02.379Z, 15s

section deploy
slack-android :done, 730991285, after 730991283, 15s
slack-ios :done, 730991286, after 730991283, 15s
```

## Gitlab pipeline as journey

```mermaid
journey
section build
  android: 5
section deploy
  s3: 3
  firebase: 5
section notify
  slack: 1
```

```mermaid
journey
section test
  unit tests: 5
section build
  build: 5
section deploy
  s3: 5
  firebase: 5
```

```mermaid
journey
section build
  android: 1
  ios: 5
section deploy
  s3: -1: skipped
  firebase: -1: skipped
  firebase: -1: skipped
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

## todo:

## gitlab 
- try depend on CI_JOB_TOKEN

### mermaid
- interactions https://mermaid-js.github.io/mermaid/diagrams-and-syntax-and-examples/gantt.html#interaction
- state
- journey

### documentaion
- https://pdoc3.github.io/pdoc/
- https://pydoc-markdown.readthedocs.io/en/latest/docs/api-documentation/processors/

### ci tools
- https://gitlab.version.fz-juelich.de/vis/jusense-cicd/-/wikis/discussion-on-howto-include-badges-in-gitlab-...
- https://github.com/jongracecox/anybadge
- https://docs.gitlab.com/ee/api/wikis.html
- gitlab release versions
- pylint (show errors in MR)