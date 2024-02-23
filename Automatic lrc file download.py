from bs4 import BeautifulSoup
import requests,re
from pathlib import Path
import os



captchaTry = 0

def check_captcha_form(soup):
    captcha = soup.find_all("form", {"id": "captcha-form"})
    if captcha:
        return True
    else:
        return False

def get_first_link(searchLink):
    response = requests.get(searchLink)
    soup = BeautifulSoup(response.text, "html.parser")

    elements = soup.find_all("div", class_="egMi0")
    try:
        first_res = elements[0]
        links = first_res.find_all("a")
        link_url = links[0]["href"]
        match = re.search(r'https://[^\&]+', link_url)
    except IndexError:
        print("List out of href links:")
        print(elements)
        match = False

    if match:
        link = match.group()
        return link
    else:
        thereIsCaptcha = check_captcha_form(soup)
        global captchaTry

        if thereIsCaptcha:
            print("Captcha Block Found. We will try once again and if found again, the program will be terminated.")
            captchaTry += 1

            if captchaTry > 2:
                print("Captcha is blocking us from getting the link. Please try again later or use a proxy network.")
                exit()
            return "Captcha_Error"

        return False

def get_lyrics(lrc_link):
    response = requests.get(lrc_link)
    soup = BeautifulSoup(response.text, "html.parser")

    elements = soup.find_all("div", class_="lyrics_details")

    try:
        lyrics = elements[0].text
        return lyrics
    except IndexError:
        print("Link may have an error or our website doesn't have your desired lyrics:")
        print(elements)
        return False

def write_to_file(lyrics, lrcFileName):
    lrc_extension = lrcFileName.replace(".mp3", ".lrc")
    file_path = Path(f"my_LRCS/{lrc_extension}")

    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with file_path.open("x") as f:
            f.write(lyrics)
        print(f"Successfully written: {lrcFileName}")
    except FileExistsError:
        print(f"{lrcFileName} file already exists. We didn't override the file. If you want to override it, please specify.")

songTitles = ['Coldplay - Sparks']

def main():
    for songName in songTitles:
        line = songName.replace("(Audio)", "").replace("(Official Video)", "").replace("(Official Lyric Video)", "")

        if line == "":
            print("Song Name is Empty!")
            return

        searchLink = f"https://www.google.com/search?q={line} lrc megalobiz"
        lrc_link = get_first_link(searchLink)

        if lrc_link and lrc_link != "Captcha_Error":
            lyrics = get_lyrics(lrc_link)
            if lyrics:
                write_to_file(lyrics, songName)
        elif not lrc_link:
            print(f"No link found for: {line}")

main()
