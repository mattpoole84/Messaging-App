import {GET_MSG_TASKS, GetMsgTasksStateType, MsgTaskActionTypes} from '../types/MessageTask_Types';
  
const initialStateGetMsgTasks: GetMsgTasksStateType = {
    tasks: []
};
  
export default function (state = initialStateGetMsgTasks , action):GetMsgTasksStateType {
      switch (action.type) {
          case GET_MSG_TASKS:
              return {
                ...state,
                tasks: action.payload
              };
          default:
              return state;
    }
};