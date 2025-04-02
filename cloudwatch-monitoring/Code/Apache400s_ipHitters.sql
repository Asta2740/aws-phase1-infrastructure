fields @timestamp, @message, @logStream, @log
    | parse @message /^(?<ip>\S+) \S+ \S+ \[(?<logTime>[^\]]+)] "(?<method>\S+) (?<url>\S+) (?<protocol>\S+)" (?<status>\d{3}) (?<bytes>\d+) "(?<referrer>[^"]*)" "(?<agent>[^"]*)"/
    | filter status >= 400 and status <= 410
    | stats count(*) as ctr by ip
    | filter ctr > 5