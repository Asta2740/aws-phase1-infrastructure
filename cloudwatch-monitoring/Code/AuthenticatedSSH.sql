fields @timestamp, @message 
| parse @message /(?<ip>\d+\.\d+\.\d+\.\d+)/ 
| filter @message like /Accepted/  or @message like  "Success"
| sort @timestamp desc