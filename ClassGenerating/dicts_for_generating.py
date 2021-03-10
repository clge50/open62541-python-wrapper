# ++++++++++++++++++++++++++ enums ++++++++++++++++++++++++++++++++++
value_backend = ("UA_ValueBackendType",
                 {
                     "UA_VALUEBACKENDTYPE_NONE": 0,
                     "UA_VALUEBACKENDTYPE_INTERNAL": 1,
                     "UA_VALUEBACKENDTYPE_DATA_SOURCE_CALLBACK": 2,
                     "UA_VALUEBACKENDTYPE_EXTERNAL": 3
                 })

log_category = ("UA_LogCategory",
                {
                    "UA_LOGCATEGORY_NETWORK": 0,
                    "UA_LOGCATEGORY_SECURECHANNEL": 1,
                    "UA_LOGCATEGORY_SESSION": 2,
                    "UA_LOGCATEGORY_SERVER": 3,
                    "UA_LOGCATEGORY_CLIENT": 4,
                    "UA_LOGCATEGORY_USERLAND": 5,
                    "UA_LOGCATEGORY_SECURITYPOLICY": 6
                })

log_level = ("UA_LogLevel",
             {
                 "UA_LOGLEVEL_TRACE": 0,
                 "UA_LOGLEVEL_DEBUG": 1,
                 "UA_LOGLEVEL_INFO": 2,
                 "UA_LOGLEVEL_WARNING": 3,
                 "UA_LOGLEVEL_ERROR": 4,
                 "UA_LOGLEVEL_FATAL": 5
             })

# ++++++++++++++++++++++++++ structs +++++++++++++++++++++++++++++++++
