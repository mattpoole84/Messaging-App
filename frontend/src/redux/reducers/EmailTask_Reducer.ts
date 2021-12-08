import {GET_EMAIL_TASKS, GetEmailTasksStateType, EmailTaskActionTypes} from '../types/EmailTask_Types';
  
const initialStateGetEmailTasks: GetEmailTasksStateType = {
    tasks: []
};
  
export default function (state = initialStateGetEmailTasks , action):GetEmailTasksStateType {
      switch (action.type) {
          case GET_EMAIL_TASKS:
              return {
                ...state,
                tasks: action.payload
              };
          default:
              return state;
    }
};