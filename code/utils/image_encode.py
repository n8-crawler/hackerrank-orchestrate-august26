import base64


def img_to_base64(img_path:str):
    with open(img_path,'rb') as f:
        encode_img = base64.b64encode(f.read()).decode('utf-8')
    return encode_img