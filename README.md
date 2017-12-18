# PyRPC

A library for connecting Discord Rich Presence to Python.

> I actually don't know what I'm doing and this project isn't finished. pls help

## How to Use

```py
# import library
import pyrpc
import asyncio

# initialize client
c = pyrpc.RpcClient("app id here", "app secret here")

# you can get your application id
# and secret from your applications
# page --
# https://discordapp.com/developers/applications/me

# authenticate w/ rpc server (results in error)
async def my_coroutine():
    c.authenticate()

    # change rich presence (not implemented)
    c.update_presence(title="Overwatch", state="Competitive | 1 - 3", details="3:05 left", large_img=pyrpc.Image(key="numbaniMap", text="on Numbani", large=True), small_img=pyrpc.Image(key="mercyHero", text="Playing as Mercy", large=False))

# run it
asyncio.get_event_loop().run_until_complete(my_coroutine())
```
