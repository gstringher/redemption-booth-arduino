import asyncio
import time
from datetime import datetime

async def esegui_background(script, arg1='', arg2=''):
    now = datetime.now()
    prefisso = now.strftime("%Y-%m-%d__%H-%M-%S__")+f"{int(now.microsecond / 1000):03d}"
    with open("logs/"+prefisso+"__"+script+".txt", 'wb') as f:
        process = await asyncio.create_subprocess_exec(
            'python', script, arg1, arg2,
            stdout=f,
            stderr=f 
        )
        time.sleep(0.01) # aspettare amleno 10ms per evitare conflitti di log


def esegui(script, arg1='', arg2=''):
    print("esecuzione", script)
    asyncio.run(esegui_background(script, arg1, arg2))
