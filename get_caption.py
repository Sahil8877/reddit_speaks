import modules 
import image_to_base64 as b64_func

def get_caption(total_imgs,imgs_list,IMG_PATH):
    caption_list = []
    for i in range(total_imgs):
        caption = modules.ollama.generate(
            model='llava:13b',
            prompt='You need to describe this image in no more than 5 words.',
            images=[b64_func.image_to_base64(f"{IMG_PATH}/{imgs_list[i]}")]
        )
        caption_list.append(caption['response'].strip())       
    return caption_list

# print(get_caption())