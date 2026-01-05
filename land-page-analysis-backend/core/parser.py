from config import Config
from bs4 import BeautifulSoup
import requests


class RequestResult:
    icon: str
    others: list[str]

def parse_google_play(package_id: str, region: str, lang: str) -> RequestResult:
    search_url = Config.GOOGLE_URL.format(package_id, region, lang)
    try:
        response = requests.get(url=search_url, headers=Config.HEADERS, timeout=Config.CRAWLER_TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        
        icon_tags = soup.find_all('img', class_="T75of nm4vBd arM4bb")
        icon_urls = icon_tags[0]["src"] if icon_tags else ""

        img_tags = soup.find_all('img', class_="T75of B5GQxf")
        images = [tag['src'] for tag in img_tags]

        return {"icon": icon_urls, "others": images}
    
    except Exception as e:
        raise Exception(f"GooglePlay解析失败: {str(e)}")

def parse_apple_store(package_id: str, region: str, lang: str) -> str:
    search_url = Config.APPLE_URL.format(package_id, region, lang)
    try:
        response = requests.get(url=search_url, headers=Config.HEADERS, timeout=Config.CRAWLER_TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        icon_tag = soup.select('div.app-icon-contianer source')
        icon_urls: str = icon_tag[0]["srcset"].split(" ")[0] if icon_tag else ""
        
        img_tags = soup.select('#product_media_phone_ source')
        images: list[str] = [tag["srcset"].split(" ")[0] for tag in img_tags]
        
        return {"icon": icon_urls, "others": images}
    except Exception as e:
        raise Exception(f"AppStore解析失败: {str(e)}")