import 'react-redux-toastr/lib/css/react-redux-toastr.min.css';

import * as React from 'react';
import { Provider } from 'react-redux';
import ReduxToastr from 'react-redux-toastr';
import { applyMiddleware, createStore } from 'redux';
import logger from 'redux-logger';

import Router from './components/Router';
import { reducer } from './reducers';

/*
 * We're giving State interface to create store
 * store is type of State defined in our reducers
 */

export const store =
    process.env.NODE_ENV === "production"
        ? createStore(reducer)
        : createStore(reducer, applyMiddleware(logger));

export default class App extends React.Component {
    public render() {
        return (
            <Provider store={store}>
                <ReduxToastr
                    timeOut={2000}
                    newestOnTop={false}
                    preventDuplicates={true}
                    position="top-center"
                    progressBar={false}
                    closeOnToastrClick={true}
                />
                <Router />
            </Provider>
        );
    }
}
