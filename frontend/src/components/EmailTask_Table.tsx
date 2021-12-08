import * as React from "react"
import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { getEmailTasks } from '../redux/actions/EmailTask_Actions';
import { RootState } from '../redux/reducers'
import { Heading, Pane, Table,Avatar,Text } from 'evergreen-ui'

export const EmailTaskTable: React.FC = () => {

    const [query, setQuery] = useState('');

    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(getEmailTasks());
    }, []);

    const EmailTasks_Data = useSelector((state: RootState) => state.email_tasks.tasks);

    if (query.length == 0) {
        var results = EmailTasks_Data;
    }
    else{
        var results = EmailTasks_Data.filter(task => task.name.includes(query.trim()));
    }

    return (
        <Pane>
            <Heading>Emails</Heading>
            <Table>
                <Table.Head>
                    <Table.SearchHeaderCell
                        onChange={setQuery}
                        value={query}
                    />
                    {/* <Table.TextHeaderCell>Name</Table.TextHeaderCell> */}
                    <Table.TextHeaderCell>Email</Table.TextHeaderCell>
                    <Table.TextHeaderCell>Subject</Table.TextHeaderCell>
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
                        <Table.TextCell>{task.email}</Table.TextCell>
                        <Table.TextCell>{task.subject}</Table.TextCell>
                        <Table.TextCell>{task.status}</Table.TextCell>
                    </Table.Row>
                    ))}
                </Table.Body>
            </Table>
        </Pane>
    )
}

export default EmailTaskTable