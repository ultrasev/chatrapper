
<div align="center">
 <figure style="text-align: align;">
     <img src="https://s3.bmp.ovh/imgs/2024/03/15/2aa0a21860f0ded7.png" width=189pt>
 </figure>
<h2>ChatGPT API (W)rapper</h2>

<a href='https://follow-your-click.github.io/'><img src='https://img.shields.io/badge/Project-Page-Green'></a> ![visitors](https://visitor-badge.laobi.icu/badge?page_id=ultrasev.chatrapper&left_color=green&right_color=red)  [![GitHub](https://img.shields.io/github/stars/ultrasev/chatrapper?style=social)](https://github.com/ultrasev/chatrapper)
</div>

免登录版 ChatGPT web API 的 Python 封装，支持本地安装和 Docker 部署。兼容 OpenAI 的 API 规范，支持 ChatGPT-3.5 模型。

# 本地安装
```bash
pip3 install git+https://github.com/ultrasev/chatrapper.git
```

# 代码中直接使用
在代码中使用同步版 `Rapper`:
```python
from chatrapper import Rapper
rapper = Rapper(stream=False)
print(rapper("鲁迅为什么打周树人？"))
```

Response:
```text
鲁迅和周树人之间的矛盾源于他们在文学理念、文学风格以及政治立场上的分歧。周树人是新文化运动的重要人物之一，与鲁迅一样，他也是一位重要的文学家和思想家。然而，两人在一些关键问题上存在分歧。
...
```

也可以通过列表传入多轮对话的历史记录。

```python
from chatrapper import Rapper
rapper = Rapper(stream=False)
messages = [
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
]
print(rapper(messages))
```

异步需求场景下，可以使用 `AsyncRapper`。

```python
import asyncio
from chatrapper import AsyncRapper

async def main():
    return await AsyncRapper(stream=True)("what is the purpose of life?")

asyncio.run(main())
```

Demo:

<figure style="text-align: left;">
    <img src="https://s3.bmp.ovh/imgs/2024/03/15/25ea45935e95e00e.gif" width=589pt>
</figure>

# Docker 部署
```bash
docker run --name rapper -p 9000:9000 ghcr.io/ultrasev/chatrapper
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
- 部署服务不挑 IP，但建议优先使用带美区 IP 的服务器。
- 合理使用 API，调用频率不宜过高。树大易招风，避免触发风控。

# TODO
- [ ] 结合 access_token 支持 GPT-4（需要登录且开通 premium）。
- [ ] 支持 OpenAI API chat 接口。