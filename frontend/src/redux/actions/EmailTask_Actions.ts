import { GET_EMAIL_TASKS, EmailTaskActionTypes } from '../types/EmailTask_Types';
import { EmailTask } from '../interfaces/EmailTask';

export const getEmailTasksAction = (tasks: EmailTask[]) => {
    return {
        type: GET_EMAIL_TASKS,
        payload : tasks
    };
};

export const getEmailTasks = () => {
    return (dispatch) => {
        // return axios.get(`${BASE_URL}/trending/all/week?api_key=${API_KEY}&language=en-US`)
        //     .then(response => {
        //         dispatch(fetchTrendData(response.data))
        //     })
        //     .catch(error => {
        //         throw(error);
        //     });
        const data = [
            {
                id : 1,
                name : 'king ba',
                email: 'simba',
                subject: 'test',
                status: 'dev',
            },
            {
                id : 2,
                name : 'Heather Morales',
                email: 'timon@test.com',
                subject: 'test',
                status: 'dev',
            },
            {
                id : 3,
                name : 'pumba tang',
                email: 'pumba@pumba.com',
                subject: 'test',
                status: 'dev',
            }
        ]

        return dispatch(getEmailTasksAction(data))
    }
  }