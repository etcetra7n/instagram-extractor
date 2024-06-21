from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as wait
from time import sleep
from requests import get


print("Enter username: ", end='')
uname = input()
print("Enter password: ", end='')
pword = input()

print("Loading webdriver...")
opts = Options()
opts.add_argument("--headless")
driver1 = webdriver.Firefox(options = opts)
driver2 = webdriver.Firefox(options = opts)
count = 1
fname = 1
cap = 1000
PAGE = "https://www.instagram.com/memes"

driver1.get("https://www.instagram.com")
print("Logging in... (1/2)")
wait(driver1, 20).until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(uname)
driver1.find_element(By.NAME, "password").send_keys(pword)
driver1.find_element(By.XPATH, "//button[@type='submit']").click()

print("Logging in... (2/2)")
driver2.get("https://www.instagram.com")
wait(driver2, 20).until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(uname)
driver2.find_element(By.NAME, "password").send_keys(pword)
driver2.find_element(By.XPATH, "//button[@type='submit']").click()

sleep(4)
driver1.get(PAGE)
sleep(10)
last_height = driver1.execute_script("return document.body.scrollHeight")
print("Starting..")

while(True):
    already_downloaded = []
    with open(f"./instagram_extractor.var", "r") as f:
        lines = f.readlines()
        if len(lines) >= 1:
            already_downloaded = [x.replace("\n", "") for x in lines]
    with open(f".p/instagram_extract_count.var", "r") as f:
        lines = f.readlines()
        fname = int(lines[0])
    file = ""
    try:
        while(count<=cap):
            #wait(driver2, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd']")))
            #posts = driver1.find_elements(By.XPATH, "//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd']")
            posts = driver1.find_elements(By.XPATH, "//a[@role='link']")
            for post in posts:
                try:
                    link = post.get_attribute('href')
                except:
                    continue
                if link in already_downloaded:
                    print("Skipping already downloaded media...")
                    continue
                if ('/p/' in link):
                    driver2.get(link)
                    img = wait(driver2, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "_aagu")))
                    file = f"./instagram_downloaded_content/{fname}.png"
                    sleep(0.6)
                    img.screenshot(file)
                    print(f"Download complete: {fname}.png ({count}/{cap})")
                elif('/reel/' in link):
                    driver2.get(link)
                    sleep(1)
                    vid = wait(driver2, 20).until(EC.presence_of_element_located((By.XPATH, "//video")))
                    recieved = False
                    tries=1
                    response = None
                    while(tries<=2):
                        try:
                            response = get(vid.get_attribute('src'))
                            recieved = True
                            break
                        except:
                            tries+=1
                            continue
                    if not recieved:
                        print("Cannot fetch video file. Continuing...")
                        continue
                    file = f"./instagram_downloaded_content/{fname}.mp4"
                    with open(file, 'wb') as f:
                        f.write(response.content)
                    print(f"Download complete: {fname}.mp4 ({count}/{cap})")
                else:
                    continue
                count+=1
                fname +=1
                with open(f"./instagram_extract_count.var", "w") as f:
                    f.seek(0)
                    f.write(f"{fname}")
                with open(f"./instagram_extractor.var", "a") as f:
                    f.write(f"{link}\n")
            print("Scrolling down...")
            driver1.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll down to bottom
            sleep(0.8) # Wait to load page
            new_height = driver1.execute_script("return document.body.scrollHeight") # Calculate new scroll height and compare with last scroll height
            last_height = new_height
            
    except KeyboardInterrupt:
        print(f"Task interrupted: Downloaded {count-1} out of {cap} files.")
        print("Do you want to terminate the task? (y/n): ", end='')
        d = input()
        if d=="y":
            print("Task terminated.")
            break
        else:
            print("Continuing...")
            continue
    except:
        raise
        #sleep(10)
        #continue
    else:
        print("Task complete: Donwloaded {count-1} files.")
    
driver1.quit()
driver2.quit()
