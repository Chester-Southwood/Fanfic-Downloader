from datetime import date
from selenium import webdriver
import os
import shutil
import sys


def create_folder(address):
    os.mkdir(address)


def create_file(address, title, contents, extension):
    path = create_unique_file_path(address + "\\" + title + "." + extension)
    with open(path, "w") as f:
        f.write(contents)


def create_unique_file_path(address):
    if not os.path.isfile(address):
        return address
    else:
        version_num = 1
        while True:
            new_path = "address[:len(address) - 4]" + " (" + str(version_num) + ")" + address[len(address) - 4:]
            if os.path.isfile(new_path):
                version_num += 1
            else:
                return new_path


def create_unique_folder_path(address):
    if not os.path.isdir(address):
        return address
    else:
        version_num = 1
        while True:
            new_path = address + " (" + str(version_num) + ")"
            if os.path.isdir(new_path):
                version_num += 1
            else:
                return new_path


def download_story(url):
    driver = init_driver()

    try:
        if is_valid_story_url(url, driver):
            driver.get("https://" + url[url.find("fanfiction.net/s/"): len(url)])

            story_name = get_name(driver)
            story_name_valid_chars = replace_invalid_char(story_name)
            local_download = ".\\downloads"

            if not os.path.isdir(local_download):
                os.mkdir(local_download)
            folder_path = create_unique_folder_path(local_download + "\\" + story_name_valid_chars)
            create_folder(folder_path)
            create_file(folder_path, "0. Description", get_description_string(driver), "txt")

            while True:
                create_file(folder_path, replace_invalid_char(get_chapter_name(driver)), get_story_content(driver), "txt")
                if not go_to_next_chap(driver):
                    break

            shutil.make_archive(story_name_valid_chars, 'zip', folder_path)
            shutil.move(story_name_valid_chars + ".zip", folder_path)

            print(story_name + " has been downloaded!")

    except Exception as e:
        print(e + "\n" + story_name + " was not downloaded!")

    driver.quit()


def get_chapter_name(driver):
    chapters = driver.find_elements_by_tag_name("option")

    if len(chapters) == 0:
        return "1. " + get_name(driver)
    else:
        for chapter in chapters:
            if chapter.get_attribute("selected") == "true":
                return chapter.text


def get_description_list(driver):
    profile_container = driver.find_element_by_id("profile_top")
    description_elements = profile_container.find_elements_by_class_name("xcontrast_txt")
    return description_elements


def get_description_string(driver):
    description_list = get_description_list(driver)

    stripped_genrerating = str.strip(description_list[7].text)
    genre_rating = str.split(stripped_genrerating, " ")

    return "Title: " + get_name(driver) + "\n" + \
           "Description: " + description_list[5].text + "\n" + \
           "Author: " + description_list[2].text + "\n" + \
           "Rating: " + genre_rating[1] + "\n" + \
           "Genre: " + genre_rating[0] + "\n" + \
           "General Info: " + description_list[6].text + "\n" + \
           "Downloaded: " + str(date.today())


def get_name(driver):
    return get_description_list(driver)[0].text


def get_story_content(driver):
    story_container = driver.find_element_by_class_name("storytext")
    story_container_elements = story_container.find_elements_by_tag_name("p")
    story_content = ""

    for story_element in story_container_elements:
        story_content += story_element.text + "\n\n"

    return story_content


def go_to_next_chap(driver):
    button_list = driver.find_elements_by_class_name("btn")

    for button in button_list:
        if str.strip(button.text) == "Next >":
            button.click()
            return True

    return False


def init_driver():
    driver_path = os.getenv("CHROMEDRIVER")
    driver = webdriver.Chrome(driver_path)
    return driver


def is_valid_story_url(url, driver):
    stripped_url = url.strip()
    is_valid = False

    possible_start_list = ["https://www.fanfiction.net/s/", "http://www.fanfiction.net/s/", "www.fanfiction.net/s/", "fanfiction.net/s/"]

    if starts_with_any(stripped_url, possible_start_list):

        actual_url = "https://" + stripped_url[stripped_url.find("fanfiction.net/s/"): len(stripped_url)]
        driver.get(actual_url)

        if len(driver.find_elements_by_tag_name("big")) == 1:
            print("Incorrect format for story URL, please verify numeric story id.")
        elif len(driver.find_elements_by_class_name("panel_warning")) == 1:
            print("Story Not Found | Story is Unavailable For Reading")
        else:
            is_valid = True
    else:
        print("URL not within fanfiction.net story directory, please verify URL")

    return is_valid


def main():
    if len(sys.argv) == 2:
        download_story(sys.argv[1])
    else:
        print("Invalid amount of parameters!")


def replace_invalid_char(original_string):
    invalid_char_list = ["\\", "/", ":", "?", '"', "<", ">", "|"]

    for invalid_char in invalid_char_list:
        original_string = original_string.replace(invalid_char, " ")

    return original_string


def starts_with_any(url, possible_start_list):
    url_lower = url.lower()

    for possible_start in possible_start_list:
        if url_lower.startswith(possible_start):
            return True
    return False


if __name__ == "__main__":
    main()