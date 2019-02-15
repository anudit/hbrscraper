import requests
import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm

class PB(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def downloadFile(fn, url, output_path):
    with PB(unit='B', unit_scale=True,miniters=1, desc=fn) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

print("Finding Available Editions ...");
urlList = []
# Generate a list of urls to download files from
r = requests.get('http://usamagazinefree.com/?s=Harvard+Business+Review')
soup = BeautifulSoup(r.content, 'html.parser')
h2List = soup.find_all("h2", class_="search-entry-header-title entry-title")
for h2 in h2List:
    a = h2.find_all("a");
    urlList.append(a[0]['href']);

print("Preparing to Download ...");
pdfList = []
pdfListNames = []
# Generate a list of files to download
for url in urlList:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    fileDiv = soup.find_all("div", class_="vk-att-item")
    for div in fileDiv:
        aList = div.find_all("a")
        for a in aList:
            # Bypass Hotlinking Protection
            temp = a['href'][33:]
            pdfList.append(temp)
            pdfListNames.append(a.text)

print("Downloading Files ...");
for index in range(len(pdfList)):
    #print(pdfListNames[index] + " : " +  pdfList[index] + "\n")
    downloadFile(pdfListNames[index], pdfList[index], pdfListNames[index])