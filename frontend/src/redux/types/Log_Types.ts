import { Log, ErrorLog } from '../interfaces/Log';

export const GET_LOGS = 'GET_LOGS';
export const GET_ERROR_LOGS = 'GET_ERROR_LOGS'

export interface GetLogStateType {
    logs: Log[];
}
export interface GetErrorLogStateType {
    error_logs: ErrorLog[];
}

interface GetLogActionType {
  type: typeof GET_LOGS;
  payload: Log[];
}
interface GetErrorLogActionType {
    type: typeof GET_ERROR_LOGS;
    payload: ErrorLog[];
}

export type LogActionTypes = GetLogActionType;
export type ErrorLogActionTypes = GetErrorLogActionType;