Background
===

When an mCent user installs an app and tries it, the app has a mobile
attribution tracking SDK that makes a call to a 3rd party attribution
platform.  In turn, this attribution platform makes a call to the mCent
servers so we can acknowledge the install, and reimburse our members.

We are trying to troubleshoot a discrepancy with the attribution
platform. Our account managers want to know how many callbacks we
received from our partner, and how many we received for a specific
campaign.

Callbacks to our system have the following URL structure:

`/aff/callback/<partner_id>?<campaign_attributes>`

Questions
===

For each problem, please provide an answer, and any scripts/commands
that you used to get to the answer.  For the scripts, please check them
in to a public github repo with a codename that does not have
Jana in the name. *Please do not fork the repo.*

Access logs are provided in `elblogs.txt`. Download the repo from
GitHub (do not fork the repo) and then create a new repo with your
submission.

1) How many callbacks did we receive for partner id `nyr8nx`.

**Running** `cat elblogs.txt | grep /aff/callback/ | grep nyr8nx | wc -l` **returns 96 callbacks**

2) How many callbacks did we receive for partner `nyr8nx` for campaign id
(cid) `X9KN0`

**Running** `cat elblogs.txt | grep /aff/callback/ | grep nyr8nx | wc -l` **returns 27 callbacks**

3) Write a python script that analyzes `elblogs.txt` and counts all
API requests (requests starting with `api/`).  Print them out in
descending frequency.

**Attached is the Python script which finds 149698 Total API Calls**

**The script also has a --mode option to look for Callbacks instead of API Calls**

**When running in CALL mode, PID and CID can be set to narrow down the results**

**Run** `python log-parser.py -h` **for assistence**

On each line, print the percentage of requests this api request represented
(to 2 decimal points of precision), the number of total requests made to this
endpoint, and the api url path.  Finally, print the total number of api
requests made in this period.

Example output:

```
50.00%  50  api/v1/track_offer_views
20.00%  20  api/v1/match_member_check
15.00%  15  api/v1/profile/forgot_password
10.00%  10  api/v1/member_id
5.00%   5   api/v1/contacts/add_email
100 Total api requests
```
