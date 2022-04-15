var $axios = axios.create({
    baseURL: 'http://localhost:5000/',
    transformRequest: [function(data, header) {
        // tmp = Qs.stringify(data)
        console.log(tmp)
        return tmp;
    }],
    timeout: 2000,
})
var config = {
    baseURL: 'http://localhost:5000/',
    transformRequest: [function(data, header) {
        tmp = Qs.stringify(data)
        console.log(tmp)
        return tmp;
    }],
    timeout: 2000,
}
var app = new Vue({
    el: '#app',
    delimiters: ['[{', '}]'],
    data: {
        buttonStatus: {
            checkCart: 'stopped',
            executeFoods: 'stopped'
        },
        test: [0]
    },
    methods: {
        checkCart: function() {
            let payload = {thread_name: 'check_cart_and_reserve_time_thread'};
            axios.post('check_cart_and_reserve_time', payload, config).then(res => {
                console.log(res)
                this.buttonStatus.checkCart = 'started';
            })
            return;
            if (this.buttonStatus.checkCart === 'stopped') {
                $axios.post('check_cart_and_reserve_time', payload).then(res => {
                    console.log(res)
                    this.buttonStatus.checkCart = 'started';
                })
            } else {
                $axios.post('stop_all').then(res => {
                    console.log(res)
                    this.buttonStatus.checkCart = 'stopped';
                })
            }
        },
        executeFoods: function() {
            this.stopAll(1);
        },
    },
    created: function() {

    }
})