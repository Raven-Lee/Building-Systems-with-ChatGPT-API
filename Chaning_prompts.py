
import basic_api_usage as ai


delimiter = "####"
system_message = f"""
You will be provided with customer service queries. \
The customer service query will be delimited with \
{delimiter} characters.
Output a python list of objects, where each object has \
the following format:
    'category':<one of Computers and Laptios, \
    Smartphones and Accessories, \
    Televisions and Home Theater Systems, \
    Gaming Consoles and Accessories, \
    Audio Equipment, Cameras and Camcorders>,
OR
    'product':<a list of products that must \
    be found in the allowed products below>

where the categories and products must be found in \
the customer service query.

If a product is mentioned, it must be associated with \
the correct category in the allowed products list below.
If no products or categories are found, output an \
empty list.

Allowed products：

Computers and Laptops category:
TechPro Ultrabook
BlueWave Gaming Laptop
PowerLite Convertible
TechPro Desktop
BlueWave Chromebook

Smartphones and Accessories category:
SmartX ProPhone
MobiTech PowerCase
SmartX MiniPhone
MobiTech Wireless Charger
SmartX EarBuds

Televisions and Home Theater Systems category:
CineView 4K TV
SoundMax Home Theater
CineView 8K TV
SoundMax Soundbar
CineView OLED TV

Gaming Consoles and Accessories category:
GameSphere X
ProGamer Controller
GameSphere Y
ProGamer Racing Wheel
GameSphere VR Headset

Audio Equipment category:
AudioPhonic Noise-Canceling Headphones
WaveSound Bluetooth Speaker
AudioPhonic True Wireless Earbuds
WaveSound Soundbar
AudioPhonic Turntable

Cameras and Camcorders category:
FotoSnap DSLR Camera
ActionCam 4K
FotoSnap Mirrorless Camera
ZoomMaster Camcorder
FotoSnap Instant Camera

Only output the list of objects, with nothing else.
"""

user_message_1=f"""
tell me about the smartx pro phone and \
the fotosnap camera, the dslr one. \
also tell me about your rvs"""

user_message_2 = f"""
my router isn't working"""
messages = [
    {'role':'system',
     'content':system_message},
    {'role':'user',
     'content':f"{delimiter}{user_message_2}{delimiter}"},
]

response,token_dict = ai.get_completion_and_token_count(messages)
print(response)
print(token_dict)
