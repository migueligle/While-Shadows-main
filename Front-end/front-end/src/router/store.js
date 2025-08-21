import Vue from 'vue'
import Vuex from 'vuex'
import { fetchShoppingCart } from '@/api/shoppingCart'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    ShoppingCart: {
      product_count: 0
    }
  },
  mutations: {
    SET_PRODUCT_COUNT (state, count) {
      state.ShoppingCart.product_count = count
    }
  },
  actions: {
    fetchShopping ({ commit }) {
      fetchShoppingCart()
        .then((response) => {
          commit('SET_PRODUCT_COUNT', response.data.product_count)
        })
        .catch((error) => {
          console.error('Error al recuperar datos', error)
        })
    }
  },
  getters: {
    getShoppingCart: state => state.ShoppingCart
  }
})

export default store
