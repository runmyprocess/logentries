#Python client for Logentries REST API.

Add conf in $HOME/.logentries as json dict:

{
"API_KEY" = "XXX",
"LOG_DICT" = {
    "my_label": "YYY",
    "my_label2": "ZZZ"
},
}

then call:
logentries my_label my_query
