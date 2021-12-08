import * as React from "react"
import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { getLogs, getErrorLogs } from '../redux/actions/Log_Actions';
import { RootState } from '../redux/reducers'
import { Heading, Pane, Table,Avatar,Text } from 'evergreen-ui'

export const LogsTable: React.FC = () => {

    const [query, setQuery] = useState('');

    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(getLogs());
    }, []);

    const Logs_Data = useSelector((state: RootState) => state.logs.logs);

    if (query.length == 0) {
        var results = Logs_Data;
    }
    else{
        var results = Logs_Data.filter(log => log.description.includes(query.trim()));
    }

    return (
        <Pane>
            <Heading>Logs</Heading>
            <Table>
                <Table.Head>
                    <Table.SearchHeaderCell
                        onChange={setQuery}
                        value={query}
                    />
                    {/* <Table.TextHeaderCell>Type</Table.TextHeaderCell> */}
                    <Table.TextHeaderCell>Description</Table.TextHeaderCell>
                    <Table.TextHeaderCell>Send At</Table.TextHeaderCell>
                    <Table.TextHeaderCell>Completed At</Table.TextHeaderCell>
                    <Table.TextHeaderCell>Status</Table.TextHeaderCell>
                </Table.Head>
                <Table.Body height={240}>
                    {results.map(log => (
                    <Table.Row key={log.id} isSelectable>
                        <Table.TextCell>{log.type}</Table.TextCell>
                        <Table.TextCell>{log.description}</Table.TextCell>
                        <Table.TextCell>{log.send_at}</Table.TextCell>
                        <Table.TextCell>{log.completed_at}</Table.TextCell>
                        <Table.TextCell>{log.status}</Table.TextCell>
                    </Table.Row>
                    ))}
                </Table.Body>
            </Table>
        </Pane>
    )
}

export const ErrorLogsTable: React.FC = () => {

    const [query, setQuery] = useState('');

    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(getErrorLogs());
    }, []);

    const Logs_Data = useSelector((state: RootState) => state.error_logs.error_logs);

    if (query.length == 0) {
        var results = Logs_Data;
    }
    else{
        var results = Logs_Data.filter(log => log.error.includes(query.trim()));
    }

    return (
        <Pane>
            <Heading>Error Logs</Heading>
            <Table>
                <Table.Head>
                    <Table.TextHeaderCell>Error</Table.TextHeaderCell>
                    <Table.TextHeaderCell>Description</Table.TextHeaderCell>
                </Table.Head>
                <Table.Body height={240}>
                    {results.map(log => (
                    <Table.Row key={log.id} isSelectable>
                        <Table.TextCell>{log.error}</Table.TextCell>
                        <Table.TextCell>{log.description}</Table.TextCell>
                    </Table.Row>
                    ))}
                </Table.Body>
            </Table>
        </Pane>
    )
}
