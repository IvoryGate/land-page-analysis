from config import Config
from bs4 import BeautifulSoup
import requests

class RequestResult:
    icon: str
    others: list[str]

def parse_google_play(package_id: str, region: str, lang: str) -> dict:
    search_url = Config.GOOGLE_URL.format(package_id, region, lang)
    try:
        current_header = Config.get_random_headers()
        response = requests.get(url=search_url, headers=current_header, timeout=Config.CRAWLER_TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        icon_tags = soup.find(name='img', attrs={'itemprop': 'image'})
        if not icon_tags:
            icon_tags = soup.find('img', class_="T75of nm4vBd arM4bb")
        
        icon_url = ""
        if icon_tags:
            raw_icon: str = str(icon_tags.get('srcset') or icon_tags.get('src', ''))
            icon_url = raw_icon.split(' ')[0] 

        img_tags = soup.find_all('img', attrs={'alt': 'Screenshot image'})
        if not img_tags:
            img_tags = soup.find_all('img', class_="T75of B5GQxf")
        
        images: list[str] = []

        for img_tag in img_tags:
            src_value: str = str(img_tag.get('srcset') or img_tag.get('src'))
            if src_value:
                clean_url = src_value.split(' ')[0]
                
                if '=' in clean_url:
                    clean_url = clean_url.split('=')[0]
                
                images.append(clean_url)

        return {"icon": icon_url, "others": images}
    
    except Exception as e:
        raise Exception(f"GooglePlay解析失败: {str(e)}")

def parse_apple_store(package_id: str, region: str, lang: str) -> dict:
    search_url = Config.APPLE_URL.format(package_id, region, lang)
    try:
        current_header = Config.get_random_headers()
        response = requests.get(url=search_url, headers=current_header, timeout=Config.CRAWLER_TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        icon_tag = soup.select('div.app-icon-contianer source')
        icon_url = icon_tag[0]["srcset"].split(" ")[0]

        img_tags = soup.select('#product_media_phone_ source')
        images: list[str] = []
        for tag in img_tags:
            images.append(tag["srcset"].split(" ")[0])
        
        return {"icon": icon_url, "others": images}
    except Exception as e:
        raise Exception(f"AppStore解析失败: {str(e)}")