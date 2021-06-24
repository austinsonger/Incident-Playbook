import { Form } from 'formsy-semantic-ui-react';
import * as React from 'react';
import Dropzone from 'react-dropzone';
import { Redirect } from 'react-router';
import { Button, Checkbox, Container, Header, Icon, Message, Popup, Segment, Step } from 'semantic-ui-react';
import { snakeToSpaced } from 'src/common';
import LoadingBar from 'src/components/misc/LoadingBar';

interface Transformer {
    id: string;
    name: string;
}

interface Backend {
    id: string;
    name: string;
}

interface DataSourceEntry {
    id: string;
    name: string;
    params: Array<{ name: string; required: boolean; default: null | string }>;
    transformers: Transformer[];
    type: string;
}

export interface UploadProps {
    postRoute: string; // Where should this post to?
    postUploadHandler?: () => null; // What to do after upload
}

export interface UploadState {
    selectedDatasource: DataSourceEntry;
    selectedTransformer: Transformer;
    selectedBackend: Backend;
    isExternal: boolean;
    comment: string;
    params: Array<{ name: string; required: boolean; default: null | string }>;
    formParams: { [name: string]: string | File };
    ready: boolean;
    errorMessage: string;
    graphRoute: string;
    redirect: boolean;
    steps: { [name: string]: { active: boolean; done: boolean; link?: string } };
    processing: boolean;
    advancedVisible: boolean;
}

export default class Upload extends React.Component<UploadProps, UploadState> {
    public pipelines: DataSourceEntry[];
    public backends: Backend[];

    constructor(props: UploadProps) {
        super(props);

        this.pipelines = [];
        this.backends = [];

        this.state = {
            ready: false,
            comment: "",
            isExternal: false,
            selectedDatasource: {} as DataSourceEntry,
            selectedTransformer: {} as Transformer,
            // By default use NetworkX
            selectedBackend: { id: "NetworkX", name: "NetworkX" },
            params: [],
            formParams: {},
            graphRoute: "",
            redirect: false,
            errorMessage: "",
            steps: {
                upload: { active: true, done: false },
                transform: { active: false, done: false },
                view: { active: false, done: false }
            },
            processing: false,
            advancedVisible: false
        };
    }

    public componentWillMount() {
        // Get the list of data sources to present in the form.
        fetch(
            `${
                process.env.NODE_ENV === "production" ? "" : "http://localhost:8000"
            }/api/datasources`
        )
            .then(resp => resp.json())
            .then(json => {
                if (json === undefined) {
                    return;
                }

                this.pipelines = json.datasources;
                this.backends = json.backends;

                const firstDataSource = this.pipelines[0];

                const isExternal = firstDataSource.type === "external";

                this.setState({
                    selectedDatasource: firstDataSource,
                    selectedTransformer: firstDataSource.transformers[0],
                    params: firstDataSource.params,
                    ready: true,
                    isExternal
                });
            });
    }

    public setActiveTranformer = (e: any, target: any) => {
        this.setState({
            selectedTransformer: target.value
        });
    };
    public setActiveBackend = (e: any, target: any) => {
        this.setState({
            selectedBackend: target.value
        });
    };

    public handleToggleAdvanced = () => {
        this.setState({
            advancedVisible: !this.state.advancedVisible
        });
    };
    public updateTransformers = (e: any, target: any) => {
        this.setState({
            selectedDatasource: target.value,
            selectedTransformer: target.value.transformers[0],
            params: target.value.params,
            isExternal: target.value.type === "external",
            formParams: {}
        });
    };

    public handleCommentChange = (e: any, data: any) => {
        this.setState({ comment: data.value });
    };

    public onDrop = (filename: string) => {
        return (accepted: File[]) => {
            const current = this.state.formParams;
            current[filename] = accepted[0];
            this.setState({
                formParams: current
            });
        };
    };

    public onParamChange = (paramName: string) => {
        return (e: any, data: any) => {
            const current = this.state.formParams;
            current[paramName] = data.value;
            this.setState({
                formParams: current
            });
        };
    };

