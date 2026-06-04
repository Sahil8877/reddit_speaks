import modules

def image_to_base64(image_path):
    # get_post()
    with open(f'{image_path}',"rb") as file:
        base64_data = modules.base64.b64encode(file.read()).decode("utf-8")
    return base64_data