export interface Log {
    id : number;
    type: string;
    description: string;
    send_at: string;
    completed_at: string;
    status: string;
}

export interface ErrorLog{
    id : number;
    error : string;
    description : string;
}