    public onSubmit = () => {
        const missing = this.state.params.filter(
            param =>
                param.required === true && !Object.keys(this.state.formParams).includes(param.name)
        );

        if (missing.length > 0) {
            const missingNames = missing.map(s => snakeToSpaced(s.name.replace("_file", "")));

            this.setState({
                errorMessage: `The following parameters are required: ${missingNames.join(", ")}`,
                graphRoute: "",
                processing: false,
                steps: {
                    upload: { active: true, done: false },
                    transform: { active: false, done: false },
                    view: { active: false, done: false }
                }
            });
            return;
        }

        const formData = new FormData();
        formData.append("datasource", this.state.selectedDatasource.id);
        formData.append("backend", this.state.selectedBackend.id);
        formData.append("transformer", this.state.selectedTransformer.id);
        formData.append("comment", this.state.comment);

        // Add in the parameters requiered by the transformer
        this.state.params.forEach(key => {
            if (this.state.formParams[key.name] !== undefined) {
                formData.append(key.name, this.state.formParams[key.name]);
            }
        });

        this.setState({
            processing: true,
            errorMessage: "",
            graphRoute: "",
            steps: {
                upload: { active: true, done: true },
                transform: { active: true, done: false },
                view: { active: false, done: false }
            }
        });

        fetch(
            `${
                process.env.NODE_ENV === "production" ? "" : "http://localhost:8000" // Point to localhost if not prod
            }/api${this.props.postRoute}`, // Use the props route.
            {
                method: "POST",
                body: formData
            }
        )
            .then(resp => resp.json())
            .then(json => {
                if (json.hasOwnProperty("message")) {
                    this.setState({
                        errorMessage: `Error on parse: ${json.message}`,
                        graphRoute: "",
                        processing: false,
                        steps: {
                            upload: { active: true, done: false },
                            transform: { active: false, done: false },
                            view: { active: false, done: false }
                        }
                    });
                } else if (json.hasOwnProperty("resp")) {
                    this.setState({
                        graphRoute: json.resp,
                        redirect: false,
                        processing: false,
                        steps: {
                            upload: { active: true, done: true },
                            transform: { active: true, done: true },
                            view: { active: true, done: true, link: json.resp }
                        }
                    });
                } else {
                    if (this.props.postUploadHandler !== undefined) {
                        this.props.postUploadHandler();
                    }

                    this.setState({
                        processing: false,
                        graphRoute: json.self,
                        redirect: true,
                        steps: {
                            upload: { active: true, done: true },
                            transform: { active: true, done: true },
                            view: { active: true, done: false, link: json.self }
                        }
                    });
                }
            });
    };

    public makeDropZones = () => {
        return this.state.params.map(param => (
            <Form.Field key={param.name} required={param.required} name={param.name}>
                <Dropzone multiple={false} onDrop={this.onDrop(param.name)}>
                    {({ getRootProps, getInputProps }) => (
                        <div {...getRootProps()}>
                            <input {...getInputProps()} />
                            <Segment placeholder={true}>
                                <Header icon={true}>
                                    <Icon name="file archive" />
                                    {!(param.name in this.state.formParams)
                                        ? snakeToSpaced(param.name.replace("_file", ""))
                                        : (this.state.formParams[param.name] as File).name}
                                </Header>
                                <Button primary={true}>Upload Data</Button>
                            </Segment>
                        </div>
                    )}
                </Dropzone>
            </Form.Field>
        ));
    };

    public makeInputs = () => {
        return this.state.params.map(param => (
            <Form.Input
                name={param.name}
                key={param.name}
                placeholder={param.default}
                label={snakeToSpaced(param.name)}
                onChange={this.onParamChange(param.name)}
                required={param.required}
            />
        ));
    };

    public makeSteps = () => {
        return (
            <Step.Group attached={"top"} widths={3}>
                <Step
                    completed={this.state.steps.upload.done}
                    active={this.state.steps.upload.active}
                >
                    <Icon name="upload" />
                    <Step.Content>
                        <Step.Title>Upload Data</Step.Title>
                        <Step.Description>Select from available data sources.</Step.Description>
                    </Step.Content>
                </Step>

                <Step
                    completed={this.state.steps.transform.done}
                    active={this.state.steps.transform.active}
                >
                    <Icon name="cogs" />
                    <Step.Content>
                        <Step.Title>Transform</Step.Title>
                        <Step.Description>Transform Data</Step.Description>
                    </Step.Content>
                </Step>

                <Step
                    completed={this.state.steps.view.done}
                    active={this.state.steps.view.active}
                    link={this.state.steps.view.link !== undefined}
                    href={this.state.steps.view.link}
                >
                    <Icon name="linode" />
                    <Step.Content>
                        <Step.Title>View Graph</Step.Title>
                    </Step.Content>
                </Step>
            </Step.Group>
        );
    };

