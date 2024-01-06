import { io } from 'socket.io-client'

const socket = io('https://xweeter-api-container:5000')

export default socket