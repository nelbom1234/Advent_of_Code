'''
Advent of Code automation template - @MathisHammel
This template provides functions to download inputs and submit answers on AoC.
You need to paste your adventofcode.com session cookie below.
If you don't know how to get this cookie, here's a quick tutorial:
- Open your browser and go to adventofcode.com, make sure you are logged in
- Open the developer console (Ctrl+Shift+I on Firefox/Chrome)
- Get the value of your session cookie:
      - Chrome : 'Application' tab > Cookies
      - Firefox : 'Storage' tab > Cookies
- The cookie is a string of 96 hexadecimal characters, paste it in the AOC_COOKIE below.
Your cookie is similar to a password, >>> DO NOT SHARE/PUBLISH IT <<<
If you intend to share your solutions, store it in an env variable or a file.
'''

import requests
import math

f = open("../../AOC_KEY")
AOC_COOKIE = f.read()
YEAR = '2024'

def get_input(day):
    req = requests.get(f'https://adventofcode.com/{YEAR}/day/{day}/input', 
                       headers={'cookie':'session='+AOC_COOKIE})
    return req.text

def get_example(day,offset=0):
    req = requests.get(f'https://adventofcode.com/{YEAR}/day/{day}',
                       headers={'cookie':'session='+AOC_COOKIE})
    return req.text.split('<pre><code>')[offset+1].split('</code></pre>')[0]

def submit(day, level, answer):
    print(f'You are about to submit the follwing answer:')
    print(f'>>>>>>>>>>>>>>>>> {answer}')
    input('Press enter to continue or Ctrl+C to abort.')
    data = {
      'level': str(level),
      'answer': str(answer)
    }

    response = requests.post(f'https://adventofcode.com/{YEAR}/day/{day}/answer',
                             headers={'cookie':'session='+AOC_COOKIE}, data=data)
    if 'You gave an answer too recently' in response.text:
        # You will get this if you submitted a wrong answer less than 60s ago.
        print('VERDICT : TOO MANY REQUESTS')
    elif 'not the right answer' in response.text:
        if 'too low' in response.text:
            print('VERDICT : WRONG (TOO LOW)')
        elif 'too high' in response.text:
            print('VERDICT : WRONG (TOO HIGH)')
        else:
            print('VERDICT : WRONG (UNKNOWN)')
    elif 'seem to be solving the right level.' in response.text:
        # You will get this if you submit on a level you already solved.
        # Usually happens when you forget to switch from `PART = 1` to `PART = 2`
        print('VERDICT : ALREADY SOLVED')
    else:
        print('VERDICT : OK !')

DAY = 5
PART = 2
s = get_input(DAY).strip() # the daily input is stored in s

'''
Your code here
Put the result in `ans` as a str or int.
'''

a = s.split("\n\n")

rules = a[0].split("\n")
updates = a[1].split("\n")

ans = 0

for update in updates:
    correct = True
    updateList = update.split(",")
    i = 1
    while i < len(updateList):
        for j in range(i-1,-1,-1):
            rule = str(updateList[i]) + "|" + str(updateList[j])
            if rule in rules:
                correct = False
                tmp = updateList[i]
                updateList[i] = updateList[j]
                updateList[j] = tmp
                i = 1
                break
        i += 1
    if not correct:
        middle = int(updateList[math.floor(len(updateList)/2)])
        ans += middle

print(ans)

submit(DAY, PART, ans)