from bs4 import BeautifulSoup
import requests, webbrowser,re
import os
from pathlib import Path
import os

filename ="songList.txt"
captchaTry=0

def check_captcha(searchLink):
			
	response=requests.get(searchLink)		 	
	soup=BeautifulSoup(response.text,"html.parser")		
	code=soup.prettify()	
	captcha= soup.find_all("form",{"id":"captcha-form"})
			
	if(captcha):
		print("Captcha found Oh noo. anandon mission fastt.")
		return True
	
	else:
		return False





def get_first_link(searchLink):
	response=requests.get(searchLink)
	 	
	soup=BeautifulSoup(response.text,"html.parser")
	
	code=soup.prettify()
	
	elements = soup.find_all("div", class_="egMi0")
	try:
		first_res=elements[0]			
		#print(first_res)
		print("\n\n")		
		links = first_res.find_all("a")
		for link in links:
		    link_url = link["href"]
		#print(code)
		match = re.search(r'https://[^\&]+', link_url)

	except IndexError:
		print(f"List out of errors : \n")
		print(elements)
		match=False
				
	# Check if a match was found
	if match:
	    link = match.group()
	    #print(link)
	    return link
	else:
	    
	    thereIsCaptcha = check_captcha(searchLink)
	    global captchaTry
	    
	    if(thereIsCaptcha):
	    	print("Captcha Block Found Will run again and If again Found terminate the program. ")
	    	
	    	captchaTry=captchaTry +1
	    	
	    	if(captchaTry > 2):
	    		print("\n Captcha Is blocking Scraping Please Try after Some time Or use a proxy Network of adress. ")
	    		exit()
	    	return "Captcha_Error"
	    else:
	    	print("No link found ")
	    
	    return False
	  
	              





def get_lyrics(lrc_link):
	response=requests.get(lrc_link)
		 	
	soup=BeautifulSoup(response.text,"html.parser")
	
	code=soup.prettify()
	
	elements = soup.find_all("div", class_="lyrics_details")
	
	try:
		#print("Lyrics is \n\n")
		lyrics=elements[0].text
		return lyrics
	except IndexError:
		print(f"Complex file Name :  ")
		print(elements)
		return False
				

		
				
						
										
def write_to_file(lyrics,lrcFileName):
	lrc_extension=lrcFileName.replace(".mp3",".lrc")
	# Create a Path object for the new file.
	file_path = Path(f"my_LRCS/{lrc_extension}")
	
	# Create the folder if it does not exist.
	file_path.parent.mkdir(parents=True, exist_ok=True)
	
	# Open the file for writing using the 'x' mode.
	try:
		with file_path.open("x") as f:
		    f.write(lyrics)
		print(f"Sucesdfully written:  {lrcFileName} ")
	except FileExistsError:
		print(f"{lrcFileName} file already exists")		




def main():
	with open(filename,"r") as f:
		line=f.readline()
		while line != "":				
			#print(line)
	
	    # Read the next line from the file.		
			search_query =f"{line} lrc megalobiz"
			
			searchLink=f"""https://www.google.com/search?q={search_query}"""
								
			lrc_link= get_first_link(searchLink)
			
			if(lrc_link and lrc_link !="Captcha_Error"):
				lyrics=get_lyrics(lrc_link)
				if(lyrics):
					write_to_file(lyrics,line)
					
					
				#print(lyrics)
			elif(lrc_link =="Captcha_Error"):
				pass	
				
			elif(not lrc_link):
				print(f"No link found for: {line}")
			line = f.readline()


main()