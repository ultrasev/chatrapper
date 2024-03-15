<figure style="text-align: left;">
    <img src="https://s3.bmp.ovh/imgs/2024/03/15/2aa0a21860f0ded7.png" width=189pt>
</figure>

# ChatGPT API (W)rapper
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

或者有异步需求的话，可以使用 `AsyncRapper`:
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
- 合理使用 API，调用频率不宜过高，避免触发风控。
