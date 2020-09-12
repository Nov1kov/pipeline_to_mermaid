#### required environments

- `GITLAB_API_TOKEN` - gitlab api token


### Gitlab pipeline as graph LR

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

## todo:

### mermaid
- interactions https://mermaid-js.github.io/mermaid/diagrams-and-syntax-and-examples/gantt.html#interaction

### graph LR
- 'running'

### ci tools
- https://gitlab.version.fz-juelich.de/vis/jusense-cicd/-/wikis/discussion-on-howto-include-badges-in-gitlab-...
- https://github.com/jongracecox/anybadge
- https://docs.gitlab.com/ee/api/wikis.html