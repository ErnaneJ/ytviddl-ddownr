import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class YtviddlDdownr:
  """
  A web crawler class to download YouTube videos using the ddownr website.
  """

  def __init__(self):
    """
    Initializes the YtviddlDdownr with necessary configurations.
    Loads environment variables, sets up the Chrome WebDriver, and 
    initializes the list of YouTube videos to download.
    """
    load_dotenv()

    self.base_url = "https://ddownr.com/en/youtube-video-downloader"
    self.service = Service(executable_path=os.getenv("CHROME_DRIVER_PATH"))
    self.driver = webdriver.Chrome(service=self.service)
    self.videos = [
      "https://www.youtube.com/watch?v=L0_nXyTMyqM"
    ]

  def run(self):
    """
    Starts the video download process.
    """
    self._download_videos()

  def close(self):
    """
    Closes the WebDriver instance, effectively ending the session.
    """
    self.driver.quit()

  def _download_videos(self):
    """
    Downloads each video in the self.videos list by interacting with the ddownr website.
    """
    for video_url in self.videos:
      self.driver.get(self.base_url)
      original_tab = self.driver.current_window_handle
      time.sleep(1)

      # Find and interact with the input and download button elements
      input_url = self.driver.find_element(By.CSS_SELECTOR, "input.input-url.link")
      download_button = self.driver.find_element(By.CSS_SELECTOR, "button.btn-download")
      
      input_url.send_keys(video_url)
      download_button.click()
      self.driver.switch_to.window(original_tab)

      time.sleep(5)

      # Wait for the download link to be available
      download_link = self.driver.find_element(By.CSS_SELECTOR, "a.btn-download")
      while not download_link.get_attribute("href"):
        time.sleep(1)

      download_link.click()
      self.driver.switch_to.window(original_tab)

      # Wait for the video to be downloaded
      video_title = self.driver.find_element(By.CSS_SELECTOR, "div.video-title").text
      download_folder = os.getenv("DOWNLOAD_FOLDER")
      target_folder = os.getenv("TARGET_FOLDER")
      video_file_path = os.path.join(download_folder, f"{video_title}.mp4")

      while not os.path.exists(video_file_path):
        time.sleep(1)

      # Move the downloaded file to the target folder
      new_file_path = os.path.join(target_folder, f"{video_title}.mp4")
      os.rename(video_file_path, new_file_path)

      # Close any additional tabs that were opened
      for tab in self.driver.window_handles:
        if tab != original_tab:
          self.driver.switch_to.window(tab)
          self.driver.close()
      
      self.driver.switch_to.window(original_tab)

if __name__ == "__main__":
  crawler = YtviddlDdownr()
  crawler.run()
  crawler.close()
