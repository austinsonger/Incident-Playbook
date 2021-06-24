# Development

Development primarily involves creating a datasource and transformer. For backend creation, see the existing `Neo4J` and `DGraph` classes for how to leverage `NetworkX` to transform a created graph.

Developing a datasource mainly involves forwarding events from it one by one into a transformer. This section will be split into two different approaches, one using a specific Transformer, and one using the `GenericTransformer`.

## Node Classes

The Node classes define a schema of attributes which belong to a certain kind of entity in the graph. They also define all outbound edges from the node, and to which type of node this edge can go to.

Most importantly, Node classes define which set of attributes can be used to determine equality between two nodes.

As an example, we can look at the `File` node class:

```python
class File(Node):
    __name__ = "File"
    __color__ = "#3CB371"

    host: Optional[str]
    full_path: Optional[str]
    file_path: Optional[str]
    file_name: Optional[str]
    extension: Optional[str]
    timestamp: Optional[int]
    hashes: Optional[Dict[str, str]] = {}

    file_of: DefaultDict["Process", FileOf]
    copied_to: DefaultDict["File", CopiedTo]

    key_fields: List[str] = ["host", "full_path"]
```

The `File` node class has 7 different properties, and 2 edge type outbound from it. Most importantly, the `File` class defines that if two instances of it have the same `host` and `full_path` values, then they are equal. In other words:

```python
File(host="foo", full_path="bar") == File(host="foo", full_path="bar")
hash(File(host="foo", full_path="bar")) == hash(File(host="foo", full_path="bar"))

# Different host, differnet hash
File(host="foo_jim", full_path="bar") != File(host="foo_jim", full_path="bar")
```

This is useful since transformers return a list of nodes, and the same entity might appear a couple of times throughout this list. This makes it so that the backend won't re-insert the same entity multiple times, and that it can simply pull out the relevant data from the current instance of that entity (for example, edges).

Creating Node classes is pretty straight forward, and requires implementing four annotations and one function:

```python
from beagle.nodes import Node
class MyNode(Node):
    __name__ :str # This is the human-friendly name of the node class.
    __color__ :str #This is a hex string representing the color of the node for visualizations (e.g "#FF0000")
    key_fields: List[str] # This is a list of attributes which, when combine, allow us to determine equality

    # Returns an array of all edge dictionarys.
    @property
    def edges(self) -> List[DefaultDict]:
        ...
```

Adding edges **outbound** from the node, requires adding an annotation of type `DefaultDict[Node, Edge]`. Let's say we want to add an edge of type `MyEdge` between a `MyNode` and a `Process`, and we want the attribute to be called `myedge_of`

```python
class MyNode(Node):
    ...

    myedge_of: DefaultDict[Process, MyEdge]

    # Make sure to initalize the dict in __init__
    def __init__(self, ...) -> None:

        self.my_edgeof = defaultdict(MyEdge)
```

## Edge Classes

Creating Edge classes mainly involves defining which attributes can be held on the edge, and the name of the edge. For example, a basic edge class with no data might look like this:

```python
class FileOf(Edge):
    __name__ = "File Of"
```

While an edge class that may hold some values can be defined like this:

```python
class ChangedValue(Edge):
    __name__ = "Changed Value"

    value: Optional[str]
    timestamp: int

    def __init__(self) -> None:
        super().__init__()
```

### Using Edge Classes

Once an edge class is defined, it is set as an attribute on a node class. Adding the edge can be done by inserting the target node into the defaultdict, and optionally adding data to that instance as shown below:

Let's say we want to add a `ChangeValue` edge from a `Process` to a `RegistryKey`, and that the edge `defaultdict` is defined on `changed_value` attribute:

```python
proc = Process(...)
reg_key = RegistryKey(...)

# No edge data
proc.changed_value[reg_key]

# With edge data
proc.changed_value[reg_key].append(timestamp=1, value="foo")
```

## ProcMon DataSource and Transformer Example

In this example, we'll create a data source and transformer for (procmon CSV files)[https://docs.microsoft.com/en-us/sysinternals/downloads/procmon]. Since these files are CSV files, our data source will not do much besides iterate over the events one by one, format the time stamp, and send it to a transformer.

#### Setting up the classes

Setting up the class is straight forward, we'll using `pandas` to read the CSV.

We'll create two files

-   `beagle/datasources/procmon_csv.py` The datasource
-   `beagle/transformers/procmon_transformer.py` The transformer

Datasource:

```python
from beagle.common.logging import logger
from beagle.datasources.base_datasource import DataSource
from beagle.transformers.procmon_transformer import ProcmonTransformer

class ProcmonCSV(DataSource):
    """Reads events in one by one from a ProcMon CSV, and parses them into the GenericTransformer"""

    name = "Procmon CSV" # The name as it'll appear in the web GUI
    category = "Procmon" # The category this will output to.
    transformers = [ProcmonTransformer] # The transformer this will send events to

    def __init__(self, procmon_csv: str) -> None:
        self.procmon_csv = procmon_csv

        super().__init__(*args, **kwargs)

        logger.info("Set up ProcmonCSVs")

```

Transformer:

```python
import re
from typing import Optional, Tuple

from beagle.common import split_path
from beagle.nodes import File, Process
from beagle.transformers.base_transformer import Transformer

class ProcmonTransformer(Transformer):
    name = "Procmon"


```

##### Generating Events

Now, taking a look at our data:

