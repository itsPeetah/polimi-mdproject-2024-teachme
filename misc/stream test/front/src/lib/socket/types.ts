export interface SocketEventHandler {
    key: string
    handler: (data: any) => void
}

export type SendMessageFunction = (data: any) => void
export type EmitEventFunction = (key: string, data: any, callback?: (val: any) => void) => void