import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

chromedriver = 'D:/companyProject/authServer/win/chromedriver.exe'
geturl = 'https://graph.fin-shine.com/oauth2/auth?client_id=b964b678-4f30-4c69-0000-000000000012&response_type=code&state=%s&redirect_uri=http://8.136.208.91/test&scope=User.Profile.Read User.Profile.ReadWrite User.Files.Read User.Files.ReadWrite'

url = geturl % str(int(time.time()))

print(url)

username = "wangjiang"
password = "1991620wind634"
company = "SOIMT"
#
chrome_driver_path_obj = Service(chromedriver)
browser = webdriver.Chrome(service=chrome_driver_path_obj)

time.sleep(0.5)
browser.get(url)
time.sleep(2)
# browser.
print(browser.page_source)

browser.find_element("id", "email").send_keys(username)
browser.find_element("id", "password").send_keys(password)
browser.find_element("id", "companycode").send_keys(company)
browser.find_element("class name", "login_button").click()

time.sleep(1)
browser.close()
browser.quit()