```csv
In [10]: !head Logfile.CSV
"Time of Day","Process Name","PID","Operation","Path","Result","Detail","TID"
"10:29:05.0593693 AM","Explorer.EXE","2900","ReadFile","C:\Windows\explorer.exe","SUCCESS","Offset: 2,275,840, Length: 16,384, I/O Flags: Non-cached, Paging I/O, Synchronous Paging I/O, Priority: Normal","3408"
"10:29:05.0595947 AM","Explorer.EXE","2900","ReadFile","C:\Windows\explorer.exe","SUCCESS","Offset: 2,255,360, Length: 16,384, I/O Flags: Non-cached, Paging I/O, Synchronous Paging I/O, Priority: Normal","3408"
"10:29:05.0610122 AM","Explorer.EXE","2900","ReadFile","C:\Windows\System32\twinui.dll","SUCCESS","Offset: 8,310,784, Length: 12,800, I/O Flags: Non-cached, Paging I/O, Synchronous Paging I/O,
```

Since there's a lot of variety in the `Detail` field, we'll leave that to the transformer to parse. The datasource will parse the time of day, and rename the fields:

```python

def events(self) -> Generator[dict, None, None]:
    # Iterate over the dataframe
    for _, row in self._df.iterrows():
        # Get times
        hr_min_sec = row["Time of Day"].split(".")[0]

        # Check if AM
        in_am = "AM" in row["Time of Day"]

        # set the hours/min/sec
        date = self.now.replace(
            second=int(hr_min_sec.split(":")[-1]),
            hour=int(hr_min_sec.split(":")[0]) + (0 if in_am else 12),
            minute=int(hr_min_sec.split(":")[1]),
        )

        epoch = int(date.strftime("%s"))

        yield {
            "event_time": epoch,
            "event_type": row["Operation"],
            "process_name": row["Process Name"],
            "path": row["Path"],
            "process_id": int(row["PID"]),
            "params": row["Detail"],
        }
```

There's no more work to do with the Datasource, when the transformer calls the `events()` function on it, it will yield events from the procmon CSV one by one after converting the `PID` field to an integer, and converting the timestamps to dates.

##### Transforming Events

The rest of the work will be done in the transformer class, the main function to implement is the `transform(self, event: dict) -> Tuple` function.

Since each different `Opreation` field (mapped to `event_type` by the datasource) has a different set of values in the `Detail` field, we'll need to write the transform as a switch statement on the `event_type`, and write functions to create `Node` classes from the individual operation types.

The first one to parse is the `Process Create` operation, which looks like this when it comes out of the Datasource:

```json
{
    "event_time": 1,
    "event_type": "Process Create",
    "process_name": "svchost.exe",
    "path": "C:\\Windows\\system32\\DllHost.exe",
    "process_id": "1234",
    "params": "PID: 4844, Command line: C:\\Windows\\system32\\DllHost.exe /Processid:{AB8902B4-09CA-4BB6-B78D-A8F59079A8D5}"
}
```

From this, we can extract the following information:

1. Parent process from the `process_name, process_id` fields.
2. The created process from the `path` and values in the `param` field.
3. The file of the created process.

To do this, we'll create the `process_create` function, define its type hints, and write a regex to pull out the PID and command line values from `event["params"]`

```python
def process_create(self, event) -> Tuple[Process, File, Process]:
    pid = -1 # Unknown PID value
    command_line = None # no command line
    match = re.match(r"PID: (\d*), Command line: (.*)", event["params"])
    if match:
        pid, command_line = match.groups()

    # parse out the image and path using beagle.common.split_path
    process_image, process_image_path = split_path(event["path"])

```

Now that we have all the values, we can make the created `Process` node, as well as use the `get_file_node()` helper to make it's `File` node.

```python
proc = Process(
    process_id=int(pid),
    process_image=process_image,
    process_image_path=process_image_path,
    command_line=command_line,
)

# Create the `File` node from `process_image` and `process_image_path`
proc_file = proc.get_file_node()
# Associate the file to the process.
proc_file.file_of[proc]
```

We can also create the parent process node from the `process_name` amnd `process_id` keys of the event:

```python
parent = Process(
    process_id=int(event["process_id"]),
    process_image=event["process_name"]
)
```

Finally, we can grab the `event_time` and create an edge between the parent and child processes, then return te created nodes.

```python
parent.launched[proc].append(timestamp=event["event_time"])
return (proc, proc_file, parent)
```

The full function:

```python
def process_create(self, event) -> Tuple[Process, File, Process]:

    pid = -1
    command_line = None
    match = re.match(r"PID: (\d*), Command line: (.*)", event["params"])
    if match:
        pid, command_line = match.groups()

    process_image, process_image_path = split_path(event["path"])

    proc = Process(
        process_id=int(pid),
        process_image=process_image,
        process_image_path=process_image_path,
        command_line=command_line,
    )
    proc_file = proc.get_file_node()
    proc_file.file_of[proc]

    parent = Process(process_id=int(event["process_id"]), process_image=event["process_name"])

    parent.launched[proc].append(timestamp=event["event_time"])

    return (proc, proc_file, parent)
```

Finally, we add this case into the transformer, so that any event which has the `Process Create` type gets mapped to this function:

```python
def transform(self, event: dict) -> Optional[Tuple]:

    operation = event["event_type"]
    if operation == "Process Create":
        return self.process_create(event)
    else:
        return None
```

That's it! now the transformer and datasource can work together to yield nodes to be placed into a graph by the backends.
