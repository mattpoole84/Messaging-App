import { MessageTask } from '../interfaces/MessageTask';

export const GET_MSG_TASKS = 'GET_MSG_TASKS';

export interface GetMsgTasksStateType {
  tasks: MessageTask[];
}

interface GetMsgTaskActionType {
  type: typeof GET_MSG_TASKS;
  payload: MessageTask[];
}

export type MsgTaskActionTypes = GetMsgTaskActionType;