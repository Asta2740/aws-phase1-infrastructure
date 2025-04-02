fields @timestamp, @message, @logStream, @log 
| parse @message /^(?<ip>\S+) \S+ \S+ \[(?<logTime>[^\]]+)] "(?<method>\S+) (?<url>\S+) (?<protocol>\S+)" (?<status>\d{3}) (?<bytes>\d+) "(?<referrer>[^"]*)" "(?<agent>[^"]*)"/ 
| filter status >= 200 and status <= 210 
| stats count(*) by bin(5m), @timestamp, method, url, ip, status