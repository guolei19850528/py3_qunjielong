# py3_qunjielong
The Python3 Qunjielong Library Developed By Guolei

# Official Documentation

## [Home](https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/)


# Installation
```shell
pip install py3_qunjielong
```

# Example
## Qunjielong
```python
import os

import diskcache

from py3_qunjielong.qunjnielong import Qunjielong, RequestUrl

cache = diskcache.Cache(directory=os.path.join(os.getcwd(), "runtime", "diskcache", "default"))
qunjielong = Qunjielong(
    secret="<secret>",
    cache=cache
)

print(
    qunjielong.token_with_cache().request_with_token(
        method="GET",
        url=f"{RequestUrl.OPEN_API_GHOME_GETGHOMEINFO}",
    )
)
```