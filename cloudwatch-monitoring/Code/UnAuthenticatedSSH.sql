fields @timestamp, @message
| parse @message /(?<ip>\d+\.\d+\.\d+\.\d+)/ 
| filter @message like "No supported authentication" or @message like "UnAuthorized" or @message like "invalid user" or @message like "AuthorizedKeysCommand"
| sort @timestamp desc