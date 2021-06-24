# Configuration

All configuration entries can be modified by setting environment variables that follow the following format (double underscores):

```
BEAGLE__{SECTION}__{KEY}
```

For example, setting the log level can be done via `BEAGLE__GENERAL__LOG_LEVEL=WARN`

Each section below represents a single entry in the configuration file:

### `general`

-   `log_level` : Logging level, can be one of `INFO`, `DEBUG`, `WARNING`, `ERROR`, `TRACE`, `CRITICAL`.
    -   Default value is `INFO`

### `neo4j`

-   `host`: The neo4j hostname, including protocol.
    -   For example `bolt://localhost:7687`
-   `username`: Username to authenticate with
-   `password`: Password for the username
-   `batch_size`: Number of items to send to Neo4J at once using UNWIND queries.
    -   Default value is `1000`

### `dgraph`

-   `host`: DGraph host URL
    -   For example, `localhost:9080`
-   `batch_size`: Number of nodes to submit at a time
    -   Default value is `1000`

### `virustotal`

-   `api_key`: The VirusTotal API Key to use for fetching data from virustotal

### `splunk`

-   `host`: The IP or FQDN of the Splunk server (no `https://`)
-   `port`: The port of `splunkd` (usually this is 8089)
-   `username`: The username of the user to run searches under
-   `password` The password of the user to run searches under
