import { GET_ERROR_LOGS, GET_LOGS } from '../types/Log_Types';
import { Log, ErrorLog } from '../interfaces/Log';

export const getLogsAction = (logs: Log[]) => {
    return {
        type: GET_LOGS,
        payload : logs
    };
};

export const getErrorLogsAction = (logs: ErrorLog[]) => {
    return {
        type: GET_ERROR_LOGS,
        payload : logs
    };
};

export const getLogs = () => {
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
                type : 'king ba',
                description: 'simba',
                send_at: 'test',
                completed_at: 'dev',
                status : 'ready'
            },
            {
                id : 2,
                type : 'Heather Morales',
                description: 'timon@test.com',
                send_at: 'test',
                completed_at: 'dev',
                status : 'ready'
            },
            {
                id : 3,
                type : 'pumba tang',
                description: 'pumba@pumba.com',
                send_at: 'test',
                completed_at: 'dev',
                status : 'ready'
            }
        ]

        return dispatch(getLogsAction(data))
    }
}
export const getErrorLogs = () => {
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
                error : 'king ba',
                description: 'simba',
            },
            {
                id : 2,
                error : 'Heather Morales',
                description: 'timon@test.com',
            },
            {
                id : 3,
                error : 'pumba tang',
                description: 'pumba@pumba.com',
            }
        ]

        return dispatch(getErrorLogsAction(data))
    }
  }