from PyKakao import Karlo
from token_1 import Kakao_Token

KAKAO_API_KEY = Kakao_Token
karlo = Karlo(service_key = KAKAO_API_KEY)

def generate_image(prompt):
    img_dict = karlo.text_to_image(prompt, 1)
    img_str = img_dict.get("images")[0].get('image')
    img = karlo.string_to_image(base64_string = img_str, mode = 'RGBA')
    img.save("./temp.png")
    return