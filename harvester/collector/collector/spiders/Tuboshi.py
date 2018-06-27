# coding: utf-8
import time
from PIL import Image
from io import BytesIO
from selenium import webdriver


class DocTuSelSpider(object):
    name = 'DocTuSel'
    home_url = 'https://m.2boss.cn/?isappinstalled=1#/city_detail?cityId=604&cityLevel=1'

    driver = None
    faq_list = []
    count = 0

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    }
    questions = []
    answers = []

    def scroll_down(self):
        self.driver.implicitly_wait(2)
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # time.sleep(1)

    def start(self):

        # option = webdriver.FirefoxOptions()
        # option.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1')

        # profile = webdriver.FirefoxProfile()
        # profile.set_preference("general.useragent.override", self.headers['User-Agent'])

        WIDTH = 350
        HEIGHT = 812
        PIXEL_RATIO = 3.0

        mobileEmulation = {"deviceMetrics": {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO},
                           "userAgent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        options = webdriver.ChromeOptions()
        options.add_experimental_option('mobileEmulation', mobileEmulation)
        options.add_argument('--headless')

        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.set_window_size(350, 812)
        print('create driver')
        self.driver.get(self.home_url)
        try:
            time.sleep(3)
            label_length = self.driver.execute_script("return document.getElementsByClassName('cityBaseHead').length;")
            del_last_label = "return document.getElementsByClassName('cityBaseHead')[{last}].remove();".format(last=str(label_length-1))
            self.driver.execute_script(del_last_label)
            self.driver.execute_script("return document.getElementsByClassName('topBox')[0].remove();")
            self.driver.execute_script("return document.getElementsByClassName('download_app')[0].remove();")

            device_pixel_ratio = self.driver.execute_script('return window.devicePixelRatio')

            total_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
            viewport_height = self.driver.execute_script('return window.innerHeight')
            total_width = self.driver.execute_script('return document.body.offsetWidth')
            viewport_width = self.driver.execute_script("return document.body.clientWidth")

            assert (viewport_width == total_width)

            # scroll the page, take screenshots and save screenshots to slices
            offset = 0  # height
            slices = {}
            while offset < total_height:
                if offset + viewport_height > total_height:
                    offset = total_height - viewport_height

                self.driver.execute_script('window.scrollTo({0}, {1})'.format(0, offset))
                time.sleep(0.3)

                img = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
                slices[offset] = img

                offset = offset + viewport_height

            # combine image slices
            stitched_image = Image.new('RGB', (total_width * device_pixel_ratio, total_height * device_pixel_ratio))
            for offset, image in slices.items():
                stitched_image.paste(image, (0, offset * device_pixel_ratio))
            height = stitched_image.height
            width = stitched_image.width
            scrollbar_width = 20
            stitched_image = stitched_image.crop((scrollbar_width, 0, width-scrollbar_width, height))  # 切掉滚动轮
            stitched_image.save('./screen.png')

            time.sleep(2)

        finally:
            self.driver.quit()


if __name__ == '__main__':
    dt = DocTuSelSpider()
    dt.start()

