'''

MIT License

Copyright (c) 2017 Harshad Sathaye

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''
import os.path

def check_requirments():
    print "\n\n======== REQUIREMENTS STATUS ========\n"
    chk = []
    req = ['Qbittorrent', 'Qbittorrent python wrapper', 'Requests']
    if os.path.isfile("C:\Program Files (x86)\qBittorrent\qbittorrent.exe"):
        print "1. "+req[0]+" - OK"
        chk.append('1')
    elif os.path.isfile("C:\Program Files\qBittorrent\qbittorrent.exe"):
        print "1. "+req[0]+" - OK"
        chk.append('1')

    else:
        print "1. "+req[0]+" - NOT INSTALLED"
        chk.append('0')

    import_list = ['qbittorrent', 'requests']

    i1 = 2
    j1 = 1
    for item in import_list:
        try:
            __import__(item, globals=globals())
            print req[j1]+" - OK"
            chk.append('1')
            i1 += 1
        except ImportError:
            print req[j1]+" - NOT INSTALLED"
            chk.append('0')
        j1 += 1
    if chk[1] == '0' or chk[2] == '0':
        print "Install pip from here - https://pip.pypa.io/en/stable/installing/"

    if chk[0] == '0':
        print "Download and install qbittorrent and make sure web UI is running on port 8080"
    if chk[1] == '0':
        print "Install pip and run 'pip install python-qbittorrent'"
    if chk[2] == '0':
        print "Install pip and run 'pip install requests'"

    if chk[0] == '0' or chk[1] == '0' or chk[2] == '0':
        return False
    else:
        return True


def get_magnet_link(url):
    req = requests.get(url)

    print req.status_code

    if "No results were returned." in req.content:
        print "1"
    else:
        data = req.content.split("<table class=\"table-list table table-responsive table-striped\">")[1]

        data = data.split("<tbody>")[1]

        data = data.split("</table>")[0]

        data = data.split("<a href=")[2]

        page = "https://1337x.to" + data.split(">")[0].split("\"")[1]

        req = requests.get(page)

        magnet_link = req.content.split("magnet\" href=\"")[1].split("\" ")[0]

        print "Magnet link found. Initiating Download"

        return magnet_link

# ============= MAIN FUNCTION =============== #


print "Lets fetch some torrents.."
ch = raw_input("Before that lets check some prerequisites- \n1.Qbittorrent (GUI)\n2.Qbittorrent python-wrapper\n3.Requests package (Y/N)")

if ch == "Y" or ch == "y":
    if check_requirments():
        print "All requirements satisfied- :)"

    else:
        print "Unmet requirements. Exiting the program. Please fulfill the requirements."
        exit()
else:
    print "Skipping requirements check"
    print "Please do not complain if anything breaks..."

from qbittorrent import Client
import requests

name = raw_input("Enter name of the web series:- ")
season = raw_input("Enter season number:- (For multiple seasons use ',') ")
episode = raw_input("Enter a range of episodes (eg. 1-10): ")

print "\n*** By default I will download the torrent with maximum seeds ***"

print "Please confirm your order:- "
print "Web series "+name+"\nSeason "+season+"\nEpisode range "+episode
ch = raw_input("\nIs your order correct ? (Y/N) : ")

if ch == "Y" or ch == "y":
    pass
else:
    print "Please re-order"
    exit()

season_list = season.split(",")
name = name.replace(" ","+")
episodes_range = episode.split("-")
no = 0

qb = Client('http://127.0.0.1:8080')
qb.login('admin','adminadmin')

for i in season_list:
    print i

    s_name = "s"+str(i).zfill(2)

    for j in xrange(int(episodes_range[0]), int(episodes_range[1])+1):
        e = "e"+str(j).zfill(2)
        url = "https://1337x.to/search/"+name+"+"+s_name+e+"/1/"
        print "\n"+url
        no += 1

        status = link = get_magnet_link(url)

        if status != "1":
            print "Link "+str(no) + ":" + link
            qb.download_from_link(link)
            print "Download started.."
        else:
            print "Episode not found. Skipping to next episode"
    s_name = ""
