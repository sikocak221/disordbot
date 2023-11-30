import requests, os, stdiomask
from uuid import uuid4
from json import loads
import time

class Intsatools:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    def login(self):
        headers = {
            "Host": "i.instagram.com",
            "X-Ig-Connection-Type": "WiFi",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Ig-Capabilities": "36r/Fx8=",
            "User-Agent": "Instagram 159.0.0.28.123 (iPhone8,1; iOS 14_1; en_SA@calendar=gregorian; ar-SA; scale=2.00; 750x1334; 244425769) AppleWebKit/420+",
            "X-Ig-App-Locale": "en",
            "X-Mid": "Ypg64wAAAAGXLOPZjFPNikpr8nJt",
            "Content-Length": "778",
            "Accept-Encoding": "gzip, deflate"
        }
        data = {

                "username":self.username,
                "reg_login":"0",
                "enc_password":f"#PWD_INSTAGRAM:0:&:{self.password}",
                "device_id":uuid4(),
                "login_attempt_count":"0",
                "phone_id":uuid4()
                }
        url = "https://i.instagram.com/api/v1/accounts/login/"
        r = requests.post(url=url,headers=headers,data=data)
        session_id = r.cookies.get("sessionid")
        if 'The password you entered is incorrect' in r.text:
            print(f"[-] Logged In Failed")
            return False
        elif 'logged_in_user' in r.text:
            print(f"[+] Logged In Success")
            with open('instagram_cookies.txt', 'w') as f:
                f.write(session_id)
            return True
        else:
            print(f"[-] Logged In Failed")
            return False
    def download_reels(self, url):
        n = 0
        while n <= 10:
            n+=1
            with open('instagram_cookies.txt') as f:
                lines = f.readlines()
                sessionid = lines[0]
            params = { '__a': 1, '__d': 1 }
            cookies = { 'sessionid': sessionid}
            response = requests.get(url, params, cookies=cookies)
            if response.status_code == 200:
                profile_data_json = response.text
                parsed_data = loads(profile_data_json)
                highest_quality_url = None
                highest_quality = 0
                for data in parsed_data['items'][0]['video_versions']:
                    if 'width' in data and 'height' in data:
                        quality = data['width'] * data['height']
                        if quality > highest_quality:
                            highest_quality = quality
                            highest_quality_url = data['url']
                return parsed_data["items"][0]["caption"]["text"], highest_quality_url
            elif response.status_code == 404:
                return None, None
            elif response.status_code == 401:
                print('Something went wrong')
                print('Error Code:', response.status_code)
                print('Reason:', response.reason)
                time.sleep(15)
                self.login()
            else:
                return None, None
        return None, None
    