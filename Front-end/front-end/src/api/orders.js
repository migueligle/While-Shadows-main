import axios from 'axios'
const BASE_URL = 'http://127.0.0.1:8000/api'

export const fetchOrders = async (params) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: params
    }
    const response = await axios.get(`${BASE_URL}/orders/`, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchOrdersStatus = async (params) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: params
    }
    const response = await axios.get(`${BASE_URL}/orders_status/`, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchCreateOrders = async (dates) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.post(`${BASE_URL}/orders/create/`, dates, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchEditOrder = async (product) => {
  try {
    const token = localStorage.getItem('color')
    const { id, ...data } = product
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.put(`${BASE_URL}/orders/${id}/update/`, data, config)
    return response.data
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchCancelOrder = async (product) => {
  try {
    const token = localStorage.getItem('color')
    const { id, ...data } = product
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.post(`${BASE_URL}/orders/${id}/cancel/`, data, config)
    return response.data
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchReturnOrder = async (product) => {
  try {
    const token = localStorage.getItem('color')
    const { id, ...data } = product
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    const response = await axios.post(`${BASE_URL}/orders/${id}/return/`, data, config)
    return response.data
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
export const fetchOrdersBase = async (params) => {
  try {
    const token = localStorage.getItem('color')
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: params
    }
    const response = await axios.get(`${BASE_URL}/orders_base/`, config)
    return response
  } catch (error) {
    this.$message.error('Error al realizar la petición', error)
    throw error
  }
}
