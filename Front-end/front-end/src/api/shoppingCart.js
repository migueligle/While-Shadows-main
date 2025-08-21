import axios from 'axios'
const BASE_URL = 'http://127.0.0.1:8000/api'

export const fetchShoppingCart = async (params) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      params: params
    }

    if (token) {
      config.headers = {
        Authorization: `Bearer ${token}`
      }
    }

    const response = await axios.get(`${BASE_URL}/shopping-carts/`, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchAddShoppingCart = async (dates) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
    }

    if (token) {
      config.headers = {
        Authorization: `Bearer ${token}`
      }
    }

    const response = await axios.post(`${BASE_URL}/shopping-carts/add/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchRemoveShoppingCart = async (dates) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
    }

    if (token) {
      config.headers = {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.post(`${BASE_URL}/shopping-carts/remove/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchIncrementProduct = async (dates) => {
  try {
    const token = localStorage.getItem('color')
    const config = {}

    if (token) {
      config.headers = {
        Authorization: `Bearer ${token}`
      }
    }

    const response = await axios.post(`${BASE_URL}/shopping-carts/increment/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}

export const fetchDecrementProduct = async (dates) => {
  try {
    const token = localStorage.getItem('color')
    const config = {}

    if (token) {
      config.headers = {
        Authorization: `Bearer ${token}`
      }
    }

    const response = await axios.post(`${BASE_URL}/shopping-carts/decrement/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchDeleteProduct = async (dates) => {
  try {
    const token = localStorage.getItem('color')
    const config = {}

    if (token) {
      config.headers = {
        Authorization: `Bearer ${token}`
      }
    }

    const response = await axios.post(`${BASE_URL}/shopping-carts/remove-product/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
