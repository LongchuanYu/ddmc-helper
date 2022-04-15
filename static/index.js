var $axios = axios.create({
    baseURL: 'http://192.168.31.98:5000/',
})
var $socket = io();
$socket.on('connect', function(data) {
    console.log('socket connected!')
});
var app = new Vue({
    el: '#app',
    delimiters: ['[{', '}]'],
    data: {
        buttonStatus: {
            checkCart: 'stopped',
            executeFoods: 'stopped'
        },
        isQuering: false,
        historyMsg: []
    },
    methods: {
        checkCart: function() {
            if (this.isQuering) {
                return;
            }
            let payload = {thread_name: 'check_cart_and_reserve_time_thread'};
            this.isQuering = true;
            if (this.buttonStatus.checkCart === 'stopped') {
                $axios.post('check_cart_and_reserve_time', payload).then(res => {
                    this.isQuering = false;
                    this.buttonStatus.checkCart = 'started';
                })
            } else {
                $axios.post('stop_thread', payload).then(res => {
                    this.isQuering = false;
                    this.buttonStatus.checkCart = 'stopped';
                })
            }
        },
        executeFoods: function() {
        },
        listenSocket: function() {
            $socket.on('common', (data) => {
                if (data.msg) {
                    this.historyMsg.push(data.msg);
                }
            })
        },
        getThreadStatus: function() {
            let threadNameMap = {
                check_cart_and_reserve_time_thread: 'checkCart'
            }
            $axios.get('get_started_thread').then(res => {
                res.data.forEach(threadName => {
                    if (threadName in threadNameMap) {
                        buttonStatusName = threadNameMap[threadName];
                        this.buttonStatus[buttonStatusName] = 'started';
                    }
                });
            })
        }
    },
    created: function() {
        this.getThreadStatus();
    },
    mounted: function() {
        this.listenSocket()
    }
})