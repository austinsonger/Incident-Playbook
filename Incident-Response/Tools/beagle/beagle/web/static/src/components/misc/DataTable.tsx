import * as React from 'react';
import {
    Menu,
    MenuItem,
    Table,
    TableBody,
    TableCell,
    TableFooter,
    TableHeader,
    TableHeaderCell,
    TableProps,
    TableRow,
} from 'semantic-ui-react';

interface DataTableState {
    currentPage: number;
    rowsPerPage: number;
    numberOfPages: number;
    columns: string[];
}

interface DataTableProps extends TableProps {
    data: any[];
    rowsPerPage?: number;
    tableProps?: TableProps;
    header?: boolean;
    columnHeader?: string[];
}

export default class DataTable extends React.Component<DataTableProps, DataTableState> {
    constructor(props: DataTableProps) {
        super(props);

        const rowsPerPage = props.rowsPerPage || 5;
        const numberOfPages = Math.ceil(props.data.length / rowsPerPage);
        const columns = props.columnHeader || Object.keys(props.data[0] || []);

        this.state = {
            currentPage: 1,
            rowsPerPage,
            numberOfPages,
            columns
        };
    }

    public handlePageClick = (e: React.MouseEvent<HTMLElement>) => {
        if (e.currentTarget.dataset.page) {
            this.setState({
                currentPage: Number(e.currentTarget.dataset.page)
            });
        }
    };

    public handleDirectionClick = (e: React.MouseEvent<HTMLElement>) => {
        const direction = e.currentTarget.dataset.direction;

        let change = 0;
        if (direction === "LEFT" && this.state.currentPage > 1) {
            change = -1;
        } else if (direction === "RIGHT" && this.state.currentPage < this.state.numberOfPages) {
            change = 1;
        }

        if (change !== 0) {
            this.setState({
                currentPage: this.state.currentPage + change
            });
        }
    };

    public render() {
        const { data } = this.props;
        const { currentPage, rowsPerPage, numberOfPages, columns } = this.state;

        // slice current data set (more filters could be added, and also sorting)
        const currentData = data.slice((currentPage - 1) * rowsPerPage, currentPage * rowsPerPage);

        let startPage = this.state.currentPage - 1;

        if (numberOfPages <= 3 || this.state.currentPage === 1) {
            startPage = 1;
        } else if (this.state.currentPage === numberOfPages) {
            startPage = this.state.currentPage - 2;
        }

        const pageRange: number[] = Array.from(
            new Array(Math.min(3, numberOfPages)),
            (x, i) => i + startPage
        );
        let entryIdx = 0;
        return (
            <div>
                <Table {...this.props.tableProps}>
                    {this.props.header && (
                        <TableHeader>
                            <TableRow>
                                {columns.map(key => (
                                    <TableHeaderCell key={key}>{key}</TableHeaderCell>
                                ))}
                            </TableRow>
                        </TableHeader>
                    )}
                    <TableBody>
                        {currentData.map(row => (
                            <TableRow key={entryIdx++}>
                                {columns.map(key => (
                                    <TableCell
                                        collapsing={true}
                                        key={entryIdx++}
                                        content={row[key]}
                                    />
                                ))}
                            </TableRow>
                        ))}
                    </TableBody>
                    <TableFooter>
                        <TableRow>
                            <TableHeaderCell {...{ colSpan: this.state.columns.length }}>
                                <Menu floated="right" pagination={true}>
                                    <MenuItem
                                        icon="angle double left"
                                        data-page={1}
                                        onClick={this.handlePageClick}
                                    />
                                    <MenuItem
                                        data-direction="LEFT"
                                        onClick={this.handleDirectionClick}
                                        icon="angle left"
                                    />
                                    {pageRange.map(pageIndex => (
                                        <MenuItem
                                            key={pageIndex}
                                            content={`${pageIndex}`}
                                            data-page={pageIndex}
                                            onClick={this.handlePageClick}
                                            active={pageIndex === this.state.currentPage}
                                            as="a"
                                        />
                                    ))}
                                    <MenuItem
                                        data-direction="RIGHT"
                                        onClick={this.handleDirectionClick}
                                        icon="angle right"
                                    />
                                    <MenuItem
                                        icon="angle double right"
                                        data-page={numberOfPages}
                                        onClick={this.handlePageClick}
                                    />
                                </Menu>
                            </TableHeaderCell>
                        </TableRow>
                    </TableFooter>
                </Table>
            </div>
        );
    }
}
