from ua import *
import base64
from PIL import Image
from io import BytesIO
import requests

cats = [
    'https://miniblogcore.azurewebsites.net/Posts/files/cat_637121647509154829.jpg',
    'https://wallpaperaccess.com/full/374195.jpg',
    'https://api.time.com/wp-content/uploads/2015/02/cats.jpg?quality=85&w=1024&h=512&crop=1',
    'https://images.ctfassets.net/cnu0m8re1exe/7sLmeD1tcL4UoIm0BjNaLh/22a9f42a4315361db96470f50b178e86/Dog-and-Cat.jpg?w=650&h=433&fit=fill',
]

for cat in cats:
    variant = UaVariant()
    response = requests.get(cat).content
    base64_cat = base64.b64encode(response)
    variant.data = UaByteString(base64_cat)

    client = UaClient()
    client.connect()
    res = client.call(UA_NS0ID.OBJECTSFOLDER, UaNodeId(1, "cat detector"), variant)

    image = Image.open(BytesIO(base64.b64decode(UaByteString(res.output[0].data).value)))
    image.show()
