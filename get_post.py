import modules
import get_topic


def get_post(IMG_PATH):
    driver = None
    try:
        subreddit = get_topic.get_topic().strip()
        
        URL = f"https://www.reddit.com/{subreddit}/hot/?t=day"
        print("🔗 Exploring link : ",URL)
        options = modules.webdriver.ChromeOptions()

        driver = modules.webdriver.Chrome(options=options)
        driver.get(URL)
        By = modules.By
        modules.WebDriverWait(driver=driver,timeout=5).until(modules.EC.presence_of_element_located((By.CSS_SELECTOR,"shreddit-post")))
        post = driver.find_element(By.CSS_SELECTOR,"shreddit-post")
        title = post.find_element(By.CSS_SELECTOR,"a[id^='post-title-']")
        image = post.find_element(By.CSS_SELECTOR,"img[id^='post-image']")
        img_data = modules.requests.get(image.get_attribute('src')).content
        now = modules.datetime.now()

        with open(f'{IMG_PATH}/{now.strftime("%A_%B_%d_%Y_%I:%M_%p")}.png','wb') as f:
            f.write(img_data)

        print("📝 Post Title : ",title.text)
        return True
    except Exception as e:
        print("Exception occured retrying now..")
        return False
    finally:
        driver.quit()

# if not get_post():
#     retry(get_post,"Image Attempt :")
