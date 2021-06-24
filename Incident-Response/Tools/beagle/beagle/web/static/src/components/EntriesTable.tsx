import * as _ from 'lodash';
import * as React from 'react';
import { Link } from 'react-router-dom';
import { Button, Container, Header, Popup } from 'semantic-ui-react';
import { snakeToSpaced } from 'src/common';

import DataTable from './misc/DataTable';
import LoadingBar from './misc/LoadingBar';

export interface EntriesTableProps {
    category: string;
    name: string;
}

interface CategoryEntry {
    comment: string;
    id: number;
    metadata: object;
}

export interface EntriesTableState {
    entries: CategoryEntry[];
    ready: boolean;
}

export default class EntriesTable extends React.Component<EntriesTableProps, EntriesTableState> {
    constructor(props: EntriesTableProps) {
        super(props);

        this.state = {
            entries: [],
            ready: false
        };
    }

    public componentWillMount = () => {
        fetch(
            `${
                process.env.NODE_ENV === "production" ? "" : "http://localhost:8000"
            }/api/categories/${this.props.category}`
        )
            .then(resp => resp.json())
            .then((json: CategoryEntry[]) => this.setState({ entries: json, ready: true }));
    };

    public render() {
        if (this.state.ready === false) {
            return <LoadingBar text={"Fetching Entries"} />;
        }

        if (this.state.entries.length === 0) {
            return (
                <Header
                    as="h1"
                    textAlign="center"
                    style={{
                        marginTop: "50px"
                    }}
                >
                    No Entries!
                </Header>
            );
        }

        const entries = this.state.entries.map((entry, idx) => {
            let pairs = _.toPairs(entry.metadata).map(pair => {
                if (typeof pair[1] === "string" && pair[1].startsWith("http")) {
                    pair[1] = <Button href={pair[1]} content="Follow Link" />;
                }
                return [
                    snakeToSpaced(pair[0]),
                    <Popup key={idx} content={pair[1]} trigger={<span>{pair[1]}</span>} />
                ];
            });

            pairs = [
                ...pairs,
                ["Comment", entry.comment],
                [
                    "Graph",
                    <Link key={idx} to={`${this.props.category}/${entry.id}`}>
                        <Button color="blue" content="View Graph" />
                    </Link>
                ]
            ];
            return _.fromPairs(pairs);
        });

        const keys = [...Object.keys(this.state.entries[0].metadata), "comment", "Graph"];

        return (
            <Container
                style={{
                    marginTop: "50px",
                    width: "90%",
                    maxWidth: "90%"
                }}
            >
                <Header as="h2" textAlign="center">
                    {this.props.name}
                </Header>
                <DataTable
                    data={entries}
                    tableProps={{
                        striped: true,
                        size: "small",
                        fixed: true
                    }}
                    header={true}
                    rowsPerPage={10}
                    columnHeader={keys.map(key => snakeToSpaced(key))}
                />
            </Container>
        );
    }
}
