# REST API

Using the docker image exposes a REST API for creating and retrieving graphs. Each section below represents a single API endpoint.

Each data source generates a graph, which is mapped back to a category (two data sources may output to the same category).

-   For example, the `GenericVTSandbox` and `GenericVTSandboxAPI` outputs to the `VT Sandbox` which has an id of `vt_sandbox`. `HXTriage` outputs to the `FireEye HX` category, which has an id of `fireeye_hx`

## REST Endpoints

<!-- @import "[TOC]" {cmd="toc" depthFrom=3 depthTo=3 orderedList=false} -->

<!-- code_chunk_output -->

-   [List Data Sources `/api/datasources`](#list-data-sources-apidatasources)
-   [New Graph `/api/new`](#new-graph-apinew)
-   [Get Graph JSON `/api/graph/<int:graph_id>`](#get-graph-json-apigraphintgraph_id)
-   [Get Graph Metadata `/api/metadata/<int:graph_id>`](#get-graph-metadata-apimetadataintgraph_id)
-   [List Categories `/api/categories`](#list-categories-apicategories)
-   [List Category Entries `/api/categories/<string:category>`](#list-category-entries-apicategoriesstringcategory)

<!-- /code_chunk_output -->

### List Data Sources `/api/datasources`

Returns a list of available datasources, which transformers they work with, as well as which parameters are required to use this datasource. This can be used to identify what values are available to be used with the [new graph](#new-graph) endpoint.

-   **URL**

    `/api/datasources`

-   **Method:**

    `GET`

*   **Success Response:**


    -   **Code:** 200 <br />
        **Output Schema:**
        ```typescript
        {
            "datasources":
                [
                    {
                        "id": string,
                        "name": string,
                        "params": [
                            {
                                "name": string,
                                "required": boolean,
                            }
                            ...
                        ],
                        "transformers": [
                            {
                                "id": string,
                                "name": string
                            }
                        ]
                        "type": "files"|"external"
                    },
                    ...
                ],
            "backends": [
                {"name": string" id": string},
                ...
            ]
        }
        ```

-   **Notes**
    <br/>
    The response JSON of this API call provides an array of all available datasources
    and backends

    The `datasources` array contains the following information:

    -   `id`: This is the python class for this datasource.
    -   `name` : The human-readable version of the name. This is the value which shows up in the dropdown on the upload form.
    -   `params`: A list of parameters that can be passed to this data source. Required parameters have the `required` field set to `True`.
    -   `transformers`: A list of transformers that this data source supports. Each one has the ID and human-readble name of the transformer.
    -   `type`: The type of data source this is:
        -   `files`: Parameters represent files that need to be uploaded
        -   `external`: Parameters represent text input which is used to fetch data by the data source class.

    For example:
    <br />

    ```json
    {
        "id": "HXTriage",
        "name": "FireEye HX Triage",
        "params": [
            {
                "name": "triage",
                "required": true
            }
        ],
        "transformers": [
            {
                "id": "FireEyeHXTransformer",
                "name": "FireEye HX"
            }
        ],
        "type": "files"
    }
    ```

    In the above, the `HXTriage` data source requires one file based parameter called `triage`, and the data it yields can be transformed into nodes via the `FireEye HX` transformer class.

    The `backends` key simply contains key/value names of the various datasource classes. For example:
    <br/>

    ```json
    { "name": "Neo4J", "id": "Neo4J" }
    ```

-   **Sample Output:**

    ```json
    {
        "datasources": [
            {
                "id": "GenericVTSandbox",
                "name": "VirusTotal v3 API Sandbox Report Files",
                "params": [
                    {
                        "name": "behaviour_report_file",
                        "required": true
                    },
                    {
                        "name": "hash_metadata_file",
                        "required": false
                    }
                ],
                "transformers": [
                    {
                        "id": "GenericTransformer",
                        "name": "Generic"
                    }
                ],
                "type": "files"
            },
            {
                "id": "HXTriage",
                "name": "FireEye HX Triage",
                "params": [
                    {
                        "name": "triage",
                        "required": true
                    }
                ],
                "transformers": [
                    {
                        "id": "FireEyeHXTransformer",
                        "name": "FireEye HX"
                    }
                ],
                "type": "files"
            }
        ],
        "backends": [{ "name": "NetworkX", "id": "NetworkX" }, { "name": "Neo4J", "id": "Neo4J" }]
    }
    ```

### New Graph `/api/new`

-   **URL**

    `/api/new`

-   **Method:**

    `POST`

-   **Data Params**

    ```typescript
    {
        // Required parameters
        "datasource": string,
        "transformer": string,
        "comment": string,
        // Optionally set the backend, by default uses NetworkX
        "backend": string | undefined

        // Parameters unique to datasource
        "param1": string|file,
        "param2": string|file,
        ...
        "paramX": string|file,
    }
    ```

    Since each different data sources may require a different number of parameters to properly work. This endpoint requires three main parameters, followed by any additional parameters used by that specific datasource.

    -   Required and optional parameters are listed in the `params` key returned in the [`/api/datasources` endpoint](#get-data-sources)

*   **Success Response:**

    If the graph is generated without any errors, the ID of the of the graph is generated, as well as the route to view it in the beagle web interface.

    -   The `self` value represents the URI for viewing the graph using the built-in web interface. The ID can be used for fetching the raw JSON using the `/graph/:id` endpoint.

    <br/>

    -   **Code:** 200 <br />
        **Content:**
        ```typescript
        {
            id : number,
            self: /:category/:id
        }
        ```

-   **Error Response:**

    This endpoint returns 400 if a parameter is missing, or 500 if there was an error. In both cases, the `message` field of the response will return a reason for failure.

    -   **Code:** 400 - Missing parameters <br />
        **Example:** `{ message : "Missing parmaeters: [transformer, datasource]" }`

    -   **Code:** 500 - Unhandled exception in graph process<br />
        **Content:** `{ message : "KeyError at line ...." }`

*   **Sample Call:**


    Creating a graph using the FireEye HX Triage requires a single parameter, `triage`. The data source ID is `HXTriage`, and the supported transformer's ID is `FireEyeHXTransformer`. If our triage is called `incident.mans`, we can create a new triage with the following CURL command.

    ```bash
    curl -F 'triage=@incident.mans' \
        -F 'datasource=HXTriage' \
        -F 'transformer=FireEyeHXTransformer' \
        -F 'comment=Stuxnet Triage' \
        http://localhost:8000/api/new
    ```

    Creating the same triag,e but this time send it to Neo4J
    ```bash
    curl -F 'triage=@incident.mans' \
        -F 'datasource=HXTriage' \
        -F 'transformer=FireEyeHXTransformer' \
        -F 'comment=Stuxnet Triage' \
        -F "backend=Neo4J" \
        http://localhost:8000/api/new
    ```

### Get Graph JSON `/api/graph/<int:graph_id>`

-   **URL**

    `/api/graph/<int:graph_id>`

-   **Method:**

    `GET`

*   **Success Response:**

    Returns a [node link data](https://networkx.github.io/documentation/stable/reference/readwrite/generated/networkx.readwrite.json_graph.node_link_graph.html) formatted representation of the graph.

    <br/>

    -   **Code:** 200 <br />
        **Content:**
        ```typescript
        {
            directed: boolean,
            links: [
                {...}
            ],
            multigraph: boolean,
            nodes: [
                {...}
            ]
        }
        ```

-   **Error Response:**

    This endpoint returns 404 if one does not exist.

    -   **Code:** 404 - Graph not found <br />
        **Example:** `{ message : "Graph not found" }`

*   **Sample Call:**

    ```bash
    curl http://localhost:8000/api/graph/3
    ```

    ```typescript
    {
        "directed": true,
        "links": [
            {
                "id": 6,
                "properties": {
                    "data": [
                        {
                            "timestamp": 1474410459
                        }
                    ]
                },
                "source": 5905145826784592000,
                "target": -6580422346879020000,
                "type": "Launched"
            }
            ...
        ],
        "multigraph": true,
        "nodes": [
            {
                "_color": "#FF0000",
                "_display": "dllhost.exe",
                "_node_type": "Process",
                "id": -6580422346879020000,
                "properties": {
                    "command_line": "C:\\Windows\\system32\\DllHost.exe /Processid:{AB8902B4-09CA-4BB6-B78D-A8F59079A8D5}",
                    "hashes": {},
                    "host": "IE10Win7",
                    "process_id": 3564,
                    "process_image": "dllhost.exe",
                    "process_image_path": "C:\\Windows\\System32",
                    "process_path": "C:\\Windows\\System32\\dllhost.exe",
                    "user": "IE10WIN7$"
                }
            }
            ...
        ]
    }
    ```

    **Note**:
    The output of this call be passed into the networkx `networkx.readwrite.json_graph.node_link_graph` function to get `networkx.Graph` objects.
    <br />

    ```python
    >>> import requests, networkx

    # Use requests to get the data as JSON
    >>> graph_data = requests.get("http://localhost:8000/api/graph/1").json()

    # Parse into a networkx graph
    >>> G = networkx.readwrite.json_graph.node_link_graph(graph_data)

    >>> G
    <networkx.classes.multidigraph.MultiDiGraph object at 0x12aac7128>
    ```

### Get Graph Metadata `/api/metadata/<int:graph_id>`

-   **URL**

    `/api/metadata/<int:graph_id>`

-   **Method:**

    `GET`

*   **Success Response:**

    Returns the metadata dictionary for a graph ID.

    <br/>

    -   **Code:** 200 <br />
        **Content:**
        ```typescript
        {
            ...
        }
        ```

-   **Error Response:**

    This endpoint returns 404 if one does not exist.

    -   **Code:** 404 - Graph not found <br />
        **Example:** `{ message : "Graph not found" }`

*   **Sample Call:**

    ```bash
    curl http://localhost:8000/api/metadata/1
    ```

    ```json
    {
        "malicious": 3,
        "name": "WallpaperHdInstaller.exe",
        "results": [
            {
                "McAfee-GW-Edition": "BehavesLike.Win32.CoinMiner.vc"
            },
            {
                "Paloalto": "generic.ml"
            },
            {
                "TrendMicro-HouseCall": "TROJ_GEN.R002H06BP19"
            }
        ],
        "sandbox_name": "Tencent HABO",
        "sha256": "d9a2ba3e2f149473d1ecf123aa548eecf26115d988265cb0bdaef7f465b10bc2"
    }
    ```

### List Categories `/api/categories`

Returns a list of all categories, their names and ids.

-   **URL**

    `/api/categories`

-   **Method:**

    `GET`

*   **Success Response:**

    -   **Code:** 200 <br />
        **Output Structure**
        ```typescript
        [
            {
                name: string,
                id: string
            }
        ];
        ```
        **Example output:**
        ```typescript
        [
            {
                id: "sysmon",
                name: "SysMon"
            },
            {
                id: "windows_event_logs",
                name: "Windows Event Logs"
            },
            {
                id: "vt_sandbox",
                name: "VT Sandbox"
            },
            {
                id: "windows_memory",
                name: "Windows Memory"
            },
            {
                id: "fireeye_hx",
                name: "FireEye HX"
            }
        ];
        ```

### List Category Entries `/api/categories/<string:category>`

Returns a list of all graphs in the current category, their ids, comments associated with them, and the metadata generated by the datasource for them, as well as the path the JSON graph on disk.

-   **URL**

    `/api/categories/<string:category>`

-   **Method:**

    `GET`

-   **Data Params**

    ```typescript
    [
        {
            comment: string,
            file_path: string,
            id: number,
            metadata: object
        }
    ];
    ```

*   **Success Response:**

    The metadata object changes on a per category basis. The graphs file name is the SHA256 of it's JSON contents.
    <br />

    -   **Code:** 200 <br />
        **Example output:**
        ```typescript
        [
            {
                comment: "PSAttack example logs",
                file_path: "90d90ebb64d60129fa8ed89e1d2ec97aea5957228cf9fd8282c6052718eba7b7.json",
                id: 1,
                metadata: {
                    hostname: "IE10Win7"
                }
            }
            ...
        ];
        ```
