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

f = open("C:\\Users\\nine4\\Desktop\\code\\AOC_KEY")
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

DAY = 2
PART = 2
s = get_input(DAY).strip() # the daily input is stored in s

'''
Your code here
Put the result in `ans` as a str or int.
'''

def TestReport(report):
    sorted_report = sorted(report)
    if report == sorted_report or report == sorted_report[::-1]:
        for i in range(1, len(report)):
            if abs(report[i] - report[i - 1]) > 3 or report[i] == report[i - 1]:
                return False
        return True
    return False

def TestReportRemoving1(report):
    sorted_report = sorted(report)
    if report == sorted_report or report == sorted_report[::-1]:
        for i in range(1, len(report)):
            if abs(report[i] - report[i - 1]) > 3 or report[i] == report[i - 1]:
                report_removed_i = report[:i] + report[i + 1 :]
                report_removed_i_1 = report[: i - 1] + report[i:]
                return TestReport(report_removed_i) or TestReport(report_removed_i_1)
        return True
    else:
        for i in range(0, len(report)):
            report_removed_i = report[:i] + report[i + 1 :]
            if TestReport(report_removed_i):
                return True

    return False
                
input = s.split("\n")

reports = [list(map(int, report.split())) for report in input]
ans = sum([TestReportRemoving1(report) for report in reports])

#print(ans)

submit(DAY, PART, ans)