import axios, { AxiosRequestHeaders } from "axios";
import { createStore, ActionContext, Store } from "vuex"
import { authService, basePath } from "../api";

type UserLogin = {
    username: string,
    password: string
}

type User = {
    username: string
}

const state = {
    user: {username: ""} as User,
    isLoggedIn: false,
    definitions: {} as Record<string, Array<{type: string, english: Array<string>}>>
};

type State = typeof state

const getters = {
    isLoggedIn: (state: State) => state.isLoggedIn,
    user: (state: State) => state.user,
    defintionFor: (state: State) => (word: string) => {
        if (!state.definitions[word]) {
            store.dispatch(ActionTypes.getWordDefinition, word)
        }
        return state.definitions[word]
    }
};

const actions = {
    async registerUser({dispatch} : Context, login: UserLogin){
        return await authService.post("/register", {"username": login.username, "password": login.password}, { withCredentials: true})
    },

    async loginUser(context: Context, login: UserLogin){
        const data = await authService.post("/login", {"username": login.username, "password": login.password}, { withCredentials: true })
        context.dispatch(ActionTypes.fetchUser)
        return data    
    },

    async fetchUser(context: Context) {
        const data = await authService.get("/user", { withCredentials: true }) as User
        context.commit(MutationTypes.setUser, data)
    },

    async logoutUser(context: Context) {
        await authService.get("/logout", { withCredentials: true })
        context.commit(MutationTypes.logoutUserState, undefined)
    },

    async getWordDefinition(context: Context, word: string) {
        const response = await axios.get(basePath + "/api/dictionary/define", {params: {"word": word}, withCredentials: true})
        context.state.definitions[word] = response.data["definitions"]
    }
};


const mutations = {
    setUser(state: State, user: User){
        state.isLoggedIn = true;
        state.user = user;
    },
    logoutUserState(state: State){
        state.isLoggedIn = false,
        state.user = {username: ""};
    }
}

function listKeys(obj: object) {
  return Object.assign({}, ...Object.keys(obj).map(key => ({ [key]: key })))
}

export type Getters = {
    [P in keyof typeof getters]: ReturnType<typeof getters[P]>
}
export type Actions = typeof actions
export type Mutations = typeof mutations
export const ActionTypes = listKeys(actions) as Record<keyof Actions, keyof Actions> 
export const MutationTypes = listKeys(mutations) as Record<keyof Mutations, keyof Mutations>

type MutationsProp = {
  commit<K extends keyof Mutations>(key: K, payload: Parameters<Mutations[K]>[1]): ReturnType<Mutations[K]>
}

export type Context = Omit<ActionContext<State, State>, "commit"> & MutationsProp

const store = createStore({
    state,
    getters,
    actions,
    mutations
});

export default store
