import { GET_MSG_TASKS } from '../types/MessageTask_Types';
import { MessageTask } from '../interfaces/MessageTask';

export const getMsgTasksAction = (tasks: MessageTask[]) => {
    return {
        type: GET_MSG_TASKS,
        payload : tasks
    };
};

export const getMsgTasks = () => {
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
                phone: 'simba',
                message: 'test',
                status: 'dev',
            },
            {
                id : 2,
                name : 'Heather Morales',
                phone: 'timon@test.com',
                message: 'test',
                status: 'dev',
            },
            {
                id : 3,
                name : 'pumba tang',
                phone: 'pumba@pumba.com',
                message: 'test',
                status: 'dev',
            }
        ]

        return dispatch(getMsgTasksAction(data))
    }
  }