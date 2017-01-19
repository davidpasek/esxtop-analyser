#!/usr/bin/python

file_header                = "esxtop-data.csv"          # all esxtop counters are located in this header (first line)
file_data                  = "esxtop-data.csv"          # comma separated values of esxtop performance data
file_counters_to_analyse   = "" # one esxtop counter per line 
file_counters_to_analyse   = "counters.physical-disks.avg-kernel-latency.conf" # one esxtop counter per line 
print_value_greater_then   = 0                          # print filter for interactive data anlysis
dictionary_header          = {}                         # all counters from the header with field position
array_counters_to_analyse  = []                         # all counters for analysis
array_datalines_to_analyse = []                         # esxtop data lines for analysis

# Read and parse esxtop header
def getEsxTopHeader(filename):
    global dictionary_header
    f = open(filename, 'r')
    string_header = f.readline()
    array_header = string_header.split(",")
    # go through header 
    i = 1
    for item in array_header:
        dictionary_header[item] = i
        i += 1

# Read and parse esxtop data for analysis
def getEsxTopDataForAnalysis(filename):
    global file_header
    global file_data
    global array_datalines_to_analyse
    f = open(filename, 'r')
    i = 1
    for line in f:
        if (file_header == file_data) and (i == 1): # ignore the first line if it is the header
            i += 1
            continue
        parts = line.split(",")
        newline = parts[0]
        for counter in array_counters_to_analyse:
            newline = newline + ',' + parts[dictionary_header[counter]]
        array_datalines_to_analyse.append(newline)
        i += 1

# Analyse data and print it
def analyseData():
    global array_datalines_to_analyse
    pos = 1 # 0 ... date/time, 1 ... first counter, 2 ... second counter, etc.
    for counter in array_counters_to_analyse:
        print '{0:40s} : {1:20s}'.format('Counter',counter)
        i = 0
        average = 0
        for line in array_datalines_to_analyse:
            parts = line.split(",")
            value = parts[pos]
            value = value.lstrip('"')
            value = value.rstrip('"')
            value = float(value)
            if i == 0:
                minimum = value + 0
                minimum_time = ""
                maximum = value + 0
                maximum_time = ""
            i += 1
            if value <= minimum:
                minimum = value
                minimum_time = parts[0]
            if value >= maximum:
                maximum = value
                maximum_time = parts[0]
            average += value
        average = average / i 
        if minimum >= print_value_greater_then or average >= print_value_greater_then or maximum >= print_value_greater_then:
            print '{0:40s} : {1:20s}'.format('Counter',counter)
        if minimum >= print_value_greater_then:
            print '{0:40s} : {1:10.2f} - Time: {2:15s}'.format('  Minimum',minimum,minimum_time)
        if average >= print_value_greater_then:    
            print '{0:40s} : {1:10.2f}'.format('  Average',average)
        if maximum >= print_value_greater_then:
            print '{0:40s} : {1:10.2f} - Time: {2:15s}'.format('  Maximum',maximum,maximum_time)
        pos += 1    

# Read and parse counters for analysis
def getCountersForAnalysis(filename):
    global header_arr
    global array_counters_to_analyse
    try:
        f = open(filename, 'r')
        for line in f:
            counter = line.rstrip('\n');
            array_counters_to_analyse.append(counter)
    except: # catch *all* exceptions
        print "Cannot read counters for analysis"

# Print esxtop header
def printEsxTopHeader():
    for item in dictionary_header:
            print item

# Print esxtop data
def printEsxTopDataForAnalysis():
    print "\"Date-time\",",
    for item in array_counters_to_analyse:
            print item,",",
    print

    for line in array_datalines_to_analyse:
            print line

# Print counters to analyse
def printCountersForAnalyss():
    i = 0
    for counter in array_counters_to_analyse:
        print "Counter: " + str(counter)
        pos = dictionary_header[counter];
        print "Position in original header:" + str(pos)
        print "Position in new header:" + str(i)
        i += 1

# Print esxtop bundle statistics
def printEsxTopBundleStats():
    print '{0:40s} : {1:20d}'.format('Num of counters in header',len(dictionary_header))
    print '{0:40s} : {1:20d}'.format('Num of counters to analyse',len(array_counters_to_analyse))
    print '{0:40s} : {1:20d}'.format('Num of data lines',len(array_datalines_to_analyse))
    # Start time
    line = array_datalines_to_analyse[0]
    parts = line.split(",")
    s = parts[0]
    if s[1:2] == '(': # This is the header therefore get time from next line
        line = array_datalines_to_analyse[1]
        parts = line.split(",")
    print '{0:40s} : {1:20s}'.format('Start time',parts[0])
    # End  time
    line = array_datalines_to_analyse[len(array_datalines_to_analyse)-1]
    parts = line.split(",")
    print '{0:40s} : {1:20s}'.format('End time',parts[0])

# Get EsxTop 
def getEsxTop():
    global file_header
    global file_data
    global file_counters_to_analyse
    getEsxTopHeader(file_header)
    getCountersForAnalysis(file_counters_to_analyse)
    getEsxTopDataForAnalysis(file_data)

# MAIN CODE
print "ESXTOP Analyzer"
print "---------------"
getEsxTop()

#printEsxTopHeader()
#printCountersForAnalysis()
#printEsxTopBundleStats()
printEsxTopDataForAnalysis()
#analyseData()
