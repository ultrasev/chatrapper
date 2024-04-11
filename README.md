
<div align="center">
 <figure style="text-align: align;">
     <img src="https://s3.bmp.ovh/imgs/2024/03/15/2aa0a21860f0ded7.png" width=189pt>
 </figure>
<h2>ChatGPT API (W)rapper</h2>

<a href='https://follow-your-click.github.io/'><img src='https://img.shields.io/badge/Project-Page-Green'></a> ![visitors](https://visitor-badge.laobi.icu/badge?page_id=ultrasev.chatrapper&left_color=green&right_color=red)  [![GitHub](https://img.shields.io/github/stars/ultrasev/chatrapper?style=social)](https://github.com/ultrasev/chatrapper)
</div>

把网页版 ChatGPT 封装为一个 API，以便在代码中使用。

# 本地安装
```bash
pip3 install git+https://github.com/ultrasev/chatrapper.git
```

# 代码中直接使用
在代码中使用 `Rapper`:
```python
import os
from chatrapper import Rapper
rapper = Rapper()
rapper("鲁迅为什么打周树人？")
```

或者有异步需求的话，可以使用 `AsyncRapper`。这种情况下，最好有多个账号支持，单账号下，同一时间只支持一轮对话。

```python
import os
import asyncio
from chatrapper import AsyncRapper
rapper = AsyncRapper()
async def main():
    print(await rapper("鲁迅为什么打周树人？"))

asyncio.run(main())
```

Demo:

<figure style="text-align: left;">
    <img src="https://s3.bmp.ovh/imgs/2024/03/15/25ea45935e95e00e.gif" width=589pt>
</figure>

# Docker 部署
```bash
docker run --name chatrapper -p 9000:9000 ghcr.io/ultrasev/chatrapper
```

请求示例:
```bash
curl http://127.0.0.1:9000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer any_string_you_like" \
    -d '{
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": "鲁迅为什么打周树人"
                }
            ],
            "stream": true
    }'
```

# Notes
- 合理使用 API，调用频率不宜过高，树大易招风，避免触发风控。

# TODO
- [ ] 结合 access_token 支持 GPT-4（需要登录且开通 premium）。
