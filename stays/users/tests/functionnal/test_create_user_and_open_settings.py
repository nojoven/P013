import pytest
from selenium.webdriver.common.by import By

@pytest.mark.django_db
def test_register_user(selenium, live_server):
    # Allez à la page de login
    selenium.get(live_server.url)

    selenium.set_window_size(1440, 780)
    selenium.find_element(By.CSS_SELECTOR, ".header-avatar").click()
    selenium.find_element(By.LINK_TEXT, "Sign In").click()
    selenium.find_element(By.LINK_TEXT, "REGISTER").click()
    selenium.find_element(By.ID, "email").click()
    selenium.find_element(By.ID, "email").send_keys("atester2024@stays.com")
    selenium.find_element(By.ID, "username").send_keys("atester2024")
    selenium.find_element(By.ID, "password1").click()
    selenium.find_element(By.ID, "password1").send_keys("AVNS_zwQY3x5vU-")
    selenium.find_element(By.ID, "password2").click()
    selenium.find_element(By.ID, "password2").send_keys("AVNS_zwQY3x5vU-")
    selenium.find_element(By.CSS_SELECTOR, ".btn").click()
    selenium.find_element(By.ID, "username").click()
    selenium.find_element(By.ID, "username").send_keys("atester2024@stays.com")
    selenium.find_element(By.ID, "password").click()
    selenium.find_element(By.ID, "password").send_keys("AVNS_zwQY3x5vU-")
    selenium.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    selenium.find_element(By.LINK_TEXT, "Settings").click()
    selenium.wait(5)