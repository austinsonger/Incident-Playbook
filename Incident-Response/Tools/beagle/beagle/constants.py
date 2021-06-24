class Protocols:
    HTTP = "HTTP"
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"


class HashAlgos:
    SHA256 = "sha256"
    MD5 = "md5"
    SHA1 = "sha1"


class HTTPMethods:
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"


class EventTypes:
    PROCESS_LAUNCHED = "process_launched"
    FILE_DELETED = "file_deleted"
    FILE_OPENED = "file_opened"
    FILE_WRITTEN = "file_written"
    FILE_COPIED = "file_copied"
    REG_KEY_OPENED = "reg_key_opened"
    REG_KEY_DELETED = "reg_key_deleted"
    REG_KEY_SET = "reg_key_set"
    LOADED_MODULE = "loaded_module"
    HTTP_REQUEST = "http_request"
    CONNECTION = "connection"
    DNS_LOOKUP = "dns_lookup"


class FieldNames:

    # General FieldNames
    TIMESTAMP = "timestamp"
    EVENT_TYPE = "event_type"

    # Process FieldNames
    PROCESS_IMAGE = "process_image"
    PROCESS_IMAGE_PATH = "process_image_path"
    PROCESS_ID = "process_id"
    COMMAND_LINE = "command_line"

    # Parent Process FieldNames
    PARENT_PROCESS_IMAGE = "parent_process_image"
    PARENT_PROCESS_IMAGE_PATH = "parent_process_image_path"
    PARENT_PROCESS_ID = "parent_process_id"
    PARENT_COMMAND_LINE = "parent_command_line"

    # File FieldNames
    FILE_NAME = "file_name"
    FILE_PATH = "file_path"
    HASHES = "hashes"

    # Copied/Moved/Renamed File Events
    SRC_FILE = "src_file"
    DEST_FILE = "dst_file"

    # HTTP Fields
    HTTP_METHOD = "http_method"
    HTTP_HOST = "http_host"
    URI = "uri"

    # IP Address fields
    IP_ADDRESS = "ip_address"
    PORT = "port"
    PROTOCOL = "protocol"

    # Registry
    HIVE = "hive"
    REG_KEY = "reg_key"
    REG_KEY_VALUE = "reg_key_value"
    REG_KEY_PATH = "reg_path"

    # Alerts
    ALERTED_ON = "alerted_on"
    ALERT_NAME = "alert_name"
    ALERT_DATA = "alert_data"
