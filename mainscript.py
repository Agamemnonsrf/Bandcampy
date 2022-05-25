import os
import re
import shutil
from tkinter import *
from tkinter import filedialog, messagebox

import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3
from titlecase import titlecase


def mainscript():
    def opendir():
        home = os.path.expanduser('~')
        window.filename = filedialog.askdirectory(
            initialdir=home, title="Select Folder")
        global directorypath
        directorypath = window.filename
        button = Button(text="Download Albums", command=geturl,
                        fg="yellow", bg="black").pack()

    def geturl():
        global rawurlpin
        allurls = entry.get()
        rawurlpin = allurls.split(",")
        x = 0
        for i in rawurlpin:
            rawurlpin[x] = requests.get(i)
            x += 1
        window.destroy()

    window = Tk()
    C = Canvas(window, bg="black", height=50, width=450)
    C.pack()
    window.title('Download Albums From Bandcamp')
    button2 = Button(text="Select Albums Download Folder",
                     fg="yellow", bg="black", command=opendir).pack()
    greeting = Label(
        text="Enter Bandcamp Album URLs Separated By Commas:", fg="yellow", bg="black")
    greeting.pack()
    entry = Entry(text="Enter Bandcamp Album URLs Separated By Commas:",
                  fg="yellow", bg="black", width=50)
    entry.pack()

    window.mainloop()

    for url in rawurlpin:
        urlist, songnames = [], []
        index = 0

        nummytrack = re.search(r'(?<=numTracks":)[^,]*', url.text)
        songnum = nummytrack.group(0)

        num2 = 0
        for i in range(int(songnum)):
            num = url.text.find('https://t4.bcbits', num2)

            songurl = url.text[num:(num + 211)]
            urlist.append(songurl)
            num2 = num + 212

        urltext = url.text
        urltext = urltext.replace('|', '#')

        exclude = [':', '\\', '/', '?', '"', '<', '>', '|', '.', '*']
        result = re.search('<title>(.*)</title>', urltext)
        nameauthor = result.group(1)

        if r'&#39;' in nameauthor:
            nameauthor = nameauthor.replace(r'&#39;', "'")
        if r'&amp;' in nameauthor:
            nameauthor = nameauthor.replace('&amp;', '&')
        for i in exclude:
            if i in nameauthor:
                nameauthor = nameauthor.replace(i, ' ')

        nameauthor = nameauthor.split(' # ')

        filename = nameauthor[0]
        filename = filename.strip()

        songnames = re.findall(
            '<span class="track-title">(.*)</span></a>', urltext)
        for i in range(len(songnames)):

            if r'&#39;' in songnames[i]:
                songnames[i] = songnames[i].replace(r'&#39;', "'")
            if r'&amp;' in songnames[i]:
                songnames[i] = songnames[i].replace('&amp;', '&')
            if r'/' in songnames[i]:
                songnames[i] = songnames[i].replace(r'/', ' ')
            if r'*' in songnames[i]:
                songnames[i] = songnames[i].replace(r'*', ' ')
            if r'?' in songnames[i]:
                songnames[i] = songnames[i].replace(r'?', ' ')

        for i in exclude:
            x = 0
            if i in songnames[x]:
                songnames[x] = songnames[x].replace(i, ' ')
            x += 1

        if os.path.exists(directorypath + '/' + filename):
            shutil.rmtree(directorypath + '/' + filename)
            os.mkdir(directorypath + '/' + filename)
        else:
            os.mkdir(directorypath + '/' + filename)

        urlistExclude = ['{', '}', ',', '"', 'n', '@']
        for i in range(len(urlist)):
            while urlist[i][-1:] in urlistExclude:
                if urlist[i][-1:] == '}':
                    urlist[i] = urlist[i][:-1]
                if urlist[i][-1:] == '{':
                    urlist[i] = urlist[i][:-1]
                if urlist[i][-1:] == ',':
                    urlist[i] = urlist[i][:-1]
                if urlist[i][-1:] == '"':
                    urlist[i] = urlist[i][:-1]
                if urlist[i][-1:] == 'n':
                    urlist[i] = urlist[i][:-1]
                if urlist[i][-1:] == '@':
                    urlist[i] = urlist[i][:-1]

        for i in urlist:
            x = requests.get(i)
            path = directorypath + '/' + filename + \
                '/' + songnames[index] + '.mp3'
            with open(path, 'wb')as f:
                f.write(x.content)
            index += 1

        arturl = re.search(
            '<meta property="og:image" content="(.*)">', urltext)
        albumart = requests.get(arturl.group(1))
        path2 = directorypath + '/' + filename + '/'+filename+'.png'
        with open(path2, 'wb')as f:
            f.write(albumart.content)

        for i in range(int(songnum)):

            currentsongpath = directorypath + '/' + \
                filename + '/' + songnames[i] + '.mp3'

            mp3 = MP3(currentsongpath, ID3=EasyID3)
            if mp3.tags is None:
                mp3.add_tags()
                mp3.save()
            audio = ID3(currentsongpath)
            with open(path2, 'rb') as albimart:
                audio['APIC'] = APIC(
                    encoding=3, mime='image/png', type=3, desc=u'Cover', data=albimart.read()
                )
            audio.save()

            audio = EasyID3(currentsongpath)
            audio["title"] = titlecase(songnames[i])
            audio["album"] = titlecase(nameauthor[0])
            audio["albumartist"] = titlecase(nameauthor[1])
            audio["tracknumber"] = str(i + 1)

            audio["artist"] = titlecase(nameauthor[1])
            audio.save(v2_version=3)
    Tk().withdraw()
    messagebox.showinfo(title='Done!', message=titlecase(
        "All albums have been successfully downloaded!"))


if __name__ == '__main__':
    mainscript()
