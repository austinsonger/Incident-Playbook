## Design Overview

Beagle's graph models are at the **host level**. Nodes are created for things like processes, files and network connections. Nodes are not _currently_ created for interhost communications (i.e, there will not be a `Computer -(RDP)-> Computer` edge), but graphs from two different hosts can be overlapped using `networkx`.

Host artifacts are mapped to classes which implement the `DataSource`, which yield events one by one from the artifact.

`Transformer` classes take the events from the data source and transform them into `Node` objects.

Finally, `Node` objects are sent to the desired storage location via a choice of `Backend` class.

## Features

The following is an overview of supported datasources and backends.

### Node Types

The following is a list of currently support Node Types

| Node Type   |
| ----------- |
| Alert       |
| Domain      |
| File        |
| IPAddress   |
| Process     |
| RegistryKey |
| URI         |

`Alert` nodes represent alerts identified in the logs (if they are available). Including these nodes allows the web interface to drop analysts into the context of the alert as soon as they generate the graph.

`URI` nodes represent the URI of an HTTP request. For example, `GET foobar.com/foo` would result in the following nodes; `Domain(foobar.com), URI(/foo)`.

### Edge Types

| Edge          | Source Type | Dest Type   | Description                                                                               |
| ------------- | ----------- | ----------- | ----------------------------------------------------------------------------------------- |
| Launched      | Process     | Process     | Process launching                                                                         |
| URIOf         | URI         | Domain      | URI of a domain                                                                           |
| ResolvesTo    | Domain      | IP Address  | Domain resolves to a domain                                                               |
| FileOf        | File        | Process     | The file which a process image belongs to                                                 |
| CopiedTo      | File        | File        | Edge representing a file was copied to another destination                                |
| Wrote         | Process     | File        | A process wrote to this file                                                              |
| Accessed      | Process     | File        | A process accessed/read from this file                                                    |
| Deleted       | Process     | File        | A process deleted this file                                                               |
| Copied        | Process     | File        | A process copied this file (the copied file will have a `CopiedTo` edge to the dest file) |
| Loaded        | Process     | File        | A process loaded a function from this file.                                               |
| ConnectedTo   | Process     | IPAddress   | A process initiated a network connection to this address                                   |
| HTTPRequestTo | Process     | URI         | A process made a HTTP Request to this URI                                                 |
| DNSQueryFor   | Process     | Domain      | A process performed a DNS request for this domain.                                        |
| ChangedValue  | Process     | RegistryKey | A process changed the value of this registry key                                          |
| CreatedKey    | Process     | RegistryKey | A process created this registry key                                                       |
| ReadKey       | Process     | RegistryKey | A process read the value of this registry key                                             |
| DeletedValue  | Process     | RegistryKey | A process deleted the value of this registry key                                          |
| DeletedKey    | Process     | RegistryKey | A process deleted this registry key                                                       |
| AlertedOn     | Process     | Node        | An alert was triggered on this node (destination can be any node type)                    |

### Data Sources

The following table lists all of the currently supported data sources. They all are automatically available in the web interface, or they can be imported from the `beagle.datasource` module.

| DataSource          | Description                                                                                                       |
| ------------------- | ----------------------------------------------------------------------------------------------------------------- |
| HXTriage            | FireEye HX triage files (`.mans`)                                                                                 |
| SysmonEVTX          | Sysmon event logs                                                                                                 |
| GenericVTSandbox    | Virustotal v3 API sandbox logs                                                                                    |
| WinEVTX             | Windows event logs                                                                                                |
| GenericVTSandboxAPI | Virustotal v3 API sandbox logs (accepts a hash rather <br/> than file and pulls via the api if a key is available |
| WindowsMemory       | Raw windows memory images (Parsed using Rekall)                                                                   |
| ProcmonCSV          | A procmon run file, exported to CSV                                                                               |
| CuckooSandboxReport | Cuckoo Sandbox Reports												  |
| FireEyeAXReport     | FireEye AX Reports												  |
### Transformers

Transformers take the events provided by the above data sources and convert them into `Node` objects.

Each datasource has an array of supported transformer with at least one transformer defined, which can be accessed via the `.transformers` attribute. Choosing a transformer which is not marked by the data source as compatible will most likely lead to errors or incorrect output

| Transformer          | Description                                                                                                             |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| FireEyeHXTransformer | A transformer meant for FireEye HX Triages                                                                              |
| SysmonTransformer    | A transformer for SysMon logs                                                                                           |
| GenericTransformer   | A generic transformer for datasources which output events that leverage the fieldnames in `beagle.constants.FieldNames` |
| WinEVTXTransformer   | A transformer for windows event logs                                                                                    |
| ProcmonTransformer   | A transformer for procmon events                                                                                        |
| FireEyeAXTransformer | A transformer for FireEye AX events											 |

### Backends

Backends are where the generated data will live.

| Backend    | Description                                                      |
| ---------- | ---------------------------------------------------------------- |
| NetworkX   | Runs on NetworkX, `DiGraph` object available via `.G` attributes |
| DGraph     | Sends data to a [DGraph](https://dgraph.io) server               |
| Neo4J      | Sends data to a [Neo4J](https://neo4j.com) server                |
| Graphistry | Sends data to a [Graphistry](https://graphistry.com) graph       |

Using the web interface will automatically use the `NetworkX` backend and make JSON versions of the graphs available via the web interface.
