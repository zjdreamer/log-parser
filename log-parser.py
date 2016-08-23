#################################################
#################################################
#################log-parser.py###################
#################################################
#################################################


#!/usr/bin/python
import argparse



parser = argparse.ArgumentParser(description='Parse a logfile for either API, or CALLback information')
parser.add_argument('log', help='the logfile to be parsed')
parser.add_argument('-m', '--mode', choices=['API', 'CALL'], default='API', help='the mode to run the parser in, accepts API and CALL (Default: API)')
parser.add_argument('--pid', help='the partner ID to search for callbacks from.')
parser.add_argument('--cid', help='the campaign ID to search for callbacks from.')

args = parser.parse_args()

def apiParse(log):
    
    try:
        logFile = open(log, "r")
    
        api_calls = {} #define empty dictionary

        for line in logFile: #loop through line by line
        
            index = line.find("api/")
        
            if(index > -1):
            
                api = line[index:]
                
                api = api.replace('"', '') #strip any rogue quotes, needed for partition to not break

                api = api.partition(' ')[0] #split on the first space, should strip everything except the api call
                
                #if api is mapped, add one, otherwise map it
                if api in api_calls:
                    api_calls[api] += 1
                else:
                    api_calls[api] = 1
        logFile.close()
        
        total_api_calls = sum(api_calls.values())
        numDig = len(str(max(api_calls.values())))

        for apis, totals in sorted(api_calls.iteritems(), reverse=True, key=lambda(k,v): (v,k)):
            percent = totals/float(total_api_calls) #float in the denom forces the whole thing to eval as a float
            percent *= 100

            apiOut = "{0:,.2f}".format(percent) #format percent to 2 decimal places
            
            #add three spaces if the current percent is under 10%, for formatting reasons
            if(percent < 10):
                apiOut += "%   "
            else:
                apiOut += "%  "

            apiOut +=  str(totals)
            
            curNumDig = len(str(totals)) #convert totals to a string and then get the number of digits
            
            #add N spaces where N is the difference between the number of digits in the current value vs the max value
            for i in range(curNumDig, numDig):
                apiOut += " "
            #add one space as the default, then append the current API
            apiOut += " " + apis
            
            print apiOut
        print str(total_api_calls) + " Total API Calls"
    
    except IOError as err:
        print('Error opening logfile: '.format(err))

def callParse(log):
     
    try:
        logFile = open(log, "r")
        
        count = 0
        pid = "/" + str(args.pid) + "?"
        cid = "cid=" + str(args.cid)

        for line in logFile.xreadlines():
        
            index = line.find("/aff/callback/")
        
            if(index > -1):
                
                #check the flags and keep a count based on the given paramaters
                if args.pid is not None and args.cid is not None:
                    if(line.find(pid) > -1 and line.find(cid) > -1):
                        count += 1
                elif args.pid is not None:
                    if(line.find(pid) > -1):
                        count+= 1
                elif args.cid is not None:
                    if(line.find(pid) > -1):
                        count += 1
                else:
                    count +=1
                           
        logFile.close()

        callOut = str(count) + " total callbacks"
        if(args.pid is not None):
            callOut += " Partner ID " + str(args.pid)
        if(args.cid is not None):
            callOut += " Campaign ID " + str(args.cid)
        
        print callOut
    
    except IOError as err:
        print('Error opening logfile: '.format(err))


if(args.mode=='CALL'):
    callParse(args.log)
else:
    apiParse(args.log) #API is the default mode, so no need to check the mode if it's not CALL
