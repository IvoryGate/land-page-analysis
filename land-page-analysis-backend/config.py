import os
import random
from dotenv import load_dotenv

load_dotenv()

class Config:

    # 数据库配置
    HOST: str | None = os.getenv("HOST")
    PORT: int | None = int(os.getenv("PORT"))
    USR: str | None = os.getenv("USR")
    PASSWORD: str | None = os.getenv("PASSWORD")
    DATABASE: str | None = os.getenv("DATABASE")
    CHARSET: str | None = os.getenv("CHARSET")

    # --- 爬虫配置信息 ---
    CRAWLER_MAX_WORKERS: int = int(os.getenv("CRAWLER_MAX_WORKERS"))
    CRAWLER_TIMEOUT: int = int(os.getenv("CRAWLER_TIMEOUT"))
    
    # HEADERS: dict | None = {
    #     'User-Agent': os.getenv('USER_AGENT')
    # }

    UA_POOL: list[str] = [
        # Chrome on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        # Chrome on MacOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        # Firefox on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        # Safari on MacOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        # Edge on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    ]

    # --- Google Play Url 配置 ---
    GOOGLE_URL: str = str(os.getenv("GOOGLE_URL"))

    # --- Apple Store Url 配置 ---
    APPLE_URL: str = str(os.getenv("APPLE_URL"))

    @classmethod
    def get_random_headers(cls) -> dict[str, str]:
        """每次调用返回一个带有随机 UA 的 Headers 字典"""
        return {
            'User-Agent': random.choice(cls.UA_POOL),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
    
    COUNTRY_LANG_MAP = {
        # --- 热门市场 (Hot Markets) ---
        'CN': 'zh', 'TW': 'zh', 'HK': 'zh',  # 大中华区
        'US': 'en', 'GB': 'en', 'CA': 'en', 'AU': 'en', 'NZ': 'en', # 英语系
        'JP': 'ja', 'KR': 'ko', # 日韩
        'FR': 'fr', 'DE': 'de', 'IT': 'it', 'ES': 'es', # 西欧四强
        'BR': 'pt', 'PT': 'pt', # 葡语系
        'RU': 'ru', # 俄语系
        'IN': 'en', 'ID': 'id', 'TH': 'th', 'VN': 'vi', # 亚洲新兴
        'TR': 'tr', 'SA': 'ar', 'AE': 'ar', # 中东

        # --- A ---
        'AD': 'ca', 'AE': 'ar', 'AF': 'fa', 'AG': 'en', 'AI': 'en', 'AL': 'sq', 'AM': 'hy', 
        'AO': 'pt', 'AQ': 'und', 'AR': 'es', 'AS': 'sm', 'AT': 'de', 'AW': 'nl', 'AX': 'sv', 
        'AZ': 'az',
        # --- B ---
        'BA': 'bs', 'BB': 'en', 'BD': 'bn', 'BE': 'nl', 'BF': 'fr', 'BG': 'bg', 'BH': 'ar', 
        'BI': 'rn', 'BJ': 'fr', 'BL': 'fr', 'BM': 'en', 'BN': 'ms', 'BO': 'es', 'BQ': 'nl', 
        'BS': 'en', 'BT': 'dz', 'BV': 'no', 'BW': 'en', 'BY': 'be', 'BZ': 'en',
        # --- C ---
        'CC': 'en', 'CD': 'fr', 'CF': 'fr', 'CG': 'fr', 'CH': 'de', 'CI': 'fr', 'CK': 'en', 
        'CL': 'es', 'CM': 'fr', 'CO': 'es', 'CR': 'es', 'CU': 'es', 'CV': 'pt', 'CW': 'nl', 
        'CX': 'en', 'CY': 'el', 'CZ': 'cs',
        # --- D ---
        'DE': 'de', 'DJ': 'fr', 'DK': 'da', 'DM': 'en', 'DO': 'es', 'DZ': 'ar',
        # --- E ---
        'EC': 'es', 'EE': 'et', 'EG': 'ar', 'EH': 'ar', 'ER': 'ti', 'ES': 'es', 'ET': 'am',
        # --- F ---
        'FI': 'fi', 'FJ': 'en', 'FK': 'en', 'FM': 'en', 'FO': 'fo', 'FR': 'fr',
        # --- G ---
        'GA': 'fr', 'GB': 'en', 'GD': 'en', 'GE': 'ka', 'GF': 'fr', 'GG': 'en', 'GH': 'en', 
        'GI': 'en', 'GL': 'kl', 'GM': 'en', 'GN': 'fr', 'GP': 'fr', 'GQ': 'es', 'GR': 'el', 
        'GS': 'en', 'GT': 'es', 'GU': 'en', 'GW': 'pt', 'GY': 'en',
        # --- H ---
        'HK': 'zh', 'HM': 'en', 'HN': 'es', 'HR': 'hr', 'HT': 'fr', 'HU': 'hu',
        # --- I ---
        'ID': 'id', 'IE': 'en', 'IL': 'he', 'IM': 'en', 'IN': 'en', 'IO': 'en', 'IQ': 'ar', 
        'IR': 'fa', 'IS': 'is', 'IT': 'it',
        # --- J ---
        'JE': 'en', 'JM': 'en', 'JO': 'ar', 'JP': 'ja',
        # --- K ---
        'KE': 'en', 'KG': 'ky', 'KH': 'km', 'KI': 'en', 'KM': 'ar', 'KN': 'en', 'KP': 'ko', 
        'KR': 'ko', 'KW': 'ar', 'KY': 'en', 'KZ': 'ru',
        # --- L ---
        'LA': 'lo', 'LB': 'ar', 'LC': 'en', 'LI': 'de', 'LK': 'si', 'LR': 'en', 'LS': 'en', 
        'LT': 'lt', 'LU': 'fr', 'LV': 'lv', 'LY': 'ar',
        # --- M ---
        'MA': 'ar', 'MC': 'fr', 'MD': 'ro', 'ME': 'sr', 'MF': 'fr', 'MG': 'mg', 'MH': 'en', 
        'MK': 'mk', 'ML': 'fr', 'MM': 'my', 'MN': 'mn', 'MO': 'zh', 'MP': 'en', 'MQ': 'fr', 
        'MR': 'ar', 'MS': 'en', 'MT': 'mt', 'MU': 'en', 'MV': 'dv', 'MW': 'en', 'MX': 'es', 
        'MY': 'en', 'MZ': 'pt',
        # --- N ---
        'NA': 'en', 'NC': 'fr', 'NE': 'fr', 'NF': 'en', 'NG': 'en', 'NI': 'es', 'NL': 'nl', 
        'NO': 'no', 'NP': 'ne', 'NR': 'en', 'NU': 'en', 'NZ': 'en',
        # --- O ---
        'OM': 'ar',
        # --- P ---
        'PA': 'es', 'PE': 'es', 'PF': 'fr', 'PG': 'en', 'PH': 'en', 'PK': 'en', 'PL': 'pl', 
        'PM': 'fr', 'PN': 'en', 'PR': 'es', 'PS': 'ar', 'PT': 'pt', 'PW': 'en', 'PY': 'es',
        # --- Q ---
        'QA': 'ar',
        # --- R ---
        'RE': 'fr', 'RO': 'ro', 'RS': 'sr', 'RU': 'ru', 'RW': 'rw',
        # --- S ---
        'SA': 'ar', 'SB': 'en', 'SC': 'fr', 'SD': 'ar', 'SE': 'sv', 'SG': 'en', 'SH': 'en', 
        'SI': 'sl', 'SJ': 'no', 'SK': 'sk', 'SL': 'en', 'SM': 'it', 'SN': 'fr', 'SO': 'so', 
        'SR': 'nl', 'SS': 'en', 'ST': 'pt', 'SV': 'es', 'SX': 'nl', 'SY': 'ar', 'SZ': 'en',
        # --- T ---
        'TC': 'en', 'TD': 'fr', 'TF': 'fr', 'TG': 'fr', 'TH': 'th', 'TJ': 'tg', 'TK': 'en', 
        'TL': 'pt', 'TM': 'tk', 'TN': 'ar', 'TO': 'to', 'TR': 'tr', 'TT': 'en', 'TV': 'en', 
        'TW': 'zh', 'TZ': 'sw',
        # --- U ---
        'UA': 'uk', 'UG': 'en', 'UM': 'en', 'US': 'en', 'UY': 'es', 'UZ': 'uz',
        # --- V ---
        'VA': 'it', 'VC': 'en', 'VE': 'es', 'VG': 'en', 'VI': 'en', 'VN': 'vi', 'VU': 'fr',
        # --- W ---
        'WF': 'fr', 'WS': 'sm',
        # --- Y ---
        'YE': 'ar', 'YT': 'fr',
        # --- Z ---
        'ZA': 'en', 'ZM': 'en', 'ZW': 'en'
    }