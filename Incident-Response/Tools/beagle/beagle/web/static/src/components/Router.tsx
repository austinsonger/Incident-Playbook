import * as React from 'react';
import { BrowserRouter, Link, Route, Switch } from 'react-router-dom';
import { Icon, Menu, Sidebar as SUSidebar } from 'semantic-ui-react';
import GraphPage from 'src/containers/GraphPage';
import Upload from 'src/views/Upload';

import EntriesTable from './EntriesTable';

interface MenuEntry {
    icon?: JSX.Element;
    name: string;
    route: string;
    id: string;
    component?: any;
}

interface SideBarState {
    entries: MenuEntry[];
}

class Sidebar extends React.Component<any, SideBarState> {
    public constructor(props: any) {
        super(props);

        this.state = {
            entries: [
                {
                    id: "upload",
                    route: "/",
                    name: "Upload Data",
                    icon: <Icon name="upload" />,
                    component: () => <Upload postRoute="/new" />
                }
            ]
        };
    }

    public componentWillMount() {
        fetch(
            `${
                process.env.NODE_ENV === "production" ? "" : "http://localhost:8000"
            }/api/categories?uploaded=true`
        )
            .then(resp => resp.json())
            .then(json => {
                this.setState({
                    entries: [
                        ...this.state.entries,
                        ...json.map((category: { name: string; id: string }) => ({
                            id: category.id,
                            name: category.name,
                            route: `/${category.id}`
                        }))
                    ]
                });
            });
    }

    public renderEntriesForCategory = (category: string, name: string) => {
        return (props: any) => {
            return <EntriesTable {...props} name={name} category={category} />;
        };
    };

    public render() {
        return (
            <BrowserRouter>
                <div>
                    <div id="siderbar">
                        <SUSidebar
                            style={{
                                position: "fixed" as "fixed",
                                width: "150px"
                            }}
                            as={Menu}
                            inverted={true}
                            animation={"overlay"}
                            visible={true}
                            vertical={true}
                            width="thin"
                        >
                            {this.state.entries.map((entry, index) => {
                                return (
                                    <Link to={entry.route} key={index}>
                                        <Menu.Item>
                                            {"icon" in entry && entry.icon}
                                            {entry.name}
                                        </Menu.Item>
                                    </Link>
                                );
                            })}
                        </SUSidebar>
                    </div>
                    <div
                        id="content"
                        style={{
                            marginLeft: "150px"
                        }}
                    >
                        <Switch>
                            {this.state.entries.map((entry, index) => {
                                if (entry.component !== undefined) {
                                    return (
                                        <Route
                                            key={index}
                                            exact={true}
                                            path={entry.route}
                                            component={entry.component}
                                        />
                                    );
                                } else {
                                    return (
                                        <Route
                                            key={index}
                                            exact={true}
                                            path={entry.route}
                                            render={this.renderEntriesForCategory(
                                                entry.id,
                                                entry.name
                                            )}
                                        />
                                    );
                                }
                            })}
                            <Route path="/:category/:id" exact={true} component={GraphPage} />
                        </Switch>
                    </div>
                </div>
            </BrowserRouter>
        );
    }
}

export default Sidebar;
