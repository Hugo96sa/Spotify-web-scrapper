import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

# Define CSS selectors
TRACKLIST_CONTAINER = 'div[data-testid="playlist-tracklist"]'
TITLE_SELECTOR = f'{TRACKLIST_CONTAINER} div.Text__TextElement-sc-if376j-0.ksSRyh.encore-text-body-medium.t_yrXoUO3qGsJS4Y6iXX.standalone-ellipsis-one-line'
ARTIST_SELECTOR = f'{TRACKLIST_CONTAINER} span.Text__TextElement-sc-if376j-0.duYgEj.encore-text-body-small.rq2VQ5mb9SDAFWbBIUIn.standalone-ellipsis-one-line'
ALBUM_SELECTOR = f'{TRACKLIST_CONTAINER} span.Text__TextElement-sc-if376j-0.gYdBJW.encore-text-body-small'
DURATION_SELECTOR = f'{TRACKLIST_CONTAINER} div.Text__TextElement-sc-if376j-0.duYgEj.encore-text-body-small.Btg2qHSuepFGBG6X0yEN'
IMG_SELECTOR = f'{TRACKLIST_CONTAINER} img.mMx2LUixlnN_Fu45JpFB.rkw8BWQi3miXqtlJhKg0.Yn2Ei5QZn19gria6LjZj'


def get_playlist_url(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()


def scraping(spotify_playlist_url, output_csv):
    driver.maximize_window()
    driver.get(spotify_playlist_url)
    driver.implicitly_wait(10)
    time.sleep(3)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        try:
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            print("Operation scrolling!!")
            time.sleep(3)  # Adjust the sleep time as needed
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("Reached the bottom of the page")
                break
            last_height = new_height
        except Exception as e:
            print(f"Error during scrolling: {e}")
            break

    # Now that all data is loaded, scrape it using CSS selectors
    titles = driver.find_elements(By.CSS_SELECTOR, TITLE_SELECTOR)
    artists = driver.find_elements(By.CSS_SELECTOR, ARTIST_SELECTOR)
    albums = driver.find_elements(By.CSS_SELECTOR, ALBUM_SELECTOR)
    durations = driver.find_elements(By.CSS_SELECTOR, DURATION_SELECTOR)
    songs_img = driver.find_elements(By.CSS_SELECTOR, IMG_SELECTOR)

    all_data = []

    for index in range(len(titles)):
        all_data.append({
            "title": titles[index].text,
            "artist": artists[index].text,
            "album": albums[index].text,
            "duration": durations[index].text,
            "album_image": songs_img[index].get_attribute('src')
        })

    df = pd.DataFrame(data=all_data)
    df.to_csv(output_csv, index=False)

    driver.close()

    return f"data has been saved in {output_csv}"
