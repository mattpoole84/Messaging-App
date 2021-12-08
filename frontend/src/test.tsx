import React from 'react';
import './App.css';

import { Spinner, Heading, Pane, majorScale, TabNavigation, Tab, minorScale, Button, LogInIcon } from 'evergreen-ui'

function App() {
  return (
    <Pane is="header" elevation={1} paddingLeft={majorScale(2)} paddingRight={majorScale(2)} height={72} display="flex" alignItems="center">
        <Pane width={1200} display="flex" alignItems="center" marginLeft="auto" marginRight="auto">
            <Heading size={500} fontWeight={700}>
                COMMUNICATION CENTER
            </Heading>

            <TabNavigation marginLeft="auto" marginRight="auto">
                {['Messages', 'Emails', 'Logs', 'Search'].map((tab, index) => (
                    <Tab key={tab} is="a" marginRight={minorScale(2)} href={tab.toLowerCase()} id={tab} isSelected={index === 0}>
                        {tab}
                    </Tab>
                ))}
            </TabNavigation>
            
            <Button appearance="primary" iconAfter={LogInIcon}>Logout</Button>

        </Pane>
    </Pane>
  );
}

export default App;