    public render() {
        if (this.state.ready === false) {
            return <LoadingBar text="Loading Configurations" />;
        } else {
            return (
                <Container
                    style={{
                        marginTop: "50px",
                        width: "65%"
                    }}
                >
                    {this.makeSteps()}
                    <Form className="attached fluid segment">
                        <Form.Group widths="equal">
                            <Form.Select
                                search={true}
                                name="datasource"
                                label={
                                    <div>
                                        <Popup
                                            trigger={<Icon name="info circle" />}
                                            content="Select the type of data you would like graphed."
                                        />
                                        <span
                                            style={{
                                                color: "rgba(0,0,0,.87)",
                                                fontSize: ".92857143em",
                                                fontWeight: 700
                                            }}
                                        >
                                            Data Source
                                        </span>
                                    </div>
                                }
                                placeholder="Select Data Source"
                                value={this.state.selectedDatasource}
                                options={this.pipelines.map(datasource => ({
                                    key: datasource.id,
                                    text: datasource.name,
                                    value: datasource
                                }))}
                                onChange={this.updateTransformers}
                            />
                            {this.state.advancedVisible &&
                                (this.state.selectedDatasource.transformers && (
                                    <Form.Select
                                        name="transformer"
                                        label={
                                            <div>
                                                <Popup
                                                    trigger={<Icon name="info circle" />}
                                                    content="Different transformers may produce different graphs"
                                                />
                                                <span
                                                    style={{
                                                        color: "rgba(0,0,0,.87)",
                                                        fontSize: ".92857143em",
                                                        fontWeight: 700
                                                    }}
                                                >
                                                    Transformer
                                                </span>
                                            </div>
                                        }
                                        placeholder="Select Transformer"
                                        value={this.state.selectedTransformer}
                                        options={this.state.selectedDatasource.transformers.map(
                                            transformer => ({
                                                key: transformer.id,
                                                text: transformer.name,
                                                value: transformer
                                            })
                                        )}
                                        onChange={this.setActiveTranformer}
                                    />
                                ))}
                            {this.state.advancedVisible && (
                                <Form.Select
                                    name="backend"
                                    label={
                                        <div>
                                            <Popup
                                                trigger={<Icon name="info circle" />}
                                                content="Destination of the graph. NetworkX will use the web GUI."
                                            />
                                            <span
                                                style={{
                                                    color: "rgba(0,0,0,.87)",
                                                    fontSize: ".92857143em",
                                                    fontWeight: 700
                                                }}
                                            >
                                                Backend
                                            </span>
                                        </div>
                                    }
                                    placeholder="Select Transformer"
                                    value={this.state.selectedBackend}
                                    options={this.backends.map(backend => ({
                                        key: backend.id,
                                        text: backend.name,
                                        value: backend
                                    }))}
                                    onChange={this.setActiveBackend}
                                />
                            )}
                        </Form.Group>
                        <Form.TextArea
                            name="comment"
                            label={"Comment"}
                            placeholder=""
                            value={this.state.comment}
                            onChange={this.handleCommentChange}
                        />

                        <Header textAlign="center" as="h5">
                            {this.state.isExternal
                                ? "Input required parameters"
                                : "Upload Required Files"}
                        </Header>
                        <Form.Group className="fluid" widths="equal">
                            {this.state.isExternal ? this.makeInputs() : this.makeDropZones()}
                        </Form.Group>
                        <Form.Field>
                            <Checkbox
                                onChange={this.handleToggleAdvanced}
                                checked={this.state.advancedVisible}
                                label="Show Advanced Options"
                            />
                        </Form.Field>
                        <Button style={{ marginTop: "1em" }} color="blue" onClick={this.onSubmit}>
                            Submit
                        </Button>
                    </Form>
                    {this.state.errorMessage !== "" && (
                        <Message
                            negative={true}
                            icon="warning sign"
                            attached="bottom"
                            header="Error"
                            content={this.state.errorMessage}
                        />
                    )}
                    {this.state.graphRoute !== "" && [
                        <Message
                            key="msg"
                            positive={true}
                            icon="lnode"
                            attached="bottom"
                            header="Graph succesfully created!"
                            content={this.state.graphRoute}
                        />,
                        this.state.redirect && (
                            <Redirect key="redirect" to={this.state.graphRoute} />
                        )
                    ]}
                    {this.state.processing && (
                        <Message info={true} icon={true} attached="bottom">
                            <Icon name="circle notched" loading={true} />
                            <Message.Content>
                                <Message.Header>Graphing data</Message.Header>
                            </Message.Content>
                        </Message>
                    )}
                </Container>
            );
        }
    }
}
