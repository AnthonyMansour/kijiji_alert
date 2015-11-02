__author__ = 'Anthony Mansour'
import urllib.request
import smtplib
import getpass
from time import asctime, sleep


def find_between(s, first, last):   # Returns substring with in 's' using 'first' and 'last' as string bounds
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

print('script started @ ' + asctime())
url = input('Enter Kijiji url (default: http://www.kijiji.ca/b-art-collectibles/banff-canmore/c12l1700234): ' + '\n')

if len(url) > 23:   # Checks if url is from kijiji.ca
    if url[:21] != "http://www.kijiji.ca/":
        url = 'http://www.kijiji.ca/b-art-collectibles/banff-canmore/c12l1700234'
else:
    url = 'http://www.kijiji.ca/b-art-collectibles/banff-canmore/c12l1700234'

print("Current url: " + url + '\n')

req = urllib.request.Request(url)
sender = input('Enter sender email (Currently @gmail.com only): ' + '\n')
password = getpass.getpass()
receiver = input('\n' + 'Enter phone number (Currently Telus/Koodo Only): ' + '\n') + '@msg.telus.com'

ad_start = '<table class=" regular-ad js-hover "'
image_start = '<img src="'
image_end = '"'
link_start = '<a href="'
link_end = '"'
title_start = '-flag" >'
title_end = '</a>'
description_start = '<p>'
description_end = '</p>'
price_start = 'price">'
price_end = '</td>'
sub_bottom = '<div id="AdsenseBottom"'

server = smtplib.SMTP("smtp.gmail.com:587")
loop = True
open('ads.txt', 'a+').close()

while loop:
    file_string = ''
    with urllib.request.urlopen(req) as response:
        page = response.read().decode(response.headers.get_content_charset())

    front_page_ads = page.count(ad_start)
    page_sub = page.replace('\n', '').replace('\r', '')
    response.close()
    page_sub = find_between(page_sub, ad_start, sub_bottom)

    ads = []
    for x in range(0, front_page_ads):
        ads.append([])
        ads[x].append(find_between(page_sub, title_start, title_end).strip(' \t\n\r'))
        ads[x].append('http://www.kijiji.ca' + find_between(page_sub, link_start, link_end).strip(' \t\n\r'))
        ads[x].append(find_between(page_sub, description_start, description_end).strip(' \t\n\r'))
        ads[x].append(find_between(page_sub, image_start, image_end).strip(' \t\n\r'))
        ads[x].append(find_between(page_sub, price_start, price_end).strip(' \t\n\r'))
        page_sub = page_sub[page_sub.index(price_end, page_sub.index(price_start) + len(price_start)) + 4:]


    for i in range(0, front_page_ads):
        for j in range(0, 4):
            file_string += ads[i][j] + ' , '
        file_string += '\n'

    f = open('ads.txt', 'r+')

    if f.read() != file_string.strip():
        f.seek(0)
        f.truncate()
        f.write(file_string.strip())
        msg = "\r\n".join([
            " ",
            ads[0][0],
            ads[0][1],
            ads[0][2],
            ads[0][3],
            ads[0][4]
        ])
        try:
            server.connect('smtp.gmail.com', '587')
            server.ehlo()
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, msg)
            server.quit()
            print('Update sent @ ' + asctime())
        except:
            print('ERROR, FAILED TO SEND SMTP! @ ' + asctime())
            loop = False
    f.close()
    sleep(5)
print('Exited')
