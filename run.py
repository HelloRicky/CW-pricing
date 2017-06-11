from __future__ import print_function
import schedule
import urllib
import time
import quickstart

url = 'https://api.thingspeak.com/update?api_key=2KGMA91G7WZ3U65U&field1='
count = 0

def postUrl(data):
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    r = urllib.urlopen(url+str(data))
    print(r.getcode(), 'sent:', data)

def job():
    global count
    count += 1
    print('it is time to do job!')
    postUrl(count)
    quickstart.main()      # main function
    return
    
def main():
    schedule.every().day.at("22:40").do(job)
    while True:
        print('working on job...')
        schedule.run_pending()
        time.sleep(20)
    
if __name__ == "__main__":
    main()

