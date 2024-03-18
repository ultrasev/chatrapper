
<div align="center">
 <figure style="text-align: align;">
     <img src="https://s3.bmp.ovh/imgs/2024/03/15/2aa0a21860f0ded7.png" width=189pt>
 </figure>
<h2>ChatGPT API (W)rapper</h2>

<a href='https://follow-your-click.github.io/'><img src='https://img.shields.io/badge/Project-Page-Green'></a> ![visitors](https://visitor-badge.laobi.icu/badge?page_id=ultrasev.chatrapper&left_color=green&right_color=red)  [![GitHub](https://img.shields.io/github/stars/ultrasev/chatrapper?style=social)](https://github.com/ultrasev/chatrapper)
</div>

把网页版 ChatGPT 包装为一个简单的 API，以便在代码、脚本中使用。

# Installation
```bash
pip3 install git+https://github.com/ultrasev/chatrapper.git
```

# Usage
环境变量中设置 `TOKEN`，然后调用 `chat` 函数即可。
```bash
export TOKEN="eyJhbGci..."
```

在代码中使用 `Rapper`:
```python
import os
from chatrapper import Rapper
token = os.environ.get("TOKEN")
rapper = Rapper(
    access_token=token
    model="text-davinci-002-render-sha"
)
rapper("鲁迅为什么打周树人？")
```

或者有异步需求的话，可以使用 `AsyncRapper`。这种情况下，最好有多个账号支持，单账号下，同一时间只支持一轮对话。

```python
import os
import asyncio
from chatrapper import AsyncRapper

token = os.environ.get("TOKEN")
rapper = AsyncRapper(
    access_token=token
    model="text-davinci-002-render-sha"
)
async def main():
    print(await rapper("鲁迅为什么打周树人？"))

asyncio.run(main())
```

Demo:

<figure style="text-align: left;">
    <img src="https://s3.bmp.ovh/imgs/2024/03/15/25ea45935e95e00e.gif" width=589pt>
</figure>


# Notes
- 一定要保护好自己的 token，不要泄露给他人。
- 合理使用 API，调用频率不宜过高，树大易招风，避免触发风控。
