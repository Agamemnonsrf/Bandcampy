# Bandcampy
Python3 script that: 
1) downloads any series of albums from bandcamp (links of bandcamp album pages seperated by commas)
2) automatically adds mp3 metadata for the album and the songs
3) automatically sorts everything into a folder in the directory of your choosing


To run you will need to install all imports using pip

Known bugs:
The script will
1) exit with an error if you try to download an album in a directory where a folder with the same name exists 
2) cause too many "Download Albums" buttons to stack on each other if you press the "Select Albums Download Folder" and then instead of selecting directory, you just quit the file selector window and do it again
3) not work on some certain albums on bandcamp for yet unknown reasons
4) exit with an error if you download too many albums (probably above 30) within a limited amount of time because of a limitation on http requests on bandcamp's side

Notes:
1) Make sure that you have seperated the links with commas correctly when downloading multiple albums at once. You can do this by hitting ctrl + A (to select the entire textbox) and pasting the contents on a txt file to check if the commas separate the links correctly 
