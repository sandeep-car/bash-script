#!/usr/local/bin/python3
# Download SPECint results from https://www.spec.org/cgi-bin/osgresults
# Then run this script against it to look for processors you are interested in.
# You can also download the CSV file containing all results to be sure, but it is over 48MB.
# Be sure to:
#1. Change the benchmark if required.
#2. Change hardware vendor (hw).
#3. Change the system.
import re
import csv
import sys
import urllib.request
from pprint import pprint

# Which benchmark result are you interested in?
#benchmark = "CINT2006rate"
benchmark = "CINT2017"
# Hardware vendor.
hw = "Dell Inc."
# System to look for.
system = "R640"
# Test to look for.
test_regex = "^([\d]+)\.gcc(\S+)(\s+)(\d+)(\s+)(\d+)"
# Spec.org's URL. Append txt results to this.
base_url = "http://spec.org/"

# Print usage messages.
def PrintUsage():

    print ("<Usage>:",sys.argv[0],"<File Name>")
    print ("Where <File Name> is the name of the file with specint data.")
    return


if __name__ == "__main__":
    try:
        if (len(sys.argv) != 2):
            PrintUsage()
            sys.exit(1)

        #1. Get the filename as an argument.
        
        csvfile = sys.argv[1]

        #2. Open the file for reading.
        try:
            print("Results for {} from {}".format(system,hw))
            with open(csvfile) as csvfp:
                csv_reader = csv.reader(csvfp, delimiter=',')

                #3. Loop through file and earch for the terms you want. Row looks like:
                # Benchmark,"Hardware Vendor",System,Result,Baseline,"# Cores","# Chips ","# Cores Per Chip ",Published,Disclosures

                sys_info=[]
                index=0
                for row in csv_reader:
                    # Skip empty lines.
                    if (len(row) == 0):
                        continue
                    if (row[0] != benchmark):
                        continue
                    if (row[1] != hw):
                        continue
                    
                    matchObj = re.search(system,row[2])
                    if (matchObj == None):
                        continue
                    full_system = re.sub(r',',';',row[2])
                    # CPU2006 and CPU2017 benchmark results have cores and sockets in different places.
                    if ("2006" in benchmark):
                        num_cores = row[5]
                        num_sockets = row[6]
                    else:
                        num_cores = row[3]
                        num_sockets = row[4]                        
                    # print("MatchObj: ", matchObj)
                    # If we are here then we've found the right server and vendor.
                    # print("Row: ", row)
                    # Now pull up the benchmark results so we can scan them.
                    hrefs = row[len(row)-1]
                    # print("HREFS: ", hrefs)
                    res = re.split("<A HREF=",hrefs)
                    for r in res:
                        # print(r)
                        matchObj = re.search(r'"(\S+)">Text</A>',r)
                        if (matchObj == None):
                            continue
                        text_results = matchObj.group(1)
                        break
                    print("URL: ", base_url + text_results)
                    webUrl = urllib.request.urlopen(base_url + text_results)
                    data = webUrl.read().decode("utf-8")
                    #testfp = open("cpu2017-20190611-15326.txt",'r')
                    #data = testfp.read()
                    #testfp.close()
                    # Now loop over test_results.
                    lines=re.split('\n',data)
                    for l in lines:
                        matchObj = re.match(test_regex,l)
                        if (matchObj == None):
                            continue
                        #print(matchObj.groups())
                        compile_time = matchObj.group(6)
                        break
                    sys_info.insert(index,[full_system,num_cores,num_sockets,compile_time])
                    index=index+1
                    print("\tSystem: {}. Number of Cores: {}. Number of Sockets: {}. Compile_time: {}".format(full_system,num_cores,num_sockets,compile_time))
            sys_info.sort(key=lambda item:item[3])
            for s in sys_info:
                pprint(s)
            sys.exit(0)
                    
        except Exception as ex:
            print(ex)
            sys.exit(1)


    except Exception as ex:
        print(ex)
        sys.exit(1)
