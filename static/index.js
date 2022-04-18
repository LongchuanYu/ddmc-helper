// var baseUrl = 'http://ddmc.remly.xyz/';
var baseUrl = 'http://192.168.31.98:5000/';
var $axios = axios.create({
    baseURL: baseUrl
})
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
        },
        executeFoods: function() {
        },
        getProxyParams: function(categories=['history_msg', 'thread_name_list', 'duration']) {
            $axios.get('get_proxy_params').then(res => {
                if (categories.includes('history_msg')) {
                    this.historyMsg = res.data.history_msg;
                    this.$refs.content.scrollTop = this.$refs.content.scrollHeight;
                }
                if (categories.includes('thread_name_list')) {
                    let threadNameMap = {
                        check_cart_and_reserve_time_thread: 'checkCart'
                    }
                    threadNameList = res.data.thread_name_list;
                    threadNameList.forEach(threadName => {
                        if (threadName in threadNameMap) {
                            buttonStatusName = threadNameMap[threadName];
                            this.buttonStatus[buttonStatusName] = 'started';
                        }
                    });
                }
                if (categories.includes('duration')) {
                    this.checkCartDuration = res.data.duration;
                }
            })
        },
        getHistoryMsgHeartBeats: function () {
            setInterval(() => {
                this.getProxyParams(['history_msg']);
            }, 3000);
        },
    },
    created: function() {
    },
    mounted: function() {
        this.getProxyParams();
        this.getHistoryMsgHeartBeats();
    }
})
