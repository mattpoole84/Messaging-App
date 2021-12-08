import {GET_LOGS, GET_ERROR_LOGS, GetLogStateType, GetErrorLogStateType } from '../types/Log_Types';
  
const initialStateGetLogs: GetLogStateType = {
    logs: []
};
  
export function LogReducer(state = initialStateGetLogs , action):GetLogStateType {
      switch (action.type) {
          case GET_LOGS:
              return {
                ...state,
                logs: action.payload
              };
          default:
              return state;
    }
};

const initialStateGetErrorLogs: GetErrorLogStateType = {
    error_logs: []
};

export function ErrorLogReducer(state = initialStateGetErrorLogs , action):GetErrorLogStateType {
      switch (action.type) {
          case GET_ERROR_LOGS:
              return {
                ...state,
                error_logs: action.payload
              };
          default:
              return state;
    }
};