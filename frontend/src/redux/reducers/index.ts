import { combineReducers } from 'redux';
import getEmailTaskReducer from './EmailTask_Reducer';
import getMsgTaskReducer from './MessageTask_Reducer';
import {LogReducer, ErrorLogReducer} from './Log_Reducer';
import { persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";


const rootReducer = combineReducers({
  email_tasks: getEmailTaskReducer,
  msg_tasks: getMsgTaskReducer,
  logs: LogReducer,
  error_logs : ErrorLogReducer,
});

export default rootReducer
export type RootState = ReturnType<typeof rootReducer>