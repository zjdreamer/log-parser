#!/usr/bin/python
import numpy as np
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
    
        api_calls = {}

        for line in logFile.xreadlines():
        
            index = line.find("api/")
        
            if(index > -1):
            
                api = line[index:]
                
                api = api.replace('"', '')

                api = api.partition(' ')[0]
                
                if api in api_calls:
                    api_calls[api] += 1
                else:
                    api_calls[api] = 1
        logFile.close()
        
        total_api_calls = sum(api_calls.values())

        for apis, totals in sorted(api_calls.iteritems(), reverse=True, key=lambda(k,v): (v,k)):
            percent = totals/float(total_api_calls)
            percent *= 100

            print "{0:,.2f}".format(percent) + "%  " + str(totals) + "  " + apis
        print str(total_api_calls) + " Total API Calls"
    
    except IOError as err:
        print('Error opening logfile: '.format(err))

def callParse(log):
     
    try:
        logFile = open(log, "r")
        
        count = 0

        for line in logFile.xreadlines():
        
            index = line.find("/aff/callback/")
        
            if(index > -1):
                
                if args.pid is not None and args.cid is not None:
                    if(line.find(args.pid) > -1 and line.find(args.cid) > -1):
                        count += 1
                elif args.pid is not None:
                    if(line.find(args.pid) > -1):
                        count+= 1
                elif args.cid is not None:
                    if(line.find(args.pid) > -1):
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
    apiParse(args.log)



