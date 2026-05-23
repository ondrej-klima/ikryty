import axios from "axios"
import {defineStore} from "pinia";

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        errorMessage: null,
        registerErrorMessage: null
    }),
    actions: {
        async register(form) {
            this.$state.registerErrorMessage = null
            await axios.post('register', form).then(async (response) => {
                    if (response.status == 200) {
                        this.$state.registerErrorMessage = null
                        let UserForm = new FormData();
                        UserForm.append('username', form.email);
                        UserForm.append('password', form.password);
                        await this.logIn(UserForm);
                    }
            }).catch(async (error) => {
                if(error.response) {
                    this.$state.registerErrorMessage = error.response.data
                }
            });
        },
        async logIn(user) {
            return await axios.post('login', user)
                    .then(async (response) => {
                        if (response.status == 200) {
                            await this.viewMe();
                            this.$state.errorMessage = null
                        }
                    })
                .catch(async (error) => {
                    if(error.response) {
                        this.$state.errorMessage = error.response.data
                    }
            });
        },
        async viewMe() {
            await axios.get('users/whoami').then((response) => {
                    this.$state.user = response.data
                }).catch(() => {
                    this.$state.user = null
                }
            );
        },
        async logOut() {
            await axios.get('users/logout').then((response) => {
                this.$state.user = null
                console.log(response.data)
            }).catch(() => {
                this.$state.user = null
            })
            this.$state.user = null;
        },
        async isAuthenticated() {
            await this.viewMe()
            return !!this.$state.user
        },
    },
    getters: {


        //isAuthenticated: state => !!state.user,
        stateUser: state => state.user,
    }
})
