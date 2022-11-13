import pyuseragents
import time
import os

from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from loguru import logger
from sys import stderr


logger.remove()
logger.add(stderr,
           format="<white>{time:HH:mm:ss}</white> | "
                  "<level>{level: <8}</level> | "
                  "<white>{message}</white>")


def clear():
    os.system('clear || cls')

def quit():
    print("\n\n")
    logger.success('The work is finished | Press Enter to exit')
    input(">> ")
    exit()


def logo():
    print("""
                      __         __          ___     
 _      ______  _____/ /______ _/ /_  ____  / (_)____
| | /| / / __ \/ ___/ //_/ __ `/ __ \/ __ \/ / / ___/
| |/ |/ / /_/ / /  / ,< / /_/ / / / / /_/ / / / /__  
|__/|__/\____/_/  /_/|_|\__,_/_/ /_/\____/_/_/\___/  
telegram >> https://t.me/workaholic_channel
""")

def _auto_form(data):
    if os.path.isfile('driver/chromedriver.exe') == True:
        driver = os.path.abspath('driver/chromedriver.exe')

    elif os.path.isfile('driver/chromedriver') == True:
        driver = os.path.abspath('driver/chromedriver')
    
    else:
        print("driver not found in Driver Folder")
        quit()

    url = "https://www.projectbrx.io"
    options = Options()
    options.headless = True
    options.add_argument("window-size=1200x600")
    options.add_argument(f'user-agent={pyuseragents.random()}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--mute-audio")
    options.add_argument('log-level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-infobars')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(driver, options=options) 

    try:

        browser.get(url)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="root"]/div/div/div/footer/div/div[1]/form/div[1]/input').send_keys(f"{data}")                
        browser.find_element_by_xpath('//*[@id="root"]/div/div/div/footer/div/div[1]/form/div[2]/button').click()
        time.sleep(2)

        logger.success(f'{data} | The email has been successfully registered')
        with open('data/registered.txt', 'a') as file:
                    file.write(f'{data}\n')


    except Exception as ex:

        logger.error(f'{data} | Unexpected error: {ex}')
        with open('data/unregistered.txt', 'a') as file:
            file.write(f'{data}\n')


    finally:

        browser.close()
        browser.quit()



if __name__ == '__main__':
    clear()
    logo()

    logger.success('Quantity Threads')
    Threads = int(input(">> "))
    full_data = []
    emails_folder = os.path.abspath("data/email.txt")
    with open(emails_folder) as f:
            emails = [line.rstrip() for line in f.readlines()]

    if len(emails) == 0:
        logger.error('You did not upload an email address to the data/email.txt folder')
        time.sleep(1)
        quit()

    else:
        for email in emails:

            if email == "":
                continue 


            elif "@" not in email:
                continue

            else:
                full_data.append(email)
                
    clear()
    logo()
    logger.success(f'Threads | {Threads}')

    logger.success(f'Email address | {len(full_data)}')
    print("\n\n")
    P = Pool(Threads)
    P.map(_auto_form, full_data)
    quit()