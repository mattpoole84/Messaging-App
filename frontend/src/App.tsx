import React from 'react';
import EmailTaskTable from './components/EmailTask_Table'
import MsgTaskTable from './components/MessageTask_Table'
import { LogsTable, ErrorLogsTable } from './components/Log_Table'
import { Route } from 'react-router-dom';
import { Heading, Pane, majorScale, TabNavigation, Tab, minorScale, Button, LogInIcon } from 'evergreen-ui'

const App = () => {
  return (
    <Pane>
        <Pane is="header" elevation={1} paddingLeft={majorScale(2)} paddingRight={majorScale(2)} height={72} display="flex" alignItems="center">
            <Pane width={1200} display="flex" alignItems="center" marginLeft="auto" marginRight="auto">
                <Heading size={500} fontWeight={700}>
                    COMMUNICATION CENTER
                </Heading>
                <TabNavigation marginLeft="auto" marginRight="auto">
                    {['Messages', 'Emails', 'Logs', 'Search'].map((tab, index) => (
                    <Tab key={tab} is="a" marginRight={minorScale(8)} href={tab.toLowerCase()} id={tab}>
                        {tab}
                    </Tab>
                    ))}
                </TabNavigation>
                <Button appearance="primary" iconAfter={LogInIcon}>Logout</Button>
            </Pane>
        </Pane>
        <Pane is="main" marginTop={majorScale(3)} width={1200} marginLeft="auto" marginRight="auto">
            <Route exact path="/emails" component={EmailTaskTable}/>
            <Route path="/messages" component={MsgTaskTable}/>
            <Route path="/logs">
                <LogsTable/>
                <ErrorLogsTable/>
            </Route>
        </Pane>
    </Pane>
  );
};

export default App;