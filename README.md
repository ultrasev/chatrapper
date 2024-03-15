<figure style="text-align: left;">
    <img src="data/logo.png" width=129pt>
</figure>

# ChatGPT API wrapper

将 ChatGPT 包装为一个简单的 API，以便在代码、脚本中使用。

# Installation
```bash
pip3 install git+https://github.com/ultrasev/chatrapper.git
```

# Usage
环境变量中设置 `TOKEN`，然后调用 `chat` 函数即可。
```bash
export TOKEN="eyJhbGci..."
```

在 Python 中使用 `Rapper`:
```python
import os
from chatgpt_wrapper import GPTWrapper
token = os.environ.get("TOKEN")
rapper = GPTWrapper(
    access_token=token
    model="text-davinci-002-render-sha"
)
rapper("鲁迅为什么打周树人？")
```

或者有异步需求的话，可以使用 `AsyncGPTWrapper`:
```python
import os
import asyncio
from chatgpt_wrapper import AsyncGPTWrapper

token = os.environ.get("TOKEN")
rapper = AsyncGPTWrapper(
    access_token=token
    model="text-davinci-002-render-sha"
)
async def main():
    print(await rapper("鲁迅为什么打周树人？"))

asyncio.run(main())
```

# 注意事项
- 一定要保护好自己的 token，不要泄露给他人。
- 合理使用 API，调用频率不宜过高，避免触发风控。
