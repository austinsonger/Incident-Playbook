# Alarms


## Match Alarm
- An Alarm is generated for each match.

## Threshold Alarm
- Build a watchlist with one or more fields
- For each matching event, add a record to the watchlist
- For each record changed, count the total number of matching records
- Alarms when Threshold exceeds a specified value
- Watchlist records are removed based on time since creation

## Blacklist Alarm
- Manually add records to a watchlist of one or more fields
- For each matching event, compare to existing records
- Alarm if matching event matches all the fields of any record
 
## Whitelist Alarm
- Manually add records to a watchlist of one or more fields
- For each matching event, compare to existing records
- Alarm if matching event does NOT match all the fields of any record

## Rolling Whitelist Alarm

(AKA sliding window)

- Build a watchlist with one or more fields, including a counter field
- For each matching event, add a record to the watchlist or increment the counter of the matching record
- Alarm when a new entry is observed (counter value == 1)
- Alarm when a counter exceeds a specified threshold
- Watchlist entries are removed based on age of last edited time

## Deviation from Baseline Alarm
- Build watchlist with one or more fields, including a numeric 'baseline' field
- For each matching event, add a record to the watchlist and calculate the average of all records' baseline value
- Matching events have their selected numeric field compared with the average baseline value
- Alarm if percentage of difference between matched event and baseline average exceeds a set value or percentage
- Watchlist records are removed based on time since creation

## Time of Day Alarm
- Build a watchlist of one or more fields, including start time of day and end time of day
- For each matching event, determine if time of event falls between matching records' start time of day and end time of day
- Alarm if event time is not within start and stop times

## Day of Week Alarm
- Build a watchlist of one or more fields, including one for each day of week
- For each matching event, determine if matching record's matching day of week field is FALSE
- Alarm if matching record's day of week field is FALSE

## Group of Alarms
- For matching alarm event, store in a watchlist
- For next matching alarm event, compare to watchlist for matches in one or more properties.
- Alarm if match is found

## Levenshtein Score Alarm

(AKA Edit Distance; AKA Similarity Score)

https://en.wikipedia.org/wiki/Levenshtein_distance

A score of 0 means both strings are equal.

- Build a watchlist of words to match against
- For each matching event, calculate levenshtein score of selected field value against each entry in watchlist
- Alarm if any score falls below a given threshold

## Shannon Entropy Score Alarm

(AKA Frequency Score; AKA randomness score)

https://en.wikipedia.org/wiki/Entropy_(information_theory)

A higher score means the string has a higher level of randomness.

- For each matching event, calculate Shannon Entropy Score of selected field value
- Alarm if any score falls below a given threshold

- Calculating the randomness of strings and Alarming when the score exceeds a given threshold.


## Alarm Controls

### Mute
- Silence identical alarms for X time period

### Aggregation
- Group identical alarms when X or more fire in Y time period

# Visualizations

## Aggregate Count

(AKA Stack Count; AKA Long Tail Analysis)

- Aggregating on specific fields and showing the total count of each set. Presented in the form of a table, bar chart, or pie chart and visually monitored.
