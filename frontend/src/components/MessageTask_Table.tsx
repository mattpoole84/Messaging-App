import * as React from "react"
import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { getMsgTasks } from '../redux/actions/MessageTask_Actions';
import { RootState } from '../redux/reducers'
import { Heading, Pane, Table,Avatar,Text } from 'evergreen-ui'

export const MsgTaskTable: React.FC = () => {

    const [query, setQuery] = useState('');

    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(getMsgTasks());
    }, []);

    const MsgTasks_Data = useSelector((state: RootState) => state.msg_tasks.tasks);

    if (query.length == 0) {
        var results = MsgTasks_Data;
    }
    else{
        var results = MsgTasks_Data.filter(task => task.name.includes(query.trim()));
    }

    return (
        <Pane>
            <Heading>Messages</Heading>
            <Table>
                <Table.Head>
                    <Table.SearchHeaderCell
                        onChange={setQuery}
                        value={query}
                    />
                    {/* <Table.TextHeaderCell>Name</Table.TextHeaderCell> */}
                    <Table.TextHeaderCell>Phone Number</Table.TextHeaderCell>
                    <Table.TextHeaderCell>Message</Table.TextHeaderCell>
                    <Table.TextHeaderCell>Status</Table.TextHeaderCell>
                </Table.Head>
                <Table.Body height={240}>
                    {results.map(task => (
                    <Table.Row key={task.id} isSelectable>
                        <Table.Cell display="flex" alignItems="center">
                            <Avatar name={task.name} />
                            <Text marginLeft={8} size={300} fontWeight={500}>
                                {task.name}
                            </Text>
                        </Table.Cell>
                        <Table.TextCell>{task.phone}</Table.TextCell>
                        <Table.TextCell>{task.message}</Table.TextCell>
                        <Table.TextCell>{task.status}</Table.TextCell>
                    </Table.Row>
                    ))}
                </Table.Body>
            </Table>
        </Pane>
    )
}

export default MsgTaskTable