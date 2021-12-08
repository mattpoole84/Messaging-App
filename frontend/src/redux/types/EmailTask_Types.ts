import { EmailTask } from '../interfaces/EmailTask';

export const GET_EMAIL_TASKS = 'GET_EMAIL_TASKS';

export interface GetEmailTasksStateType {
  tasks: EmailTask[];
}

interface GetEmailTaskActionType {
  type: typeof GET_EMAIL_TASKS;
  payload: EmailTask[];
}

export type EmailTaskActionTypes = GetEmailTaskActionType;