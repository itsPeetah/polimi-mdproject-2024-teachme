
// import { Manager, Socket } from 'socket.io-client';
// import { RecordAudio } from './RecordAudio';



// export class WebsocketManager{
//     mediaRecorder?: RecordAudio;
//     mediaStream?: MediaStream;
//     audioSocket?: Socket;
//     paused = false;
//     audioSocketNameSpace = 'audio';
//     webSocketURL = 'ws://localhost:3000'
//     saveAudioPath = 'save-audio'
//     onAudioBlobReceived?: (data: any) => void;
//     constructor() {}
//     async start(deviceId: string) {
//         const constraints = {
//             audio: {
//                 deviceId: { exact: deviceId },
//                 echoCancellation: false,
//                 noiseSuppression: false,
//             },
//         };
//         try {
//             this.mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
//             this.mediaRecorder = new RecordAudio(this.mediaStream);
//             const audioSocketManager = new Manager(this.webSocketURL, {
//                 query: {
//                     audioFileName:'my-audio-file-name'
//                    /* ......your query params
//                    for example 
//                     userId: 'xxx-xxx-xxxx-xxxx'
//                   */
//                 },
//                 transports: ['websocket'],
//                 path: this.saveAudioPath,
//                 timeout: 200000,
//             });

//             this.audioSocket = audioSocketManager.socket(this.audioSocketNameSpace, {
//                 auth: {
//                     authorization: 'authorization key',
//                 },
//             });
//             this.audioSocket.on('connect', () => {
            
//             });
//            /*
//             Handle on error and on disconnnecti websocket
//             this.audioSocket.on('disconnect',(e)=>{console.log(e);})
//              this.audioSocket.on('error',(e)=>{console.log(e);})       
//           */
//            this.mediaRecorder.addEventListener('dataavailable', (data: any) => {
//              this.audioSocket?.emit('recording', data);
//           });
//           this.mediaRecorder.start();
//          // send start recording command
//          this.audioSocket.emit('start-recording', 'start');
//         } catch (e) {
//             console.log(e);
//             // handle error here
//         }
//     }

//     stop() {
//         this.closeResources();
//     }

//     cancel() {
//           this.closeResources();
//     }

//     getState() {
//         return ToUserStateMap[this.state];
//     }

//     pause() {
//         this.paused = true;
//     }
  

//     onWebSocketError(event: any) {
//         this.handleError();
//         this.closeResources();
//     }


//     closeResources() {
//         try {
//             this.audioSocket?.disconnect();
//             this.audioSocket?.emit('end-recording', 'end');
//             this.stopAllMicrophoneInstances();
//             this.audioSocket = undefined;         
//         } catch (e) {
//             console.log(e);
//         }
//         if (this.mediaRecorder) {
//             this.mediaRecorder.stop();
//             this.mediaRecorder = undefined;
//         }
//     }

//     stopAllMicrophoneInstances() {
//         if (this.mediaRecorder) {
//             this.mediaRecorder.removeEventListener('dataavailable', ()=>{this.onMediaRecorderData()});
//             this.mediaRecorder.stop();
//             this.mediaRecorder = undefined;
//         }
//         if (this.mediaStream !== null) {
//             this.mediaStream?.getTracks().forEach(function (track) {
//                 track.stop();
//             });
//             this.mediaStream = undefined;
//         }
//     }

//     handleError(status: any, message: string) {
//         if (this.onError) {
//             this.onError(status, message);
//         }
//     }

//     handleFinished() {
//         this.onFinished();
//     }
// }