var baseUrl = 'http://ddmc.remly.xyz/';
// var baseUrl = 'http://192.168.31.98:5000/';
var $axios = axios.create({
    baseURL: baseUrl
})
var $socket = io();
try {
    var $vConsole = new VConsole();
} catch {}

var app = new Vue({
    el: '#app',
    delimiters: ['[{', '}]'],
    data: {
        buttonStatus: {
            checkCart: 'stopped',
            executeFoods: 'stopped'
        },
        checkCartDuration: '',
        isQuering: false,
        historyMsg: [],
        socketConnected: false,
    },
    methods: {
        checkCart: function() {
            if (this.isQuering) {
                return;
            }
            let payload = {
                thread_name: 'check_cart_and_reserve_time_thread',
                duration: this.checkCartDuration || undefined
            };
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

            this.setDurationToLocalStorage();
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
        },
        setDurationToLocalStorage: function() {
            window.localStorage.setItem('duration', this.checkCartDuration);
        },
        getDurationFromLocalStorage: function() {
            let duration = window.localStorage.getItem('duration');
            if (duration) {
                this.checkCartDuration = duration;
            }
        },
        getHistoryMsg: function() {
            $axios.get('get_history_msg').then(res => {
                this.historyMsg = res.data;
            })
        },
    },
    created: function() {
        $socket.on('connect', (data) => {
            console.log('socket connected!')
            this.socketConnected = true;
        });

    },
    mounted: function() {
        this.getHistoryMsg();
        this.getThreadStatus();
        this.listenSocket();
        this.getDurationFromLocalStorage();
    }
})
